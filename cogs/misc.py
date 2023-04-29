from time import time as presentTime
import datetime
import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
from discord_slash import cog_ext, utils
import os
from dotenv import load_dotenv
import subprocess
import sys
import matplotlib.pyplot as plt
import numpy as np
from discord_slash.utils.manage_commands import create_option, create_choice
from datetime import datetime, timedelta
import pytz
from clean import *
import io
IST = pytz.timezone('Asia/Kolkata')

BOT_UID = os.getenv('BOT_UID') # previously botID and pesuID
confessChannel = os.getenv('CONFESS_ID')
GUILD_ID = int(os.getenv('GUILD_ID'))
MOD_LOGS = os.getenv('MOD_LOGS')
TOKEN = os.getenv('DISCORD_TOKEN')
electiveChoiceList = []
ADMIN_ID = os.getenv('ADMIN_ROLE')
MOD_ID = os.getenv('MOD_ROLE')
BOTDEV_ID = os.getenv('BOTDEV_ROLE')
BOTS_ID = os.getenv('BOTS_ROLE')
MUTED_ID = os.getenv('MUTED_ROLE')
VERIFIED_ID = os.getenv('VERIFIED_ROLE')
RR_ID = os.getenv('RR_ROLE')
EC_ID = os.getenv('EC_ROLE')
HN_ID = os.getenv('HN_ROLE')
SENIOR_ID = os.getenv('SENIOR_ROLE')
JUNIOR_ID = os.getenv('JUNIOR_ROLE')
GOD_ID = os.getenv('GOD_ID')

