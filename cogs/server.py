import discord
from discord.ext import commands, tasks
import os
import asyncio
import base64
from discord.utils import get
from datetime import datetime
from selenium import webdriver
from pathlib import Path
from cogs.helpers import helpers
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash import cog_ext, utils

os.getenv('BOT_TEST') 
os.getenv('BOT_LOGS')
os.getenv('GUILD_ID')
os.getenv('botID')
os.getenv('MOD_LOGS')

ADMIN = 1032709443940524228
MODS = 1032709443940524227
BOT_DEVS = 1032709443940524226
JUST_JOINED = 1032714828197937152
VERIFIED = 1032714872695304203
SENIOR = 1032714925832949820






class server(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.uptimeinfo ="`p!uptime` or `p!ut`\n\n\nShows how long the bot has been online for\n\n"
        self.loadit = "`p!loadit <extention>`\n\n\nLoads the extention\n\n"
        self.unloadit = "`p!unloadit <extention>`\n\nUnloads the extention\n\n"
        self.polsho = "`p!pollshow` or `p!ps <pollMsgLink>`\n\nShows the results of the poll\n\n"
        self.pull = "`p!pull`\n\nPull the latest code of the bot. Maybe.\n\n"
        self.scrape = "`p!scrape`\n\nIdk how this works tbh :upside_down:\n\n"
        self.rest = "`p!restart`\n\nRestarts the bot :flushed:\n\n"
        self.confessen = "`p!enableconfess`\n\n\nEnables the confess feature\n\n"
        self.confessdis = "`p!disableconfess`\n\n\nDisables the confess feature\n\n"
	#self.confbanusr =
        self.veri = '`p!v` or `p!verify`\np!v help\np!v {SRN}\n\n'
        self.count = '`p!c` or `p!count <role [Not mention]>`\n\nReturns the number of people with the specified role\n\n'
        self.ping = '`p!ping` or `p!Ping`\n\n\nReturns the bot\'s latency\n\n'
        # self.news = '`!news [optional]`\n\nPESU Academy Notifications\nUsage:\n`!news`: Gets the latest announcement\n`!news today`: Gets today\'s announcements\n`!news {N}`: Gets the last "N" announcements(where N is a number)\n`!news today {N}`: Gets last "N" announcements made today\n`!news all`: Gets all announcements(max: 10)'
        self.poll = '`p!poll`\n\n\nStarts a poll\n\n'
        self.info = '`p!i` or `p!info <Mention>|<UserID>`\n\nReturns the information about a verified user on this server\n\n'
        self.deverify = '`p!d` or `p!deverify`\n\n\nDeverifies and removes the data of the user from the verified list\n\n'
        self.fil = f'`p!f` or `p!file`\n\nSends the verified.csv file to <#{931523862443724830}>\n\n'
        #self.purge = '`p!p` or `p!purge`\n!p <amount>\n\nPurges the specified number of messages(limit=1000)'
        self.echo = '`p!e` or `p!echo <channel> <Text>`\n\nEchoes a message through the bot to the specified channel\n\n'
        self.mute = '`p!mute <Mention> <Time> <Reason>`\n\nMutes the user for the specified time\n\n'
        self.unmute = '`p!unmute <Mention>`\n\n\nUnmutes the user\n\n'
        self.lock = '`p!lock <channel> <Reason>`\n\nLocks the specified channel\n\n'
        self.unlock = '`p!unlock <channel>`\n\n\nUnlocks the specified channel\n\n'
        self.kick = '`p!kick <Mention> <Reason>`\n\nKicks the member from the server\n\n'
        self.snipeinfo = "`p!snipe`\n\n\nResends the last deleted message on the server\n\n"
	# self.checkPESUAnnouncement.start()
        # self.checkNewDay.start()
        self.snipe = None


    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        self.guildObj = self.client.get_guild(GUILD_ID)
        self.admin = get(self.guildObj.roles, id=1032709443940524228)
        self.mods = get(self.guildObj.roles, id=1032709443940524227)
        self.bot_devs = get(self.guildObj.roles, id=1032709443940524226)
        self.just_joined = get(self.guildObj.roles, id=1032714828197937152)
        self.verified = get(self.guildObj.roles, id=1032714872695304203)
        self.senior = get(self.guildObj.roles, id=1032714925832949820)
        await self.client.get_channel(BOT_LOGS).send("Bot is online")
        await self.client.get_channel(BOT_LOGS).send(f"Logged in as {self.client.user}")
        await self.client.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name="with the PRIDE of PESU"),
        )


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # error handling, in case of an error the error message will be put up in the channel
        string = f"Something's wrong, I can feel it\n{str(error)}"
        await ctx.channel.send("``{}``".format(string))
        await self.client.get_channel(BOT_LOGS).send(f"{string}\n{str(ctx.message.author.mention)} is a noob who made this mistake in {str(ctx.message.channel.mention)}")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.client.get_channel(BOT_LOGS).send(f"**{member.name}** Joined\n=> {str(member.mention)} just joined")
        await member.add_roles(self.just_joined)

    @commands.Cog.listener()
    async def on_member_remove(self, user):
        await self.client.get_channel(BOT_LOGS).send(f"**{str(user)}** just left.")
        await self.client.get_channel(BOT_LOGS).send(f"=> {str(user.mention)} just left :(")
        if(helpers(self.client).getDeverified(str(user.id))):
            await self.client.get_channel(BOT_LOGS).send("Deverified the user")


    #@commands.Cog.listener()
    #async def on_member_update(self, before, after):
    #    if((self.budday not in before.roles) and (self.budday in after.roles)):
    #        await self.client.get_channel(798472825589334036).send(f"Yo, it's {before.mention}'s birthday!")


    @commands.Cog.listener()
    async def on_message(self, message):
        if(message.author.bot):
            pass
        else:
            temp = message.content.replace("`", "|")
            if (f'<@!{BOT_DEVS}>' in str(temp)): # Bot devs
                ping_log = f"{message.author.mention} pinged botdev in {message.channel.mention}"
                ping_embed = discord.Embed(title="Ping", color=0x0000ff)
                ping_embed.add_field(name="Ping report", value=ping_log, inline=False)
                ping_embed.add_field(name="Message content", value=f"https://discord.com/channels/{GUILD_ID}/{message.channel.id}/{message.id}", inline=False)
                await self.client.get_channel(MOD_LOGS).send(embed=ping_embed)
            if (f'<@&{MODS}>' in str(temp)) : #Time keepers
                ping_log = f"{message.author.mention} pinged mods in {message.channel.mention}"
                ping_embed = discord.Embed(title="Ping", color=0x0000ff)
                ping_embed.add_field(name="Ping report", value=ping_log, inline=False)
                ping_embed.add_field(name="Message content", value=f"https://discord.com/channels/{GUILD_ID}/{message.channel.id}/{message.id}", inline=False)
                await self.client.get_channel(MOD_LOGS).send(embed=ping_embed)
            if (f'<@&{ADMIN}>' in str(temp)):
                ping_log = f"{message.author.mention} pinged admin in {message.channel.mention}"
                ping_embed = discord.Embed(title="Ping", color=0x0000ff)
                ping_embed.add_field(name="Ping report", value=ping_log, inline=False)
                ping_embed.add_field(name="Message content", value=f"https://discord.com/channels/{GUILD_ID}/{message.channel.id}/{message.id}", inline=False)
                await self.client.get_channel(MOD_LOGS).send(embed=ping_embed)


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if((reaction.message.author.id == botID) and (not user.bot)):
            try:
                s = reaction.message.embeds[0].footer.text.lower()
                if('poll by' in s):
                    for rr in reaction.message.reactions:
                        if(rr == reaction):
                            pass
                        else:
                            rlist = await rr.users().flatten()
                            if(user in rlist):
                                await rr.remove(user)
            except:
                pass


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if(message.author.bot):
            pass
        else:
            self.snipe = message
            await asyncio.sleep(60)
            self.snipe = None

    @commands.command(aliases=['snipe'])
    async def _snipe(self, ctx):
        if(self.snipe == None):
            await ctx.channel.send("There is nothing to snipe")
        else:
            await ctx.channel.send(f"**{self.snipe.author.mention} on {self.snipe.channel.mention}:** {self.snipe.content}")
            try:
                attachment = self.snipe.attachments
                await attachment[0].save(attachment[0].filename)
                await ctx.channel.send(file=discord.File(attachment[0].filename))
                os.remove(attachment[0].filename)
            except:
                pass
            self.snipe = None


    @commands.command(aliases=['h', 'help'])
    async def _help(self, ctx):
        help_embed = discord.Embed(title="PESU BOT", color=0x48BF91)
        if(self.just_joined in ctx.author.roles):
            help_embed.add_field(name="Verification", value=self.veri)
            await ctx.channel.send(embed=help_embed)
            return
        help_embed.add_field(name="Count", value=self.count)
        help_embed.add_field(name="Ping", value=self.ping)
        help_embed.add_field(name="Poll", value=self.poll)
        help_embed.add_field(name="Snipe", value=self.snipeinfo)
        help_embed.add_field(name="PollShow", value=self.polsho)
        help_embed.add_field(name="Uptime", value=self.uptimeinfo)
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles) or (self.bot_devs in ctx.author.roles)):
            help_embed.add_field(name="User Info", value=self.info)
            help_embed.add_field(name="Deverify", value=self.deverify)
            #help_embed.add_field(name="Purge", value=self.purge)
            help_embed.add_field(name="Echo", value=self.echo)
            if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
                help_embed.add_field(name="Enable Confess", value=self.confessen)
                help_embed.add_field(name="Disable Confess", value=self.confessdis)
                help_embed.add_field(name="Mute", value=self.mute)
                help_embed.add_field(name="Unmute", value=self.unmute)
                help_embed.add_field(name="Lock", value=self.lock)
                help_embed.add_field(name="Unlock", value=self.unlock)
                help_embed.add_field(name="Kick", value=self.kick)
            if((self.admin in ctx.author.roles) or (self.bot_devs in ctx.author.roles)):
                help_embed.add_field(name="Load", value=self.loadit)
                help_embed.add_field(name="Unload", value=self.unloadit)
                help_embed.add_field(name="File", value=self.fil)
                help_embed.add_field(name="Restart", value=self.rest)
                help_embed.add_field(name="Pull", value=self.pull)
                help_embed.add_field(name="Scrape", value=self.scrape)
        await ctx.channel.send(embed=help_embed)


    @cog_ext.cog_slash( name="ping",
                        guild_ids=[GUILD_ID],
                        description="Check for latency"
                      )
    async def _ping(self, ctx):
        ps = f"Pong!!!\nPing = `{str(round(self.client.latency * 1000))} ms`"
        await ctx.reply(ps)


    def getDeverified(self, a=""):
        dat = ""
        ret = False
        file1 = open('cogs/verified.csv', 'r')

        for line in file1:
            if(a not in line.split(',')):
                dat += line
            else:
                ret = True

        file1.close()
        file1 = open('cogs/verified.csv', 'w')
        file1.write(dat)
        file1.close()

        return ret


def setup(client):
    client.add_cog(server(client))
