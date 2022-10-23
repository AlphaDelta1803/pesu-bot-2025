import discord # discord module is an API wrapper for discord written in python
from discord.ext import commands 
import os #allows us to interact with the operating system using python
from dotenv import load_dotenv #used to access environment variables
from discord_slash import SlashCommand  #discord_slash is a python API wrapper for discord interactions

load_dotenv('.env') #loads the environment variables file

client = commands.Bot(command_prefix='p!', help_command=None, intents=discord.Intents().all()) 
#initialises a discord bot with the prefix for its commands set to p!

#having no help command, and subscribed (listening) to all events
slash = SlashCommand(client, sync_on_cog_reload = True, sync_commands=True)

# .env summons
BOT_LOGS = os.getenv('BOT_LOGS')   # Bot Logs channel ID
BOTDEV_ROLE = os.getenv('BOTDEV_ROLE')   # Bot Dev' Role ID
BOT_TOKEN = os.getenv('DISCORD_TOKEN')   # Returns value of the environment variable with key == DISCORD_TOKEN


@client.command(aliases = ['loadit'])   # Decorator that loads cog 
async def load(ctx, extension):   # Function that loads cog
    bot_devs = discord.utils.get(ctx.guild.roles, id=BOTDEV_ROLE)
    if(bot_devs in ctx.author.roles):
        try:
            client.load_extension(f"cogs.{extension}")
            success_msg = f"cogs.{extension} was loaded succesfully"
            await ctx.channel.send(success_msg)
            await client.get_channel(BOT_LOGS).send(success_msg)
        except Exception as err:   # Except block to handle any exceptions encountered
            await ctx.channel.send(err)
    else:
        await ctx.channel.send("Unauthorised. How did you find this wtf-")


@client.command(aliases = ['unloadit'])   # Decorator that unloads cog
async def unload(ctx, extension):   # Function that unloads cog
    bot_devs = discord.utils.get(ctx.guild.roles, id=BOTDEV_ROLE)
    if(bot_devs in ctx.author.roles):
        try:
            client.unload_extension(f"cogs.{extension}")
            success_msg = f"cogs.{extension} was unloaded succesfully"
            await ctx.channel.send(success_msg)
            await client.get_channel(BOT_LOGS).send(success_msg)
        except Exception as err: #except block to handle any exceptions encountered
            await ctx.channel.send(err)
    else:
        await ctx.channel.send("Unauthorised. How did you find this wtf-")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}") #uses string slicing to use only the file name without the extension


client.run(BOT_TOKEN)  # Line that runs the bot