class misc(commands.Cog):

    def __init__(self, client):
        self.client = client
        # self.purge = '`!p` or `!purge`\n!p {amount}\n\nPurges the specified number of messages(limit=1000)'
        self.echo = '`!e` or `!echo`\n!e {Channel mention} {Text}\n\nEchoes a message through the bot to the specified channel'
        self.mute = '`!mute`\n!mute {Member mention} {Time} {Reason: optional}\n\nMutes the user for the specified time\nLimit: 14 days'
        self.unmute = '`!unmute`\n!unmute {Member mention}\n\nUnmutes the user'
        self.lock = '`!lock`\n!lock {Channel mention} {Reason: optional}\n\nLocks the specified channel'
        self.unlock = '`!unlock`\n!unlock {Channel mention}\n\nUnlocks the specified channel'
        self.kick = '`!kick`\n!kick {Member mention} {Reason: optional}\n\nKicks the member from the server'
        self.confessions = {}
        self.mutedict = {}
        self.startTime = int(presentTime())
        self.flush_confessions.start()
        self.load_roles()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        self.load_roles()


    def load_roles(self):
        try:
            self.guildObj = self.client.get_guild(GUILD_ID)
            self.admin = get(self.guildObj.roles, id=ADMIN_ID)
            self.mods = get(self.guildObj.roles, id=MOD_ID)
            self.bot_devs = get(self.guildObj.roles, id=BOTDEV_ID)
            self.bots = get(self.guildObj.roles, id=BOTS_ID)
            self.pesu_bot = get(self.guildObj.roles, id=BOT_UID)
            self.muted = get(self.guildObj.roles, id=MUTED_ID)
        except:
            pass

    @cog_ext.cog_slash( name="uptime",
                        guild_ids=[GUILD_ID],
                        description="Shows how long the bot has been online for"
                      )
    async def _upTime(self, ctx):
        currTime = int(presentTime())
        seconds = (currTime - self.startTime)//1
        await ctx.reply("Bot uptime: `{}`".format(str(timedelta(seconds = seconds))))   

    @cog_ext.cog_slash( name="count",
                        description="Counts the number of users with a specific",
                        guild_ids=[GUILD_ID],
                        options=[
                            create_option(
                                name="rolename",
                                description="The channel to be unlocked",
                                option_type=3,
                                required=False
                            )
                        ]
                      )
    async def _count(self, ctx, rolename = ""):
        rolename = rolename.split('&')
        temp = []
        for i in rolename:
            temp.append(i.strip())
        rolename = temp
        await ctx.reply(f"Got request for role {str(rolename)}")
        if(rolename == ['']):
            await ctx.channel.trigger_typing()
            for guild in self.client.guilds:
                total = len(guild.members)
                verified_role = get(ctx.guild.roles, id=VERIFIED_ID)
                rrRole = get(self.guildObj.roles, id=RR_ID)
                ecRole = get(self.guildObj.roles, id=EC_ID)
                seniorRole = get(self.guildObj.roles, id=SENIOR_ID)
                hnRole = get(self.guildObj.roles, id=HN_ID)
                juniorRole = get(self.guildObj.roles, id=JUNIOR_ID)
                verified = 0
                hooman = 0
                bots = 0
                seniorsNos = 0
                juniorNos = 0
                rrPeeps = 0
                ecPeeps = 0
                hnPeeps = 0
                for mem in guild.members:
                    if(verified_role in mem.roles):
                        verified +=1
                    if(rrRole in mem.roles):
                        rrPeeps += 1
                    if(ecRole in mem.roles):
                        ecPeeps += 1
                    if(hnRole in mem.roles):
                        hnPeeps += 1
                    if(seniorRole in mem.roles):
                        seniorsNos += 1
                    if(juniorRole in mem.roles):
                        juniorsNos += 1
                    perms = ctx.channel.permissions_for(mem)
                    if(perms.view_channel):
                        if(mem.bot):
                            bots += 1
                        else:
                            hooman += 1
            stats = f"""**Server Stats:**
                Total number of people on the server: `{total}`
                Total number of verified people: `{verified}`
                Total number of seniors: `{seniorsNos}`
                Total number of juniors: `{juniorsNos}`
                Total members from RR Campus: `{rrPeeps}`
                Total members from EC Campus: `{ecPeeps}`
                Total members from HN Campus: `{hnPeeps}`
                Number of people that can see this channel: `{hooman}`
                Number of bots that can see this channel: `{bots}`"""
            await ctx.reply(stats)
        else:
            thisRole = []
            for roles in rolename:
                thisRole.append(get(ctx.guild.roles, name=roles))
            for guild in self.client.guilds:
                count = 0
                for member in guild.members:
                    boolean = True
                    # bool will be true only if all the roles passed as args are present
                    for roles in thisRole:
                        if roles not in member.roles:
                            boolean = False
                    if boolean:
                        count += 1
            await ctx.reply(f"{str(count)} people has role {str(thisRole)}")

    #@commands.command(aliases=['p', 'purge'])
    #async def _clear(self, ctx, amt=0):
    #    purge_embed = discord.Embed(
    #        title="Purge", color=0x48BF91, description=self.purge)
    #    if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles) or (self.bot_devs in ctx.author.roles)):
    #        if(amt == 0):
    #            await ctx.channel.send("Lawda tell how much you want to purge", embed=purge_embed)
    #            return
    #        if(amt > 1000):
    #            await ctx.channel.send("Lawda, limit is 1000 okay?", embed=purge_embed)
    #            return
    #        await ctx.channel.purge(limit=amt+1)
    #    else:
    #        await ctx.channel.send(f"{ctx.author.mention} You are not authorised to do that")
    



    #@commands.command(aliases=['e', 'echo'])
    @cog_ext.cog_slash( name="echo",
                        description="Echoes a message through the bot to the specified channel",
                        guild_ids=[GUILD_ID],
                        options=[
                            create_option(
                                name="Channel",
                                description="Channel the message is to be sent to",
                                option_type=7,
                                required=True
                            ),
                            create_option(
                                name="Message",
                                description="Message to be sent",
                                option_type=3,
                                required=True
                            )
                        ]
                      )    
    async def _echo(self, ctx, Channel: discord.TextChannel = None, *, Message: str = ''):
        echo_embed = discord.Embed(
            title="Echo", color=0x48BF91, description=self.echo)
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles) or (self.bot_devs in ctx.author.roles)):
            if(Channel == None):
                await ctx.channel.send(embed=echo_embed)
                return
            attachment = ctx.message.attachments
            if(Channel.id == ctx.channel.id):
                await ctx.message.delete()
            if(len(attachment) != 0):
                await attachment[0].save(attachment[0].filename)
                sent = await Channel.send(file=discord.File(attachment[0].filename))
                os.remove(attachment[0].filename)
                if(message != ''):
                    await sent.edit(content=Message)
            else:
                await Channel.send(content=Message)
        else:
            await ctx.channel.send("Bro you can't do that")
