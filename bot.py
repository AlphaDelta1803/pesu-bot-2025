import discord #discord module is an API wrapper for discord written in python
from discord.ext import commands 
import os #allows us to interact with the operating system using python
from dotenv import load_dotenv #used to access environment variables
from discord_slash import SlashCommand  #discord_slash is a python API wrapper for discord interactions

load_dotenv('.env') #loads the environment variables folder
TOKEN = os.getenv('DISCORD_TOKEN') #returns value of the environment variable with key == DISCORD_TOKEN

client = commands.Bot(command_prefix='p!', help_command=None, intents=discord.Intents().all()) 
#initialises a discord bot with the prefix for its commands set to p!
#having no help command, and subscribed (listening) to all events
slash = SlashCommand(client, sync_on_cog_reload = True, sync_commands=True)

BOT_LOGS = 931523901731799080
BOT_ROLE = 931588180174589983 #bot role id


@client.command(aliases = ['loadit'])
async def load(ctx, extension): #loads the cog
    bot_devs = discord.utils.get(ctx.guild.roles, id=BOT_ROLE)
    if(bot_devs in ctx.author.roles):
        try:
            client.load_extension(f"cogs.{extension}")
            success = f"cogs.{extension} was loaded succesfully"
            await ctx.channel.send(success)
            await client.get_channel(BOT_LOGS).send(success)
        except Exception as e: #except block to handle any exceptions encountered
            await ctx.channel.send(e)
    else:
        await ctx.channel.send("Unauthorised")


@client.command(aliases = ['unloadit'])
async def unload(ctx, extension): #unloads the cog
    bot_devs = discord.utils.get(ctx.guild.roles, id=BOT_ROLE)
    if(bot_devs in ctx.author.roles):
        try:
            client.unload_extension(f"cogs.{extension}")
            success = f"cogs.{extension} was unloaded succesfully"
            await ctx.channel.send(success)
            await client.get_channel(BOT_LOGS).send(success)
        except Exception as e: #except block to handle any exceptions encountered
            await ctx.channel.send(e)
    else:
        await ctx.channel.send("Unauthorised")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}") #uses string slicing to use only the file name without the extension


client.run(TOKEN)
