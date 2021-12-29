#!/usr/bin/env python3
import os
import sys
import time
import json
import discord
import requests
import threading
from dotenv import load_dotenv
from discord.ext import tasks

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN_TEST = os.getenv('DISCORD_TOKEN_TEST')
COINMARKETCAP_TOKEN = os.getenv('COINMARKETCAP_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
CHANNEL_MEMBER_ID = int(os.getenv('CHANNEL_MEMBER_ID'))
CHANNEL_PRICE_ID = int(os.getenv('CHANNEL_PRICE_ID'))
MM_CMC_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
MM_CMC_PARAMS = {'slug':'million'}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': COINMARKETCAP_TOKEN,
}

client = discord.Client()

price = 0
volume = 0
rank = 0
def ExtractCoinMarketCap():
    global price, volume, rank
    while True:
        try:
            response = requests.get(
                MM_CMC_URL,
                params=MM_CMC_PARAMS,
                headers=headers
            )
            data = json.loads(response.text)
            price = data['data']['10866']['quote']['USD']['price']
            volume = data['data']['10866']['quote']['USD']['volume_24h']
            rank = data['data']['10866']['cmc_rank']
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print("ERROR:\n\t", e)
        time.sleep(120)

@client.event
async def on_ready():
    ChangeChannelNames.start()

@tasks.loop(seconds=60)
async def ChangeChannelNames():
    guild = client.get_guild(GUILD_ID)
    member_count = str(guild.member_count)
    channel_member = client.get_channel(CHANNEL_MEMBER_ID)
    output_member = member_count + ' members'
    await channel_member.edit(name=output_member)
    channel_price = client.get_channel(CHANNEL_PRICE_ID)
    s_price = str(int(price)) + ' usd'
    await channel_price.edit(name=s_price)

@client.event
async def on_message(message):
    if message.content.startswith('!price'):
        r_price = round(price, 2)
        s_price = str(r_price) + '$'
        await message.reply(s_price, mention_author=True)
    if message.content.startswith('!volume'):
        r_volume = round(volume)
        s_volume = f"${r_volume:,}"
        await message.reply(s_volume, mention_author=True)
    if message.content.startswith('!rank'):
        await message.reply(rank, mention_author=True)

if __name__ == "__main__":
    mode = sys.argv[1]
    threading.Thread(target=ExtractCoinMarketCap).start()
    if mode == "prod":
        client.run(TOKEN)
    if mode == "test":
        client.run(TOKEN_TEST)