#opt type 6 is user
#opt type 7 is channel

    @cog_ext.cog_slash( name="mute",
                        description="Mutes the user for the specified time",
                        guild_ids=[GUILD_ID],
                        options=[
                            create_option(
                                name="User",
                                description="User to be muted",
                                option_type=6,
                                required=True
                            ),
                            create_option(
                                name="time",
                                description="Duration to be muted for",
                                option_type=3,
                                required=True
                            ),
                            create_option(
                                name="Reason",
                                description="Reason for mute",
                                option_type=3,
                                required=False
                            )
                        ]
                      )
    @ commands.command(aliases=['mute'])
    async def _mute(self, ctx, User: discord.Member = None, time='', *, Reason: str = 'no reason given'):
        mute_help_embed = discord.Embed(
            title="Mute", color=0x48BF91, description=self.mute)

        if(ctx.author.mention == User.mention):
            mod = self.client.get_user(BOT_UID)
        else:
            mod = ctx.author

        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles) or (mod.id == BOT_UID)):
            if(User != None):
                seconds = 0
                if(time.lower().endswith("d")):
                    seconds += int(time[:-1]) * 60 * 60 * 24
                if(time.lower().endswith("h")):
                    seconds += int(time[:-1]) * 60 * 60
                elif(time.lower().endswith("m")):
                    seconds += int(time[:-1]) * 60
                elif(time.lower().endswith("s")):
                    seconds += int(time[:-1])

                if((seconds <= 0) or (seconds > 1209600)):
                    await ctx.channel.reply(f"{ctx.author.mention}, please enter a valid amount of time", embed=mute_help_embed)
                elif((mod.id == BOT_UID) and (seconds < 1800)):
                    await ctx.channel.reply(f"{ctx.author.mention}, self-mute is only for 30 minutes or more")
                else:
                    if(self.muted in User.roles):
                        await ctx.channel.send("Lawda they're already muted means, how much more you'll do, sad fellow")
                    else:
                        if((self.admin in User.roles) or (self.mods in User.roles)):
                            await ctx.channel.send("Lawda, they're an admin/mod. I can't mute them")
                        elif(self.bots in User.roles):
                            await ctx.channel.send("You dare try to mute my own kind")
                        else:
                            await member.add_roles(self.muted)
                            mute_embed = discord.Embed(
                                title="Mute", color=0xff0000)
                            mute_user = f"{User.mention} was muted"
                            mute_embed.add_field(
                                name="Muted user", value=mute_user)
                            await ctx.channel.send(embed=mute_embed)
                            mute_embed_logs = discord.Embed(
                                title="Mute", color=0xff0000)
                            mute_details_logs = f"{User.mention}\t Time: {time}\n Reason: {Reason}\n Moderator: {mod.mention}"
                            mute_embed_logs.add_field(
                                name="Muted user", value=mute_details_logs)
                            await self.client.get_channel(MOD_LOGS).send(embed=mute_embed_logs)
                            muteTime = int(presentTime())
                            if User.id in self.mutedict:
                                self.mutedict[User.id] = muteTime
                            else:
                                self.mutedict[User.id] = muteTime
                            #store the timestamp of mute
                            await asyncio.sleep(seconds)
                            if(self.muted in User.roles):
                                if User.id in self.mutedict:
                                    if self.mutedict[User.id] == muteTime:
                                        #if the time in memory of auto-unmute is same as the time of mute
                                        #then its the correct mute-unmute pair
                                        unmute_embed = discord.Embed(
                                            title="Unmute", color=0x00ff00)
                                        unmute_user = f"{User.mention} welcome back"
                                        unmute_embed.add_field(
                                            name="Unmuted user", value=unmute_user)
                                        await ctx.channel.send(embed=unmute_embed)
                                        unmute_embed_logs = discord.Embed(
                                            title="Unmute", color=0x00ff00)
                                        unmute_details_logs = f"{User.mention}\n Moderator: Auto"
                                        unmute_embed_logs.add_field(
                                            name="Unmuted user", value=unmute_details_logs)
                                        await self.client.get_channel(MOD_LOGS).send(embed=unmute_embed_logs)
                                        await member.remove_roles(self.muted)
                                        self.mutedict.pop(User.id)
                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                if member.id in self.mutedict:
                                    self.mutedict.pop(User.id)
            else:
                await ctx.channel.send(f"{ctx.author.mention}, mention the user, not just the name", embed=mute_help_embed)
        else:
            await ctx.channel.send("Lawda you're not authorised to do that")


    @cog_ext.cog_slash(name="unmute",
                        description="Unmutes the user mentioned",
                        guild_ids=[GUILD_ID],
                        options=[
                            create_option(
                                name="User",
                                description="User to be unmuted",
                                option_type=6,
                                required=True
                            )
                        ]
                      )
    # @ commands.command(aliases=['unmute'])
    async def _unmute(self, ctx, User: discord.Member):
        unmute_help_embed = discord.Embed(
            title="Unmute", color=0x48BF91, description=self.unmute)
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
            try:
                if(self.muted not in User.roles):
                    await ctx.channel.send("Lawda he's not muted only means what I'll do")
                else:
                    unmute_embed = discord.Embed(
                        title="Unmute", color=0x00ff00)
                    unmute_user = f"{member.mention} welcome back"
                    unmute_embed.add_field(
                        name="Unmuted user", value=unmute_user)
                    await ctx.channel.send(embed=unmute_embed)
                    unmute_embed_logs = discord.Embed(
                        title="Unmute", color=0x00ff00)
                    unmute_details_logs = f"{User.mention}\n Moderator: {ctx.author.mention}"
                    unmute_embed_logs.add_field(
                        name="Unmuted user", value=unmute_details_logs)
                    await self.client.get_channel(MOD_LOGS).send(embed=unmute_embed_logs)
                    await member.remove_roles(self.muted)
                    if member.id in self.mutedict:
                        self.mutedict.pop(User.id)
            except:
                await ctx.channel.send(embed=unmute_help_embed)
        else:
            await ctx.channel.send("Lawda you're not authorised to do that")

    # @ commands.command(aliases=['lock'])
    @cog_ext.cog_slash( name="lock",
                        description="Locks the specified channel",
                        guild_ids=[GUILD_ID],
                        options=[
                            create_option(
                                name="Channel",
                                description="The channel to be locked",
                                option_type=7,
                                required=True
                            ),
                            create_option(
                                name="Reason",
                                description="The reason why it is to be locked",
                                option_type=3,
                                required=False
                            )
                        ]
                      )
    async def _lock_channel(self, ctx, *, Channel = None, Reason: str = 'No reason given'):
        lock_help_embed = discord.Embed(
            title="Embed", color=0x48BF91, description=self.lock)

        overwrites = discord.PermissionOverwrite(
            send_messages=False, view_channel=False)
        if(Channel == None):
            Channel = ctx.channel
        if(Channel not in ctx.guild.channels):
            Reason = str(channelobj)
            Channel = ctx.channel

        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
            await Channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            lock_embed = discord.Embed(
                title="Channel Locked :lock:", color=0xff0000, description=reason)
            await Channel.send(embed=lock_embed)
            lock_message = discord.Embed(
                title="", color=0x00ff00, description=f"Locked {Channel.mention}")
            await ctx.reply(embed=lock_message)
            lock_logs = discord.Embed(title="Lock", color=0xff0000)
            lock_logs.add_field(name="Channel", value=Channel.mention)
            lock_logs.add_field(name="Moderator", value=ctx.author.mention)
            await self.client.get_channel(MOD_LOGS).send(embed=lock_logs)
        else:
            await ctx.reply("Lawda, I am not Dyno to let you do this")

    # @ commands.command(aliases=['unlock'])
    @cog_ext.cog_slash( name="unlock",
                        description="Unlocks the specified channel",
                        guild_ids=[GUILD_ID],
                        options=[
                            create_option(
                                name="Channel",
                                description="The channel to be unlocked",
                                option_type=7,
                                required=True
                            )
                        ]
                      )
    async def _unlock_channel(self, ctx, Channel:discord.TextChannel = None):
        unlock_help_embed = discord.Embed(
            title="Unlock", color=0x48BF91, description=self.unlock)
        overwrites = discord.PermissionOverwrite(view_channel=False)

        if(Channel == None):
            Channel = ctx.channel

        perms = Channel.overwrites_for(ctx.guild.default_role)

        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
            if ((perms.view_channel == False) and (perms.send_messages == False)):
                await Channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
                unlock_embed = discord.Embed(
                    title="Channel Unlocked :unlock:", color=0x00ff00)
                await Channel.send(embed=unlock_embed)
                unlock_message = discord.Embed(
                    title="", color=0x00ff00, description=f"Unlocked {Channel.mention}")
                await ctx.channel.send(embed=unlock_message)
                unlock_logs = discord.Embed(title="Unlock", color=0x00ff00)
                unlock_logs.add_field(name="Channel", value=Channel.mention)
                unlock_logs.add_field(
                    name="Moderator", value=ctx.author.mention)
                await self.client.get_channel(MOD_LOGS).reply(embed=unlock_logs)
            else:
                await ctx.reply("Lawda that channel is already unlocked")
        else:
            await ctx.channel.send("Lawda, I am not Dyno to let you do this")

    #@ commands.command(aliases=['contribute', 'support'])
    #async def _support(self, ctx, *params):
    #    Embeds = discord.Embed(title="Contributions", color=0x00ff00)
    #    Embeds.add_field(
    #        name="Github repo", value="https://github.com/AlphaDelta1803/pesu-bot-2025", inline=False)
    #    Embeds.add_field(
    #        name='\u200b', value="If you wish to contribute to the bot, run these steps:", inline=False)
    #    rules = {
    #        0: "Fork the repository with the latest main branch. Don't start working with any deprecated versions",
    #
    #        1: "Make any changes/additions you wish to do",
    #
    #        2: "Start a pull request with the following information furnished in the request message: 'The cog you wish to change | What did you change'",
    #
    #        3: "Wait for approval for reviewers. Your PR may be directly accepted or requested for further changes.",
    #
    #    }
    #    for ruleNo in rules:
    #        Embeds.add_field(name='\u200b', value="`" +
    #                         str(ruleNo) + '`: ' + rules[ruleNo], inline=False)
    #
    #    stark = ctx.guild.get_member(718845827413442692).mention
    #    flabby = ctx.guild.get_member(467341580051939339).mention
    #    e11i0t = ctx.guild.get_member(621283810926919680).mention
    #    sach = ctx.guild.get_member(723377619420184668).mention
    #    alpha = ctx.guild.get_member(523340943437594624).mention
    #    Embeds.add_field(name="Reviewers", value="`ArvindAROO` - {}\n `Flab-E` - {}\n `Mre11i0t` - {} and\n `sach-12` - {}".format(
    #        stark, flabby, e11i0t, sach, alpha), inline=False)
    #    Embeds.add_field(
    #        name="Important", value="**Under no circumstances is anyone allowed to merge to the main branch.**", inline=False)
    #    await ctx.send(embed=Embeds)

    # @commands.command(aliases=['poll'])
    @cog_ext.cog_slash( name="poll",
                        guild_ids=[GUILD_ID],
                        description="Starts a poll",
                        options=[
                            create_option(
                                name="question",
                                description="Question or statement",
                                option_type=3,
                                required=True
                            ),
                            create_option(
                                name="Options",
                                description="[Option 1][Option2][Option3]",
                                option_type=3,
                                required=True
                            )
                        ]
                      )
    async def poll_command(self, ctx, *, question, Options: str = ''):
        msg_1 = Options.split('[')
        poll_list = []
        for i in msg_1:
            j = (i.replace(']', '').replace('[', ''))
            if(j == ''):
                continue
            poll_list.append(j.strip())
        if(len(poll_list) == 0):
            await ctx.reply("Not enough parameters", hidden=True)
        elif(len(poll_list) == 1):
            await ctx.reply("You need more than one choice", hidden=True)
        elif(len(poll_list) > 10):
            await ctx.reply("Can't have more than nine choice", hidden=True)
        else:
            options = poll_list
            reactions_list = [':one:', ':two:', ':three:', ':four:',
                              ':five:', ':six:', ':seven:', ':eight:', ':nine:']
            new_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣',
                        '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
            poll_embed = discord.Embed(title=question, color=0x7289da, timestamp=datetime.now(IST))
            for i in range(len(poll_list)):
                poll_embed.add_field(
                    name="\u200b", value=f"{reactions_list[i]} {options[i]}", inline=False)
            poll_embed.set_footer(text=f"Poll by {ctx.author}")
            required_message = await ctx.reply(embed=poll_embed)
            for i in range(len(poll_list)):
                await required_message.add_reaction(new_list[i])

