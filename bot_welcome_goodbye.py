#!/usr/bin/env python3
import os
import sys
import discord
from discord.ext import commands
from dotenv import load_dotenv

# ENVIRONMENTAL VARIABLES
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_INTRO = int(os.getenv('CHANNEL_INTRO'))
CHANNEL_WELCOME = int(os.getenv('CHANNEL_WELCOME'))
CHANNEL_GOODBYE = int(os.getenv('CHANNEL_GOODBYE'))
CHANNEL_ROLES = int(os.getenv('CHANNEL_ROLES'))

intents = discord.Intents.all()
client = commands.Bot(
    command_prefix = '!', 
    intents=intents
)

@client.event
async def on_member_join(member):
   await client.get_channel(CHANNEL_WELCOME).send(
        f"""Ehy {member.mention} welcome to Million Token,
        say something cool about you on <#{CHANNEL_INTRO}>
        and add some fancy roles to you on <#{CHANNEL_ROLES}>!""")

@client.event
async def on_member_remove(member):
   await client.get_channel(CHANNEL_GOODBYE).send(
        f"{member.name} has left")

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "prod":
        client.run(TOKEN)
    if mode == "test":
        client.run(TOKEN_TEST)
