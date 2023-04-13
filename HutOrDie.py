import asyncio
import discord
import time
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='>', intents=intents)
asking_channels = {}

pizza_str = ['pizza', '피자', '🍕']
yes_str = ['yes', 'ok', 'yep', 'yeah', '응', '그래', '좋아', 'ㅇㅇ']
no_str = ['dominos', 'no', 'nope', 'nah', '도미노', '아니' ,'ㄴㄴ', '안돼']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_guild_join(guild):
    print(f'Joined in {guild.name}')

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    if message.channel in asking_channels:
        if any(n_str in message.content.lower() for n_str in no_str):
            client = asking_channels[message.channel]
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./shoot.wav"), volume=0.5)
            client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
            await message.channel.send(f'🔫')
            time.sleep(1.0)
            await client.disconnect()
            del asking_channels[message.channel]
        elif any(y_str in message.content.lower() for y_str in yes_str):
            client = asking_channels[message.channel]
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./nomnom.wav"), volume=0.5)
            client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
            await message.channel.send(f'👍')
            time.sleep(13.0)
            await client.disconnect()
            del asking_channels[message.channel]
    else:
        if any(p_str in message.content.lower() for p_str in pizza_str ):
            if message.author.voice:
                client = await message.author.voice.channel.connect()
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./pizzahut.wav"), volume=0.5)
                client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
                await message.channel.send("Pizza Hut?")
                asking_channels[message.channel] = client
            else:
                await message.channel.send("Where are you? 🔫👀")

bot.run('token')