# Will do later - alfadelta10010
    @commands.command(aliases=['pollshow', 'ps'])
    async def poll_results(self, ctx, msglink: str = ''):
        if(msglink == ''):
            await ctx.channel.send("Message Link is required")
            return
        try:
            msgcomp = msglink.split('/')
            msgid = int(msgcomp[-1].strip())
            msgchannel = int(msgcomp[-2].strip())
            dest = self.client.get_channel(msgchannel)
            msgObj = await dest.fetch_message(msgid)
        except:
            await ctx.channel.send("Poll not found.")
            return
        results = []
        choices = []
        try:
            poll_embed = msgObj.embeds[0]
        except:
            await ctx.channel.send("This ain't a poll bruh")
            return
        for i in poll_embed.fields:
            choices.append(i.value.split(':')[2].strip())
        for i in msgObj.reactions[:len(choices)]:
            results.append(i.count - 1)

        y = np.array(results)
        # pltAlt = plt
        plt.pie(y, labels=choices)
        plt.legend(loc=2)
        plt.savefig('ps.jpg')
        file1 = discord.File('ps.jpg')

        poll_results = discord.Embed(title="Poll Results", color=0x7289da)
        for j in range(len(choices)):
            poll_results.add_field(
                name=choices[j], value=f"{results[j]} votes", inline=False)
        poll_results.set_image(url="attachment://ps.jpg")
        await ctx.channel.send(embed=poll_results, file=file1)
        plt.close()
        os.remove('ps.jpg')

    # @ commands.command(aliases=['kick'])
    @cog_ext.cog_slash( name="kick",
                        description="Kicks the member from the server",
                        options=[
                            create_option(
                                name="Member",
                                description="Member to be kicked or members seperated by \" \"",
                                option_type=3,
                                required=True
                            ),
                            create_option(
                                name="reason",
                                description="The reason for kick",
                                option_type=3,
                                required=True
                            )
                        ]
                      )
    async def _kick(self, ctx, Member, *, reason:str = ""):
        kick_help_embed = discord.Embed(
            title="Kick", color=0x48BF91, description=self.kick)

        if(reason == ""):
            reason = "no reason given"
        mens = [int(i.replace('<', "").replace(">", "").replace("@", "")) for i in Member.split(" ")]

        if(len(mens) == 0):
            await ctx.reply("Mention the user and not just the name", embed=kick_help_embed)
            return
        else:
            member = mens[0]
            member = await self.guildObj.fetch_member(member)

        # a small little Spartan easter egg
        if ((self.bots in member.roles) and (ctx.author.id == 621677829100404746)):
            await ctx.reply("AAAAAAAAAAAAAHHHHHHHHHHHH no no no not again spartan!!! NOOOO")
            return

        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
            if(self.bots in member.roles):
                await ctx.channel.send("You dare to try kick one of my brothers huh")
            elif((self.admin in member.roles) or (self.mods in member.roles)):
                await ctx.channel.send("Gomma you can't kick admins or mods")
            else:
                kick_embed = discord.Embed(
                    title="", color=0xff0000, description=f"{member.mention}** was kicked**")
                await ctx.channel.send(embed=kick_embed)
                kick_logs = discord.Embed(title="Kick", color=0xff0000, timestamp=datetime.utcnow())
                kick_logs.add_field(name="Moderator", value=ctx.author.mention, inline=False)
                kick_logs.add_field(name="Reason", value=reason, inline=False)
                await self.client.get_channel(MOD_LOGS).send(embed=kick_logs)
                try:
                    await member.send(f"You were kicked from the PES'25 Batch Discord Server\n Reason: {reason}")
                except:
                    await ctx.reply("That nonsense fellow hasn't opened his DMs only, I can't do anything about that useless fellow")
                await ctx.guild.kick(member, reason=reason)
        else:
            await ctx.channel.send("Lawda, I am not RoboTop to let you do this")

    @commands.command(aliases=['pull'])
    async def git_pull(self, ctx):
        if ctx.author.id == GOD_ID:
            sys.stdout.flush()
            p = subprocess.Popen(['git', 'pull'], stdout=subprocess.PIPE)
            for line in iter(p.stdout.readline, ''):
                if not line:
                    break
                await ctx.channel.send(str(line.rstrip(), 'utf-8', 'ignore'))
            sys.stdout.flush()
        else:
            await ctx.channel.send("Lawda what are you trying to pull:eyes: :face_with_open_eyes_and_hand_over_mouth:\n You can't execute this command")

    #@commands.command(aliases = ['bash'])
    #async def _script(self, ctx):
    #    if ctx.author.id == 723377619420184668 or ctx.author.id == 718845827413442692 or ctx.author.id == 523340943437594624:
    #        await ctx.channel.send("Enter your command")
    #        message = await self.client.wait_for('message', check=lambda m: m.author.id == ctx.author.id)
    #        code = None
    #        if message.content.startswith('```'):
    #            code = message.content[3:-3]
    #        else:
    #            code = message.content
    #        # all the bash command which can delete or modify file content
    #        if 'rm' in code or 'sudo' in code or '>' in code:
    #            await ctx.channel.send("This might overwrite the file contents, not gonna do")
    #            return
    #        if message.content == 'exit' or code == None:
    #            await ctx.channel.send("Bye!")
    #            return
    #        p = subprocess.Popen(code, stdout=subprocess.PIPE, shell=True)
    #        output = ""
    #        for line in iter(p.stdout.readline, ''):
    #            if not line:
    #                break
    #            out = str(line.rstrip(), 'utf-8', 'ignore')
    #            output += str(line.rstrip(), 'utf-8', 'ignore')
    #            try:
    #                await ctx.channel.send(out)
    #            except:
    #                continue
    #        if (output == ""):
    #            await ctx.channel.send("Empty output")
    #
    #    else:
    #        await ctx.channel.send("Lawda you can't execute this command")

    """
    @commands.command()
    async def scrape(self, ctx, rr:int = 0, ec:int = 0):
        if((self.admin in  ctx.author.roles) or (self.bot_devs in ctx.author.roles)):
            if (rr == 0 or ec == 0):
                await ctx.send("Provide args for range limiter")
                return
            await ctx.send("Beginning scrape job...")
            scrape_job()
            await ctx.send("Getting new csrf token and cookie set...")
            cook, csrf_token = get_meta()
            await ctx.send("Scraping begins...")
            await ctx.send("RR Campus data being retrieved...")
            rr_scrape(rr, cook, csrf_token)
            await ctx.send("Finished RR Campus")
            await ctx.send("EC Campus data being retrieved...")
            ec_scrape(ec, cook, csrf_token)
            await ctx.send("Finished EC Campus")
            await ctx.send("The Most dangerous Scraping is done")
            formatting()
            await ctx.send("Finished formatting")
            brs = br_func()
            await ctx.send("Here is the branch list")
            await ctx.send(brs)
            await ctx.send("Replacing file...")
            last()
            await ctx.send("fin.")
            await ctx.send(ctx.author.mention)
        else:
            await ctx.send("You are not authorised for this command")
    """
    # @commands.command(aliases=['restart'])
    @cog_ext.cog_slash( name="restart",
                        guild_ids=[GUILD_ID],
                        description="Restarts the bot"
                      )
    async def _restart(self, ctx):
        if ((self.admin in ctx.author.roles) or (self.bot_devs in ctx.author.roles)):
            await self.git_pull(ctx)
            await self.client.get_channel(BOT_TEST).send(file=discord.File("cogs/verified.csv"))
            p = subprocess.Popen(['python3', 'start.py'])
            sys.exit(0)
        else:
            await ctx.reply("Cuteeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            await asyncio.sleep(1)
            await ctx.reply("**NO.**")

    @commands.command(aliases=['enableconfess'])
    async def flush_slash(self, ctx):
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles) or (self.bot_devs in ctx.author.roles)):
            await ctx.channel.trigger_typing()
            await utils.manage_commands.add_slash_command(bot_id=botID, bot_token=TOKEN, guild_id=GUILD_ID, cmd_name='confess', description='Submits an anonymous confession', options=[create_option(name="confession", description="Opinion or confession you want to post anonymously", option_type=3, required=True), create_option(name="msg_id", description="Message you want this confession to reply to", option_type=3, required=False)])
            await ctx.channel.send("Done")
            enabled = discord.Embed(title="Announcement from the mods", color=discord.Color.green(
            ), description="The confessions features has been enabled")
            await self.client.get_channel(confessChannel).send(embed=enabled)
            overwrites = discord.PermissionOverwrite(view_channel=False)
            await self.client.get_channel(confessChannel).set_permissions(ctx.guild.default_role, overwrite=overwrites)
        else:
            await ctx.channel.send("You are not authorised for this")

    @commands.command(aliases=['disableconfess'])
    async def disable_confess(self, ctx):
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
            await ctx.channel.trigger_typing()
            resp = await utils.manage_commands.get_all_commands(botID, TOKEN, guild_id=GUILD_ID)
            slash_id = 0
            for comms in resp:
                if(comms['name'] == 'confess'):
                    slash_id = int(comms['id'])
            await utils.manage_commands.remove_slash_command(bot_id=botID, bot_token=TOKEN, guild_id=GUILD_ID, cmd_id=slash_id)
            await ctx.channel.send("Done")
            disabled = discord.Embed(title="Announcement from the mods", color=discord.Color.red(
            ), description="The confessions features has been disabled")
            await self.client.get_channel(confessChannel).send(embed=disabled)
            overwrites = discord.PermissionOverwrite(
                send_messages=False, view_channel=False)
            await self.client.get_channel(confessChannel).set_permissions(ctx.guild.default_role, overwrite=overwrites)
        else:
            await ctx.channel.send("You are not authorised for this")

    @cog_ext.cog_slash(
                        name="nickchange", 
                        description="Change someone else's nickname", 
                        options=[
                                  create_option( 
                                                 name="Member", 
                                                 description="The member whose nickname you desire to change", 
                                                 option_type=6, 
                                                 required=True
                                               ), 
                                  create_option( 
                                                 name="New_Nickname", 
                                                 description="The new name you want to give this fellow", 
                                                 option_type=3, 
                                                 required=True
                                               )
                                ]
                      )
    async def nickchange(self, ctx, Member: discord.Member, New_Nickname: str):
        perms = ctx.channel.permissions_for(ctx.author)
        if((perms.manage_nicknames) and (ctx.author.top_role.position > Member.top_role.position)):
            try:
                await Member.edit(nick=New_Nickname)
                await ctx.send(content=f"Nicely changed {Member.name}'s name", hidden=True)
            except:
                await ctx.send(content="Can't do this one man!", hidden=True)
        else:
            await ctx.send(content=f"Soo cute you trying to change {Member.name}'s nickname", hidden=True)

    @cog_ext.cog_slash(name="pride", description="Flourishes you with the pride of PESU", guild_ids=[GUILD_ID], options=[create_option(name="Message_ID", description="Message ID of any message you wanna reply to with the pride", option_type=3, required=False)])
    async def pride(self, ctx, *, Message_ID: str = ''):
        # await ctx.defer()
        try:
            Message_ID = int(Message_ID)
            msgObj = await ctx.channel.fetch_message(Message_ID)
            await ctx.defer(hidden=True)
            await msgObj.reply(
                "https://tenor.com/view/pes-pesuniversity-pesu-may-the-pride-of-pes-may-the-pride-of-pes-be-with-you-gif-21274060")
        except Exception as e:
            await ctx.defer()
            await ctx.reply(content="https://tenor.com/view/pes-pesuniversity-pesu-may-the-pride-of-pes-may-the-pride-of-pes-be-with-you-gif-21274060")

    @cog_ext.cog_slash(name="confess", description="Submits an anonymous confession", options=[create_option(name="confession", description="Opinion/confession you want to post anonymously", option_type=3, required=True), create_option(name="msg_id", description="Message you want this confession to reply to", option_type=3, required=False)])
    async def confess(self, ctx, *, confession: str, msg_id:str = ''):
        await ctx.defer(hidden=True)
        banFile = open('cogs/ban_list.csv', 'r')
        memberId = str(ctx.author_id)
        banList = []
        for line in banFile:
            banList.append(line.split('\n')[0].replace('\n', ''))
        if(memberId not in banList):
            confessEmbed = discord.Embed(title="Anonymous confession", color=discord.Color.random(
            ), description=confession, timestamp=datetime.now(IST))
            dest = self.client.get_channel(confessChannel)
            await ctx.send(f":white_check_mark: Your confession has been submitted to {dest.mention}", hidden=True)
            try:
                msg_id = int(msg_id)
                msgObj = await dest.fetch_message(msg_id)
                await msgObj.reply(embed=confessEmbed)
            except:
                await dest.send(embed=confessEmbed)
            messages = await dest.history(limit=3).flatten()
            for message in messages:
                if((message.author.id == botID) and (len(message.embeds) > 0)):
                    required_message = message
                    break
            await self.storeId(str(ctx.author_id), str(required_message.id))
        else:
            await ctx.reply(":x: You have been banned from submitting anonymous confessions", hidden=True)

    async def storeId(self, memberId: str, messageId: str):
        confessions = self.confessions
        for key in confessions:
            if(key == memberId):
                confessions[key].append(messageId)
                self.confessions = confessions
                return
            else:
                continue
        confessions[memberId] = [messageId]


