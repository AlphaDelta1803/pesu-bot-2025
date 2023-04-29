import discord
from dotenv import load_dotenv
import os
from discord.ext import commands
from asyncio import sleep
from discord.utils import get
from cogs.helpers import helpers
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
BOT_TEST = os.getenv('BOT_TEST')
BOT_LOGS = os.getenv('BOT_LOGS')
GUILD_ID = int(os.getenv('GUILD_ID'))

ADMIN_ID = os.getenv('ADMIN_ROLE')
MOD_ID = os.getenv('MOD_ROLE')
BOTDEV_ID = os.getenv('BOTDEV_ROLE')
UNVERIFIED_ID = os.getenv('UNVERIFIED_ROLE')
VERIFIED_ID = os.getenv('VERIFIED_ROLE')
SENIORS_ID = os.getenv('SENIOR_ROLE')
FIRSTYR_ID = os.getenv('JUNIOR_ROLE')
SECONDYR_ID = os.getenv('SECONDYR_ROLE')
RR_ID = os.getenv('RR_ROLE')
EC_ID = os.getenv('EC_ROLE')
HN_ID = os.getenv('HN_ROLE')


def stream(inp):
    if inp == "ECE":
        return "ECE"
    elif inp == 'CSE':
        return "CSE"
    elif inp == "ME":
        return "Mech"
    elif inp == "EEE":
        return "EEE"
    elif inp == "BT":
        return "Biotech"
    else:
        return "BBA/B.Com"

