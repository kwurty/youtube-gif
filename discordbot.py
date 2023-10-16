# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import random

from pytube import YouTube
from moviepy.editor import *
from conversion import Conversions
import tempfile
import re
import os

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def gif(ctx, url: str, time: str, length:int = 3, message:str = ""):

    match = re.match("^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$", url)
    if not match:
        await ctx.send("Bad Youtube URL")
        return

    youtube = YouTube(url)


    timearr = time.split(":")
    if not len(timearr) == 3:
        await ctx.send("Please enter a correct time format (HH:MM:SS)")
        return
        
    hours = timearr[0]
    minutes = timearr[1]
    seconds = timearr[2]
    print(hours, minutes, seconds)
    startTime = (int(hours) * 60 * 60) + (int(minutes) * 60) + int(seconds)

    if(startTime > youtube.length):
        await ctx.send(f"The time entered is longer than the actual video ")
        return
    
    if not isinstance(length, int) or length < 1 or length > 5:
        await ctx.send(f"Enter a length of between 1-5")
        return

    conversion = Conversions(youtube, "/", startTime, length)
    conversion.find720p()
    conversion.downloadVideo()
    conversion.setClipLocation()
    if len(message) > 0:
        conversion.addText(message)
    conversion.exportGif()

    with open(conversion.videoLocation, 'rb') as f:
        picture = discord.File(conversion.gifLocation)
        await ctx.send(file=picture)
    # await ctx.send(file=discord.File(conversion.videoLocation))



@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')


bot.run(os.environ['discord_api_key'])