# remind me to check if it's actually hidden or nah - alfadelta10010
    # @commands.command(aliases=['confessban', 'cb'])
    @cog_ext.cog_slash(name="confessban", description="Bans a user from submitting confessions who submitted a confession **based on message ID**", guild_ids=[GUILD_ID], options=[create_option(name="Message_ID", description="Message ID of the confession", option_type=3, required=True)])
    async def confess_ban(self, ctx, Message_ID: str):
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
            #await ctx.defer(hidden=True)
            confessions = self.confessions
            msg_id_str = str(Message_ID)
            banFile = open('cogs/ban_list.csv', 'r')
            banList = []
            for line in banFile:
                banList.append(line.split('\n')[0].replace('\n', ''))
            banFile.close()
            banFile = open('cogs/ban_list.csv', 'a')
            for key in confessions:
                msgList = confessions[key]
                if(msg_id_str in msgList):
                    if(key not in banList):
                        banFile.write(f"{key}\n")
                        await ctx.reply("Member banned succesfully", hidden=True)
                        banFile.close()
                        try:
                            dm = await self.client.fetch_user(int(key))
                            dm_embed = discord.Embed(title="Notification", description="You have been banned from submitting confessions", color=discord.Color.red())
                            await dm.send(embed=dm_embed)
                        except:
                            await ctx.reply("DMs were closed", hidden=True)
                        return
                    else:
                        await ctx.reply("This fellow was already banned", hidden=True)
                else:
                    continue
            await ctx.reply("Could not ban", hidden=True)
            banFile.close()
        else:
            await ctx.reply("You are not authorised to do this", hidden=True)

    @cog_ext.cog_slash(name="confessbanuser", description="Bans a user from submitting confessions", guild_ids=[GUILD_ID], options=[create_option(name="Member", description="User/Member to ban", option_type=6, required=True)])
    async def confess_ban_user(self, ctx, Member: discord.Member):
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
            # await ctx.defer(hidden=True)
            user_id = str(Member.id)
            banFile = open('cogs/ban_list.csv', 'r')
            banList = []
            for line in banFile:
                banList.append(line.split('\n')[0].replace('\n', ''))
            banFile.close()
            if(user_id not in banList):
                banFile = open('cogs/ban_list.csv', 'a')
                banFile.write(f"{user_id}\n")
                await ctx.reply("User banned succesfully") #, hidden=True)
                banFile.close()
                try:
                    dm = await self.client.fetch_user(int(user_id))
                    dm_embed = discord.Embed(title="Notification", description="You have been banned from submitting confessions", color=discord.Color.red())
                    await dm.send(embed=dm_embed)
                except:
                    await ctx.reply("DMs were closed, can't do anything with these people") #, hidden=True)
            else:
                await ctx.reply("This user has already been banned, what more do you want") #, hidden=True)
        else:
            await ctx.reply("You are not authorised for this, go man")

    #@commands.command(aliases=['confessunban', 'cub'])
    @cog_ext.cog_slash(name="confessunbanuser", description="Unbans a user from submitting confessions", options=[create_option(name="Member", description="User/Member to unban", option_type=6, required=True)])
    async def confess_unban_user(self, ctx, Member: discord.Member):
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles)):
            # await ctx.defer(hidden=True)
            user_id = str(Member.id)
            dat = ''
            deleted = False
            banFile = open('cogs/ban_list.csv', 'r')
            for line in banFile:
                if(user_id in line.split(',')[0].replace('\n', '')):
                    deleted = True
                    continue
                dat += line
            banFile.close()
            if(deleted):
                banFile = open('cogs/ban_list.csv', 'w')
                banFile.write(dat)
                banFile.close()
                await ctx.send("User has been unbanned successfully") #, hidden=True)
                try:
                    dm = await self.client.fetch_user(int(user_id))
                    dm_embed = discord.Embed(title="Notification", description="You have been unbanned from submitting confessions", color=discord.Color.green())
                    await dm.send(embed=dm_embed)
                except:
                    await ctx.send("DMs were closed, what can I do ;-;") #, hidden=True)
            else:
                await ctx.send("This fellow was never banned in the first place :clown:") #, hidden=True)


    @tasks.loop(hours=24)
    async def flush_confessions(self):
        self.confessions = {}


def setup(client):
    client.add_cog(misc(client))
