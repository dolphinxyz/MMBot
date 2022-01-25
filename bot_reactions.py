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
TL_EMOJIS = json.loads(os.getenv('TL_EMOJIS'))
MM_EMOJIS = json.loads(os.getenv('MM_EMOJIS'))
BTC_EMOJIS = json.loads(os.getenv('BTC_EMOJIS'))
ETH_EMOJIS = json.loads(os.getenv('ETH_EMOJIS'))

EMOJIS_DICT = [
    {
        "category": "techlead",
        "custom": True, 
        "keywords": [' TL', 'TL ', 'tl ', 'techlead', 'patrik'],
        "ids": TL_EMOJIS
    },
    {
        "category": "million",
        "custom": True,
        "keywords": ['million', ' MM', 'MM ', 'mm ', ' mm'],
        "ids": MM_EMOJIS
    },
    {
        "category": "bitcoin",
        "custom": True,
        "keywords": ['btc', 'BTC', 'Bitcoin', 'bitcoin', 'BITCOIN'],
        "ids": BTC_EMOJIS
    },
    {
        "category": "ethereum",
        "custom": True,
        "keywords": ['eth', 'ETH', 'Ethereum', 'ethereum', 'ETHEREUM'],
        "ids": ETH_EMOJIS
    },
    {
        "category": "lfg",
        "custom": False,
        "keywords": ['lfg', 'LFG'],
        "ids": ['🇱', '🇫', '🇬']
    },
    {
        "category": "moon",
        "custom": False,
        "keywords": ['moon'],
        "ids": ['🇲', '🇴', '🅾️', '🇳', '🌝'],
    }
]

intents = discord.Intents.all()
client = commands.Bot(
    command_prefix = '!', 
    intents=intents
)

@client.event
async def on_message(message):
    message_content = message.content
    for i in EMOJIS_DICT:
        for key in i['keywords']:
            if key in message_content:
                for emoji in i['ids']:
                    if i['custom']:
                        reaction = client.get_emoji(emoji)
                        await message.add_reaction(reaction)
                    else:
                        await message.add_reaction(emoji)

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "prod":
        client.run(TOKEN)
    if mode == "test":
        client.run(TOKEN_TEST)
