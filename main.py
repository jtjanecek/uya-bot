from datetime import datetime	
import requests
import discord
from discord.ext import tasks
import asyncio
import os

client = discord.Client()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

import requests 

from datetime import datetime
from pytz import timezone
import pytz

def getDate():
    date_format='%m/%d/%Y %H:%M:%S %Z'
    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    return 'Updated at: ' + date.strftime(date_format)

def callPlayers():
    playersRes = requests.get("http://s2online.socomcommunity.com/api/universes/players?applicationId=10684")
    info = playersRes.json()
    return info

def callGames():
    gameRes = requests.get("http://s2online.socomcommunity.com/api/rooms/68")
    gameInfo = gameRes.json()
    return gameInfo

def getPlayers(res):
    players = "Players Online:\n"
    for player in res:
        players+= "-"+player["name"] +"\n"
    return players

def getGames(info):
    print("Info:", info)
    res = "No Games :(" if len(info) == 0 else "Current Games:\n"
    for game in info:
        if game['players'] == []:
            continue
        host = game['players'][0]['name']
        host+= "'s"
        res+= "{}, Occupancy: ({}/{})\n".format(host, game['playerCount'], game['maxPlayers'])
    return res

def numPlayers(info):
    res = "Nobody is online." if len(info) == 0 else "There are {} players online.".format(len(info))
    return res

def getText():
    
    info = callPlayers()
    players = getPlayers(info)

    gameInfo = callGames()
    games = getGames(gameInfo)

    return getDate() + '```\n' + players + '\n```' + '\n\n ```' + games + '```'

@client.event
async def on_ready():
    print("Bot is ready...")

    channel = client.get_channel(CHANNEL_ID)

	# First message
    text = getText()
    message = await channel.send(getText())

    while True:
        await asyncio.sleep(60)
        print(datetime.now())
        await message.edit(content=getText())

client.run(TOKEN)