class verification(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.data_list = [
            'PRN',
            'SRN',
            'Semester',
            'Section',
            'Cycle',
            'Stream/Campus',
            'Stream',
            'Campus',
        ]
        self.user_info = [
            'Member',
            'Member ID',
            'PRN',
            'SRN',
            'Semester',
            'Section',
            'Cycle',
            'Stream/Campus',
            'Stream',
            'Campus',
            'verified',
        ]
        self.info = '`!i` or `!info`\n!i {Member mention}\n!i {Member ID}\n\nReturns the information about a verified user on this server'
        self.deverify = '`!d` or `!deverify`\n!d {Member mention}\n\nDeverifies and removes the data of the user from the verified list'
        self.load_roles()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        self.load_roles()

    def campus(self, inp):
        if "PES University (Ring Road)" in inp:
            return self.rrRole
        if "PES University (Electronic City)" in inp:
            return self.ecRole

    def load_roles(self):
        try:
            self.guildObj = self.client.get_guild(GUILD_ID)
            self.admin = get(self.guildObj.roles, id=ADMIN_ID)
            self.mods = get(self.guildObj.roles, id=MOD_ID)
            self.bot_devs = get(self.guildObj.roles, id=BOTDEV_ID)
            self.just_joined = get(self.guildObj.roles, id=UNVERIFIED_ID)
            self.verified = get(self.guildObj.roles, id=VERIFIED_ID)
            self.senior = get(self.guildObj.roles, id=SENIORS_ID)
            self.firstyr = get(self.guildObj.roles, id=FIRSTYR_ID)
            self.secndyr = get(self.guildObj.roles, id=SECONDYR_ID)
            self.rrRole = get(self.guildObj.roles, id=RR_ID)
            self.ecRole = get(self.guildObj.roles, id=EC_ID)
            self.hnRole = get(self.guildObj.roles, id=HN_ID)
        except:
            pass

    @cog_ext.cog_slash( name="verify",
                        description="Verify your identity to access rest of the server",
                        guild_ids=[GUILD_ID],
                        options=[
                            create_option(
                                name="SRN",
                                description="Enter your SRN. Looks like PES1UG26CS999. (Enter PRN if you don't have)",
                                option_type=3,
                                required=True
                            )
                        ]
                      )
    # @commands.command(aliases=['v', 'V', 'verify', ' verify'])
    async def _verify(self, ctx, SRN=""):
        # embed variables
        success = discord.Embed(title="Sucess", color=0x00FF00)
        fail = discord.Embed(title="Fail", color=0x0FF0000)
        veri = discord.Embed(title="Verification", description="SRN & PRN/Section Verification Process", color=0x0000FF)
        veri.add_field(name="Process", value="1. Enter SRN (PES1UG-/PES2UG-) as argument.\n2. Enter PRN (PES120-/PES220-) or section when prompted by the bot.")
        user = ctx.author

        if(self.verified in user.roles):
            await ctx.channel.send(f"{user.mention}, you've already been verified. Are you tring to steal someone's identity you naughty little...")
            return

        # help for verification
        if(('help' in SRN) or (SRN == "")):
            await ctx.channel.send(embed=veri)
            return

        # checking if the user entered the PRN instead of the SRN
        if (("PES12020" in SRN) or ("PES22020" in SRN) or ("PES12019" in SRN) or ("PES22019" in SRN) or ("PES12021" in SRN) or ("PES22021" in SRN)):
            veri.add_field(name="No SRN found", value="Enter SRN and not PRN as argument")
            await ctx.channel.send(f"{user.mention}", embed=veri)
            return

        # getting credentials from the batch list
        dat = helpers(self.client).getuser(SRN)

        # if the SRN is already in the verified.csv file
        if("Done" in dat):
            await ctx.channel.send(f"{user.mention}, you have already been verified")
            await ctx.channel.send("To avoid spamming we allow only one account per user")
            await ctx.channel.send("If you think someone else has used your SRN, please ping `@alfadelta10010` without fail")
            return

        # if the SRN is not found in the batch list
        if('Error' in dat):
            fail.add_field(name="Invalid SRN", value=f"SRN ({SRN}) not found")
            await ctx.channel.send(f"{user.mention}", embed=fail)
            return
        elif('No match' in dat):
            fail.add_field(name="wrong SRN/PRN", value=f"{SRN} not matching the pattern")
            await ctx.channel.send(f"{user.mention}", embed=fail)
            await ctx.channel.send("`Note: The entered SRN/PRN isn't matching any set of values in our database. Do ping`<@!523340943437594624> `to let him know of the issue`")
            return

        else:
            if('PES12018' in SRN or "PES22018" in SRN):  # Cause '22 batch kids don't have PRN
                await ctx.channel.send(f"{user.mention}, now enter your section to complete verification")
                msg = await self.client.wait_for("message", check=lambda msg: msg.author == ctx.author)
                msg = str(msg.content)
                msg = 'Section ' + msg.upper()
                if(msg != dat[3]):
                    fail.add_field(name="Section validation failed", value=f"{msg} entered does not match the corresponding SRN {SRN}")
                    await ctx.channel.send(f"{user.mention}", embed=fail)
                    await sleep(6)
                    await ctx.channel.purge(limit=4)
                    return
                if dat[2] == 'Sem-7':
                    str_rl = stream(dat[6])
                    camp_rl = campus(dat[7])
                    try:
                        st_role = get(user.guild.roles, name=str_rl)
                        await user.add_roles(self.senior)
                        await user.add_roles(st_role)
                        await user.add_roles(camp_rl)
                    except Exception as e:
                        print(e)
                        await ctx.channel.send(f"{user.mention} Looks like your role isn't on the server yet. DM or tag {self.admin.mention}")
                        return
                elif dat[2] == 'Sem-8':
                    str_rl = stream(dat[6])
                    camp_rl = campus(dat[7])
                    try:
                        st_role = get(user.guild.roles, name=str_rl)
                        await user.add_roles(self.senior)
                        await user.add_roles(st_role)
                        await user.add_roles(camp_rl)
                    except Exception as e:
                        print(e)
                        await ctx.channel.send(f"{user.mention} Looks like your role isn't on the server yet. DM or tag {self.admin.mention}")
                        return
            elif('PES1UG22' in SRN or "PES2UG22" in SRN):  # Cause '26 batch kids don't have SRN
                await ctx.channel.send(f"{user.mention}, now enter your section to complete verification")
                msg = await self.client.wait_for("message", check=lambda msg: msg.author == ctx.author)
                msg = str(msg.content)
                msg = 'Section ' + msg.upper()
                if(msg != dat[3]):
                    fail.add_field(name="Section validation failed", value=f"{msg} entered does not match the corresponding SRN {SRN}")
                    await ctx.channel.send(f"{user.mention}", embed=fail)
                    await sleep(6)
                    await ctx.channel.purge(limit=4)
                    return
                if dat[2] == 'Sem-1':
                    str_rl = stream(dat[6])
                    camp_rl = campus(dat[7])
                    try:
                        st_role = get(user.guild.roles, name=str_rl)
                        await user.add_roles(self.firstyr)
                        await user.add_roles(st_role)
                        await user.add_roles(camp_rl)
                    except Exception as e:
                        print(e)
                        await ctx.channel.send(f"{user.mention} Looks like your role isn't on the server yet. DM or tag {self.admin.mention}")
                        return
                elif dat[2] == 'Sem-2':
                    str_rl = stream(dat[6])
                    camp_rl = campus(dat[7])
                    try:
                        st_role = get(user.guild.roles, name=str_rl)
                        await user.add_roles(self.firstyr)
                        await user.add_roles(st_role)
                        await user.add_roles(camp_rl)
                    except Exception as e:
                        print(e)
                        await ctx.channel.send(f"{user.mention} Looks like your role isn't on the server yet. DM or tag {self.admin.mention}")
                        return
            else:
                await ctx.channel.send(f"{user.mention}, now enter PRN to complete verification")
                msg = await self.client.wait_for("message", check=lambda msg: msg.author == ctx.author)
                if(msg.content != dat[0]):
                    fail.add_field(name="PRN validation failed", value=f"PRN ({msg.content}) entered did not match the corresponding SRN ({SRN})")
                    await ctx.channel.send(f"{user.mention}", embed=fail)
                    await sleep(6)
                    await ctx.channel.purge(limit=4)
                    return
                if(dat[2] == 'Sem-3'):
                    str_rl = stream(dat[6])
                    camp_rl = campus(dat[7])
                    try:
                        st_role = get(user.guild.roles, name=str_rl)
                        await user.add_roles(self.secndyr)
                        await user.add_roles(st_role)
                        await user.add_roles(camp_rl)
                    except Exception as e:
                        print(e)
                        await ctx.channel.send(f"{user.mention} Looks like your role isn't on the server yet. DM <@!523340943437594624>")
                        return
                elif(dat[2] == 'Sem-4'):
                    str_rl = stream(dat[6])
                    camp_rl = campus(dat[7])
                    try:
                        st_role = get(user.guild.roles, name=str_rl)
                        await user.add_roles(self.secndyr)
                        await user.add_roles(st_role)
                        await user.add_roles(camp_rl)
                    except Exception as e:
                        print(e)
                        await ctx.channel.send(f"{user.mention} Looks like your role isn't on the server yet. DM <@!523340943437594624>")
                        return
                if(dat[2] == 'Sem-5'):
                    str_rl = stream(dat[6])
                    camp_rl = campus(dat[7])
                    try:
                        st_role = get(user.guild.roles, name=str_rl)
                        await user.add_roles(self.senior)
                        await user.add_roles(st_role)
                        await user.add_roles(camp_rl)
                    except Exception as e:
                        print(e)
                        await ctx.channel.send(f"{user.mention} Looks like your role isn't on the server yet. DM <@!523340943437594624>")
                        return
                elif(dat[2] == 'Sem-6'):
                    str_rl = stream(dat[6])
                    camp_rl = campus(dat[7])
                    try:
                        st_role = get(user.guild.roles, name=str_rl)
                        await user.add_roles(self.senior)
                        await user.add_roles(st_role)
                        await user.add_roles(camp_rl)
                    except Exception as e:
                        print(e)
                        await ctx.channel.send(f"{user.mention} Looks like your role isn't on the server yet. DM <@!523340943437594624>")
                        return
                
                
                #if(role_str not in [r.name for r in ctx.guild.roles]):
                #    await ctx.channel.send(f"{user.mention} Looks like your role isn't on the server yet. DM <@!523340943437594624>")
                #    return
                #else:
                #    role = get(user.guild.roles, name=role_str)
                #    await user.add_roles(role)

            for i in range(8):
                success.add_field(name="{0}".format(self.data_list[i]), value=dat[i])
            await ctx.channel.send(f"{user.mention}", embed=success)
            await sleep(6)

            # update verified.csv
            with open('cogs/verified.csv', 'a') as file:
                file.write(f"{user.display_name},{user.id}," + ','.join(dat).replace('\n', '') + ',verified\n')
            # add the verified and remove the just joined roles
            await user.add_roles(self.verified)
            await user.remove_roles(self.just_joined)

            await ctx.channel.purge(limit=5)
        await self.client.get_channel(BOT_LOGS).send(f"{user.mention}", embed=success)


    @cog_ext.cog_slash( name="info",
                        description="Returns the information about a verified user on this server",
                        guild_ids=[GUILD_ID],
                        options=[
                            create_option(
                                name="user",
                                description="Mention the user",
                                option_type=6,
                                required=True
                            )
                        ]
                      )
    # @commands.command(aliases=['info', 'i'])
    async def _info(self, ctx, user):
        info_embed = discord.Embed(title="User Info", color=0x48BF91)
        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles) or (self.bot_devs in ctx.author.roles)):
            try:
                #user = await commands.MemberConverter().convert(ctx, member)
                data = helpers(self.client).getVerified(str(user.id))
                if('unverified' in data):
                    await ctx.channel.send(f"{ctx.author.mention} The user has not been verified yet")
                    return
                for i in range(len(self.user_info)):
                    info_embed.add_field(name=self.user_info[i], value=data[i])
                await ctx.channel.send(embed=info_embed)
            except:
                await ctx.channel.send(f"{ctx.author.mention} enter a valid member")
        else:
            await ctx.channel.send("You are not authorised to do that. Where did you find this-")

    @cog_ext.cog_slash( name="deverify",
                        description="Deverifies and removes the data of the user frccom the verified list",
                        guild_ids=[GUILD_ID],
                        options=[
                            create_option(
                                name="user",
                                description="Mention the user",
                                option_type=6,
                                required=True
                            )
                        ]
                      )
    # @commands.command(aliases=['d', 'deverify'])
    async def _deverify(self, ctx, user=""):
        deverify_embed = discord.Embed(title="Deverify", color=0x48BF91, description=self.deverify)

        if(user == ""):
            await ctx.channel.send("Mention a member as argument", embed=deverify_embed)
            return
        #user = ""
        #try:
        #    user = await commands.MemberConverter().convert(ctx, member)
        #except:
        #    await ctx.channel.send("Mention a valid member", embed=deverify_embed)
        #    return

        if((self.admin in ctx.author.roles) or (self.mods in ctx.author.roles) or (self.bot_devs in ctx.author.roles)):
            if(helpers(self.client).getDeverified(str(user.id))):
                for role in user.roles[1:]:
                    await user.remove_roles(role)
                await user.add_roles(self.just_joined)
                await ctx.channel.send(f"De-verified {user.mention}")
            else:
                await ctx.channel.send(f"{ctx.author.mention}, the user has not been verified")
        else:
            await ctx.channel.send("You are not authorised to do that")

    @cog_ext.cog_slash (name="file", description="Sends the file of verified members to <#{}>".format(BOT_TEST), guild_ids=[GUILD_ID])
    # @commands.command(aliases=['f', 'file'])
    async def _file(self, ctx):
        if((self.admin in ctx.author.roles) or (self.bot_devs in ctx.author.roles)):
            await ctx.channel.send("You have the necessary role")
            await self.client.get_channel(BOT_TEST).send(file=discord.File("cogs/verified.csv"))
        else:
            await ctx.channel.send("You are not authorised to do that")


def setup(client):
    client.add_cog(verification(client))
