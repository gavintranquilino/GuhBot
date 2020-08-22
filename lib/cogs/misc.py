# 3rd party modules
import discord
from asyncio import sleep
from discord.ext import commands

# Builtin modules
from os import getcwd
from json import load, dump
from aiohttp import request


class Misc(commands.Cog):
    """Miscellaneous Commands"""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['corona', 'coronavirus', 'covid19', 'covid-19'])
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def covid(self, ctx, *, country: str = None):
        """COVID-19 summary and stats"""

        api_url = 'https://api.covid19api.com/summary'

        await ctx.trigger_typing()

        async with request('GET', api_url, headers={}) as response:

            if not country:
                country = 'Global'
                if response.status == 200:
                    data = await response.json()
                    newConfirmed = f"{data[country]['NewConfirmed']:,d}"
                    totalConfirmed = f"{data[country]['TotalConfirmed']:,d}"
                    newDeaths = f"{data[country]['NewDeaths']:,d}"
                    totalDeaths = f"{data[country]['TotalDeaths']:,d}"
                    newRecovered = f"{data[country]['NewRecovered']:,d}"
                    totalRecovered = f"{data[country]['TotalRecovered']:,d}"

                else:
                    await ctx.send(f"API returned a `{response.status} status.` Try again.")

            else:
                country = country.title()
                if response.status == 200:
                    data = await response.json()
                    for element in data['Countries']:
                        if element['Country'] == country:
                            newConfirmed = f"{element['NewConfirmed']:,d}"
                            totalConfirmed = f"{element['TotalConfirmed']:,d}"
                            newDeaths = f"{element['NewDeaths']:,d}"
                            totalDeaths = f"{element['TotalDeaths']:,d}"
                            newRecovered = f"{element['NewRecovered']:,d}"
                            totalRecovered = f"{element['TotalRecovered']:,d}"

                else:
                    await ctx.send(f"API returned a `{response.status} status.` Try again.")

            embed = discord.Embed(title=f"{country} COVID-19 Stats",
                                  url='https://covid19api.com/',
                                  description='Get current [COVID-19 statistics](https://covid19api.com/). Data updated multiple times a day.',
                                  colour=ctx.author.colour,
                                  timestamp=ctx.message.created_at)
            try:
                fields = [('New Confirmed Cases', newConfirmed, True),
                          ('Total Confirmed Cases', totalConfirmed, True),
                          ('New Deaths', newDeaths, False),
                          ('Total Deaths', totalDeaths, True),
                          ('New Recoveries', newRecovered, True),
                          ('Total Recoveries', totalRecovered, False),
                          ('Help Stop COVID-19', '[Advice to the Public](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public)', True)]
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)
                embed.set_thumbnail(
                    url='https://cdn.discordapp.com/attachments/239446877953720321/691020838379716698/unknown.png')
                embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                                 icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            except UnboundLocalError:
                await ctx.send(f"Sorry {ctx.author.mention}, I couldn\'t find COVID-19 stats for `{country}`")

    @commands.command(aliases=['server_stats'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def server_info(self, ctx):
        """Get information on the current server"""

        try:
            bans = ('🔨 Banned Members', len(await ctx.guild.bans()), True)
        except:
            bans = ('\u200b', '\u200b', True)

        embed = discord.Embed(title='Server Information',
                              colour=ctx.guild.owner.colour,
                              timestamp=ctx.message.created_at)

        embed.set_thumbnail(url=ctx.guild.icon_url)

        statuses = [len(list(filter(lambda m: str(m.status) == 'online', ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == 'idle', ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == 'dnd', ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == 'offline', ctx.guild.members)))]

        fields = [('📛 Name', ctx.guild.name, True),
                  ('💳 ID', ctx.guild.id, True),
                  ('👑 Owner', ctx.guild.owner, True),
                  ('🌎 Region', ctx.guild.region, True),
                  ('🕑 Created At', ctx.guild.created_at.strftime('%d/%m/%Y %H:%M:%S'), True),
                  ('👥 Members', len(ctx.guild.members), True),
                  ('👤 Humans', len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                  ('🤖 Bots', len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
                  ('💭 Statuses',
                   f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
                  ('📜 Text channels', len(ctx.guild.text_channels), True),
                  ('🔊 Voice channels', len(ctx.guild.voice_channels), True),
                  ('🌀 Categories', len(ctx.guild.categories), True),
                  ('🏁 Roles', len(ctx.guild.roles), True),
                  bans]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command(aliases=['av', 'pfp', 'profile', 'profile_pic', 'profile_picture'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, member: discord.Member = None):
        """Returns the user's profile picture and ID"""

        if not member:
            member = ctx.author

        embed = discord.Embed(colour=member.colour, timestamp=ctx.message.created_at)
        embed.add_field(name=f"{member.name}#{member.discriminator}", value=f"User ID: {member.id}")
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['user_info', 'who_is'])
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def whois(self, ctx, member: discord.Member = None):
        """Get info on a specific user"""

        if not member:
            member = ctx.author

        roles = [role for role in member.roles]
        lenroles = len(roles)
        if lenroles == 1:
            mentions = f"@everyone"
            top_role = '@everyone'
            lenroles = lenroles
        else:
            mentions = " ".join([r.mention for r in member.roles if r != ctx.guild.default_role])
            top_role = member.top_role.mention
            lenroles = lenroles - 1
        if member == ctx.guild.owner:
            acknowledgements = 'Server Owner'
        elif member == self.client.user:
            acknowledgements = 'Hey that\'s me!'
        elif member.bot:
            acknowledgements = 'Discord Bot'
        elif member.guild_permissions.administrator:
            acknowledgements = 'Server Admin'
        else:
            acknowledgements = None

        embed = discord.Embed(description=f"{member.mention}\nID:{member.id}",
                              colour=member.colour,
                              timestamp=ctx.message.created_at)
        fields = [('Nickname', member.display_name, True),
                  ('Status', member.status, True),
                  ('Joined', member.joined_at.strftime('%a, %b %d, %Y, %I:%M %p'), False),
                  ('Registered', member.created_at.strftime('%a, %b %d, %Y, %I:%M %p'), True),
                  (f"Roles [{lenroles}]", mentions, False),
                  ('Highest Role', top_role, True)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        if acknowledgements:
            embed.add_field(name='Acknowledgements', value=acknowledgements)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['afkon', 'afk_on'])
    @commands.cooldown(2, 5, commands.BucketType.member)
    async def afk(self, ctx, *, reason: str='No reason'):
        """Set your account to an AFK status"""

        author_id = str(ctx.author.id)
        path = getcwd()+'/lib/config/users.json'
        with open(path, 'r') as file:
            data = load(file)

        if len(reason) >= 150:
            embed = discord.Embed(title='⛔ Error!',
                                  description=f"Sorry {ctx.author.mention}, but {self.client.user.name} found an error.",
                                  colour=self.client.colours['RED'],
                                  timestamp=ctx.message.created_at)

            embed.add_field(name='Too many characters!', value=f"{ctx.author.mention}, your AFK status is equal to or has over 50 characters.")
            embed.set_thumbnail(url='https://media.giphy.com/media/8L0Pky6C83SzkzU55a/giphy.gif')
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url)

        elif author_id not in data or not data[author_id]['afk']['status']:
            embed = discord.Embed(title=f"🟡 Now AFK",
                                  description=f"{ctx.author.mention} is now **AFK** for: **{reason}**",
                                  colour=self.client.colours['YELLOW'],
                                  timestamp=ctx.message.created_at)
            embed.add_field(name='❓ How to remove an AFK status', value=f"If you wish to **remove** your **AFK status**, say something in one of the channels that {self.client.user.name} can see.\n\nYou can **clear** your **AFK status** in any server that {self.client.user.name} is in.")
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url)

            data[author_id] = {'afk': {'status': True, 'mentions': 0, 'reason': reason}}
            with open(path, 'w') as file:
                dump(data, file, indent=4)

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.client.ready:
            self.client.cogs_ready.ready_up('Misc')


def setup(client):
    client.add_cog(Misc(client))
