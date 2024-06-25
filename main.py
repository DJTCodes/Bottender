import asyncio
import discord
import os
import nacl
import random
import sys
import yt_dlp
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix='!')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.command(name='help')
async def help(ctx):
    help_menu = '''
    Here are the commands you can call:
    ================================

    !hello - Say hello to the bot.

    !beer_me - Order a frosty cold beer.

    !russian_roulette - Feeling lucky?

    !play_music - ex) !play_music YOUTUBEURLHERE

    !roll_dice - Roll the dice.

    !log_off - Make me log off.

    ================================
    To use any of these commands, simply type the command name (including the !) in the chat.
    '''
    await ctx.send(help_menu)

def russian_roulette_game(members):
    victim = random.choice(members)
    return victim


@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command(name='beer_me')
async def beer_me(ctx):
    member = ctx.author.name
    await ctx.send(f'*Pours a frosty cold root beer and slides it over to {member}.*')

# @bot.command(name='dice_game')
# async def roll_dice(ctx):
#     #player turn
#     die_one = random.randint(1, 6)
#     die_two = random.randint(1, 6)
#     dice_roll = die_one + die_two
#     await ctx.send(f"You rolled a {dice_roll}!")
#     #bot turn
#     await ctx.send("Now it's my turn...")
#     bot_one = random.randint(1,6)
#     bot_two = random.randint(1,6)
#     bot_roll = bot_one + bot_two
#     await ctx.send(f"I rolled a {bot_roll}")
#     #who win
#     if(dice_roll > bot_roll):
#         await ctx.send("Rats! You win.")
#     elif(dice_roll < bot_roll):
#         await ctx.send("You lose. GG.")
#     else:
#         await ctx.send("A draw!")

@bot.command(name='roll_dice')
async def roll_dice(ctx):
    die_one = random.randint(1, 6)
    die_two = random.randint(1, 6)
    dice_roll = die_one + die_two
    await ctx.send(f"You rolled a {dice_roll}!")

@bot.command(name='russian_roulette')
async def russian_roulette(ctx):
    members = ctx.author.voice.channel.members
    victim = russian_roulette_game(members)
    await ctx.send(f'*The gun points to {victim.name}*\nGoodbye!')
    await victim.edit(voice_channel=None)

@bot.command(name='play_music')
async def play_music(ctx, url: str):

    channel = ctx.author.voice.channel

    voice_channel = get(bot.voice_clients, guild=ctx.guild)

    if voice_channel and voice_channel.is_connected():
        await voice_channel.move_to(channel)
    else:
        voice_channel = await channel.connect()

    with yt_dlp.YoutubeDL({'format': 'bestaudio'}) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']

    def my_after(error):
        coro = voice_channel.disconnect()
        fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
        try:
            fut.result()
        except Exception as e:
            print(f"An error has occurred: {e}", file=sys.sterr)

    voice_channel.play(discord.FFmpegPCMAudio(URL), after=my_after)

@bot.command(name='stop_music')
async def stop_music(ctx):
    voice_channel = get(bot.voice_clients, guild=ctx.guild)
    if voice_channel and voice_channel.is_playing():
        voice_channel.stop()

@bot.command(name='log_off')
async def log_off(ctx):
    await ctx.send('Goodbye.')
    await bot.close()


