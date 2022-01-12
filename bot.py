#!/usr/bin/env python3
import os
import sys
import time
import json
import discord
import datetime
import requests
from dotenv import load_dotenv
from discord.ext import tasks, commands

# ENVIRONMENTAL VARIABLES
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN_TEST = os.getenv('DISCORD_TOKEN_TEST')
COINMARKETCAP_TOKEN = os.getenv('COINMARKETCAP_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
CHANNEL_MEMBER_ID = int(os.getenv('CHANNEL_MEMBER_ID'))
CHANNEL_PRICE_ID = int(os.getenv('CHANNEL_PRICE_ID'))
CHANNEL_DAYS_ID = int(os.getenv('CHANNEL_DAYS_ID'))
CHANNEL_ONLINE_ID = int(os.getenv('CHANNEL_ONLINE_ID'))
MM_CMC_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
MM_CMC_PARAMS = {'slug':'million'}
COVALENT_URL = os.getenv('COVALENT_URL')
COVALENT_API_TOKEN = os.getenv('COVALENT_API_TOKEN')
SOLSCAN_URL = os.getenv('SOLSCAN_URL')
CHANNEL_HOLDERS_ETHEREUM = int(os.getenv('CHANNEL_HOLDERS_ETHEREUM'))
CHANNEL_HOLDERS_POLYGON = int(os.getenv('CHANNEL_HOLDERS_POLYGON'))
CHANNEL_HOLDERS_KUSAMA = int(os.getenv('CHANNEL_HOLDERS_KUSAMA'))
CHANNEL_HOLDERS_AVALANCHE = int(os.getenv('CHANNEL_HOLDERS_AVALANCHE'))
CHANNEL_HOLDERS_BINANCE = int(os.getenv('CHANNEL_HOLDERS_BINANCE'))
CHANNEL_HOLDERS_SOLANA = int(os.getenv('CHANNEL_HOLDERS_SOLANA'))
CHANNEL_HOLDERS_TOTAL = int(os.getenv('CHANNEL_HOLDERS_TOTAL'))
CHANNEL_WELCOME = int(os.getenv('CHANNEL_WELCOME'))
CHANNEL_GOODBYE = int(os.getenv('CHANNEL_GOODBYE'))
CHANNEL_INTRO = int(os.getenv('CHANNEL_INTRO'))
MM_EMOJIS = json.loads(os.getenv('MM_EMOJIS'))

COVALENT_DICT = [
    {
        "chain": "ETH",
        "chainid": 1,
        "contract": '0x6b4c7a5e3f0b99fcd83e9c089bddd6c7fce5c611',
        "holders": 0,
        "channelid": CHANNEL_HOLDERS_ETHEREUM
    },
    {
        "chain": "MATIC",
        "chainid": 137,
        "contract": '0x5647fe4281f8f6f01e84bce775ad4b828a7b8927',
        "holders": 0,
        "channelid": CHANNEL_HOLDERS_POLYGON
    },
    {
        "chain": "BSC",
        "chainid": 56,
        "contract": '0xbf05279f9bf1ce69bbfed670813b7e431142afa4',
        "holders": 0,
        "channelid": CHANNEL_HOLDERS_BINANCE
    },
    {
        "chain": "AVAX",
        "chainid": 43114,
        "contract": '0x993163CaD35162fB579D7B64e6695cB076EF5064',
        "holders": 0,
        "channelid": CHANNEL_HOLDERS_AVALANCHE
    },
    {
        "chain": "KSM",
        "chainid": 1285,
        "contract": '0x95bf7e307bc1ab0ba38ae10fc27084bc36fcd605',
        "holders": 0,
        "channelid": CHANNEL_HOLDERS_KUSAMA
    },
]

# GLOABL VARIABLES
PRICE = 0
VOLUME = 0
HOLDERS_ETH = 0
HOLDERS_BSC = 0
HOLDERS_SOL = 0
HOLDERS_MATIC = 0
HOLDERS_AVAX = 0
HOLDERS_KSM = 0
HOLDERS_TOTAL = 0

intents = discord.Intents.all()
client = commands.Bot(
    command_prefix = '!', 
    intents=intents
)

@client.event
async def on_ready():
    ChangeChannelNameMembers.start()
    ChangeChannelNamePrice.start()
    ChangeChannelNameDays.start()
    UpdateOnlineUserCounter.start()
    ExtractCoinMarketCap.start()
    ExtractHolders.start()
    ExtractHoldersSolana.start()
    UpdateHolders.start()
    UpdateHoldersTotal.start()

@client.command()
async def price(ctx):
    r_price = round(PRICE, 2)
    s_price = str(r_price) + '$'
    await ctx.send(s_price)

@client.command()
async def volume(ctx):
    r_volume = round(VOLUME)
    s_volume = f"${r_volume:,}"
    await ctx.send(s_volume)

@tasks.loop(seconds=240)
async def ExtractCoinMarketCap():
    global PRICE, VOLUME
    try:
        response = requests.get(
            MM_CMC_URL,
            params=MM_CMC_PARAMS,
            headers = {
              'Accepts': 'application/json',
              'X-CMC_PRO_API_KEY': COINMARKETCAP_TOKEN,
            }
        )
        data = json.loads(response.text)
        PRICE = data['data']['10866']['quote']['USD']['price']
        VOLUME = data['data']['10866']['quote']['USD']['volume_24h']
    except Exception as e:
        print("ERROR ExtractCoinMarketCap:\n\t", e)

@tasks.loop(seconds=200)
async def ExtractHolders():
    for i in COVALENT_DICT:
        try:
            temp_chain = i['chainid']
            temp_contract = i['contract']
            temp_url = COVALENT_URL.format(
                chain=temp_chain,
                contract=temp_contract,
                pageSize = 100000,
                covalentkey = COVALENT_API_TOKEN
            )
            response = requests.get(temp_url)
            data = json.loads(response.text)
            i['holders'] = len(data['data']['items'])
        except Exception as e:
            print("ERROR ExtractHolders:\n\t", i['chain'], e)

@tasks.loop(seconds=200)
async def ExtractHoldersSolana():
    global HOLDERS_SOL
    try:
        response = requests.get(SOLSCAN_URL)
        data = json.loads(response.text)
        holder = data['holder']
        HOLDERS_SOL = holder
        channel = client.get_channel(CHANNEL_HOLDERS_SOLANA)
        output = str(HOLDERS_SOL) + ' SOL'
        await channel.edit(name=output)
    except Exception as e:
        print("ERROR ExtractHoldersSolana:\n\t", e)

@tasks.loop(seconds=200)
async def UpdateHolders():
    for i in COVALENT_DICT:
        channel = client.get_channel(i['channelid'])
        output = str(i['holders']) + ' ' + i['chain']
        await channel.edit(name=output)

@tasks.loop(seconds=120)
async def UpdateHoldersTotal():
    total = 0
    for i in COVALENT_DICT:
        total = total + i['holders']
    total = total + HOLDERS_SOL
    channel_total = client.get_channel(CHANNEL_HOLDERS_TOTAL)
    output_total = str(total)
    await channel_total.edit(name=output_total)

@tasks.loop(seconds=60)
async def ChangeChannelNameMembers():
    guild = client.get_guild(GUILD_ID)
    member_count = str(guild.member_count)
    channel_member = client.get_channel(CHANNEL_MEMBER_ID)
    output_member = member_count + ' MEMBERS'
    await channel_member.edit(name=output_member)

@tasks.loop(seconds=60)
async def UpdateOnlineUserCounter():
    channel_online = client.get_channel(CHANNEL_ONLINE_ID)
    members = client.get_all_members()
    count_online = 0
    for member in members:
        if str(member.status) != "offline":
            if not member.bot:
                count_online = count_online + 1
    s_online = str(count_online) + ' ONLINE'
    await channel_online.edit(name=s_online)

@tasks.loop(seconds=60)
async def ChangeChannelNamePrice():
    channel_price = client.get_channel(CHANNEL_PRICE_ID)
    s_price = str(round(PRICE, 2)) + ' $'
    await channel_price.edit(name=s_price)

@tasks.loop(seconds=86400)
async def ChangeChannelNameDays():
    channel_days = client.get_channel(CHANNEL_DAYS_ID)
    today = datetime.date.today()
    genesis = datetime.date(2021, 7, 1)
    delta_days = today - genesis
    s_days = str(delta_days.days) + ' DAYS'
    await channel_days.edit(name=s_days)

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "prod":
        client.run(TOKEN)
    if mode == "test":
        client.run(TOKEN_TEST)
