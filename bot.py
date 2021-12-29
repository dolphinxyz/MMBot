#!/usr/bin/env python3
import os
import sys
import time
import json
import discord
import datetime
import requests
import threading
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
MM_CMC_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
MM_CMC_PARAMS = {'slug':'million'}

# GLOABL VARIABLES
PRICE = 0
volume = 0
rank = 0

client = commands.Bot(command_prefix = '!')

@client.command()
async def ping(ctx):
    await ctx.send("PONG")
    
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

@client.command()
async def rank(ctx):
    await ctx.send(RANK)

@client.event
async def on_ready():
    ChangeChannelNameMembers.start()
    ChangeChannelNamePrice.start()
    ChangeChannelNameDays.start()
    ExtractCoinMarketCap.start()

@tasks.loop(seconds=120)
async def ExtractCoinMarketCap():
    global PRICE, VOLUME, RANK
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
        RANK = data['data']['10866']['cmc_rank']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print("ERROR:\n\t", e)

@tasks.loop(seconds=60)
async def ChangeChannelNameMembers():
    guild = client.get_guild(GUILD_ID)
    member_count = str(guild.member_count)
    channel_member = client.get_channel(CHANNEL_MEMBER_ID)
    output_member = member_count + ' members'
    await channel_member.edit(name=output_member)

@tasks.loop(seconds=60)
async def ChangeChannelNamePrice():
    channel_price = client.get_channel(CHANNEL_PRICE_ID)
    s_price = str(int(PRICE)) + ' usd'
    await channel_price.edit(name=s_price)

@tasks.loop(seconds=86400)
async def ChangeChannelNameDays():
    channel_days = client.get_channel(CHANNEL_DAYS_ID)
    today = datetime.date.today()
    genesis = datetime.date(2021, 7, 1)
    delta_days = today - genesis
    s_days = str(delta_days.days) + ' days'
    await channel_days.edit(name=s_days)

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "prod":
        client.run(TOKEN)
    if mode == "test":
        client.run(TOKEN_TEST)

