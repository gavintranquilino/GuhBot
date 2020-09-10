# 3rd party modules
import discord
from discord.ext import commands
from typing import Optional, Union
from apscheduler.triggers.cron import CronTrigger
from psutil import Process, virtual_memory, cpu_percent

# Builtin modules
from os import getcwd
from time import time
from random import choice
from json import load, dump
from platform import python_version
from datetime import datetime, timedelta


class Meta(commands.Cog):

    """About the bot"""

    def __init__(self, client):
        self.client = client
        self._message = 'watching @GuhBot | {guilds:,} servers & {users:,} users | version {version:s}'

        client.scheduler.add_job(self.set, CronTrigger(second=0))

    @property
    def message(self):
        """Status formatter"""

        return self._message.format(guilds=len(self.client.guilds), users=len(set(self.client.get_all_members())), version=self.client.version)

    @message.setter
    def message(self, value):
        """Message setter"""

        if value.split(' ')[0] not in ('playing', 'watching', 'listening-to', 'streaming'):
            raise ValueError('Invalid discord.Activity type.')
        self._message = value

    async def set(self):
        """Set the current bot status"""

        _type, _name = self.message.split(' ', maxsplit=1)
        await self.client.change_presence(activity=discord.Activity(
            name=_name,
            type=getattr(discord.ActivityType, _type, discord.ActivityType.watching),
        ))

    @commands.command(hidden=True)
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def help(self, ctx, *cog):
        """Displays this message"""

        if not cog:
            embed = discord.Embed(title='🔧 Module List',
                                  description=f"Do `{self.client.prefix(self.client, ctx.message)}help [module]` for more info on a specific module.",
                                  colour=ctx.author.colour,
                                  timestamp=ctx.message.created_at)

            cog_list = []
            for x in self.client.cogs:
                if x.lower() == 'errors':
                    pass
                else:
                    cog_list.append((x, self.client.cogs[x].__doc__, False))
            for name, value, inline in cog_list:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            await ctx.send(embed=embed)
        else:
            if len(cog) > 1:
                embed = discord.Embed(title='⛔ Error!',
                                      description='That is way too many cogs!',
                                      colour=self.client.colours['RED'],
                                      timestamp=ctx.message.created_at)
                embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                                 icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(url=self.client.user.avatar_url)
                await ctx.send(embed=embed)
            else:
                found = False
                for x in self.client.cogs:
                    for y in cog:
                        if x.lower() == y.lower():
                            embed = discord.Embed(title=f"🚧 {str(x).title()} Command List",
                                                  description=f"**{str(x).title()} - {self.client.cogs[x].__doc__}**\nDo `{self.client.prefix(self.client, ctx.message)}help [command]` for more info on a command",
                                                  colour=ctx.author.colour,
                                                  timestamp=ctx.message.created_at)

                            command_list = []
                            for c in self.client.get_cog(y.capitalize()).get_commands():
                                if not c.hidden:
                                    if c.signature:
                                        command_list.append((f"`{c.qualified_name} {c.signature}`", f"{c.help}", False))
                                    else:
                                        command_list.append((f"`{c.qualified_name}`", f"{c.help}", False))
                            for name, value, inline in command_list:
                                embed.add_field(name=name, value=value, inline=inline)
                            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                                             icon_url=ctx.author.avatar_url)
                            embed.set_thumbnail(url=self.client.user.avatar_url)
                            found = True
                if not found:
                    for x in self.client.cogs:
                        for c in self.client.get_cog(x).get_commands():
                            if c.name == cog[0].lower():
                                embed = discord.Embed(title='🔧 Command Syntax',
                                                      description='GuhBot\'s commands and how to use them.',
                                                      colour=ctx.author.colour,
                                                      timestamp=ctx.message.created_at)
                                embed.add_field(name=f"{c.name} - {c.help}",
                                                value=f"Proper Syntax:\n`{c.qualified_name} {c.signature}`",
                                                inline=False)
                                if c.aliases == [] or c.aliases == [None]:
                                    c.aliases.clear()
                                    c.aliases.append('No Aliases')
                                embed.add_field(name='Command Aliases',
                                                value=', '.join(c.aliases),
                                                inline=False)
                                embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                                                 icon_url=ctx.author.avatar_url)
                                embed.set_thumbnail(url=self.client.user.avatar_url)
                        found = True
                else:
                    await ctx.message.add_reaction(emoji='👍')
                try:
                    await ctx.send(embed=embed)
                except UnboundLocalError:
                    embed = discord.Embed(title='⛔ Error!',
                                          description=f"How would you even use the command or module \"**{cog[0]}**\"?\nSorry, but I don\'t see a command or module called \"**{cog[0]}**\"",
                                          colour=self.client.colours['RED'],
                                          timestamp=ctx.message.created_at)
                    await ctx.send(embed=embed)

    @commands.command(aliases=['change_prefix'])
    @commands.cooldown(2, 10, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, *, new_prefix: str='guh '):
        """Set a custom prefix for your server"""

        if len(new_prefix) >= 10:
            embed = discord.Embed(title='⛔ Error!',
                                  description=f"Sorry {ctx.author.mention}, but {self.client.user.name} found an error.",
                                  colour=self.client.colours['RED'],
                                  timestamp=ctx.message.created_at)

            embed.add_field(name='Too many characters!', value=f"{ctx.author.mention}, your custom prefix is equal to or has over 10 characters.")
            embed.set_thumbnail(url='https://media.giphy.com/media/8L0Pky6C83SzkzU55a/giphy.gif')
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        else:
            try:
                if new_prefix == 'guh ':
                    self.client.guild_data[str(ctx.message.guild.id)].pop('prefix', None)

                else:
                    self.client.guild_data[str(ctx.message.guild.id)]['prefix'] = new_prefix

            except KeyError:
                self.client.guild_data[str(ctx.message.guild.id)] = {'prefix': new_prefix}

            await ctx.send(f"Set the custom prefix to `{new_prefix}`\nDo `{new_prefix}prefix` to set it back to the default prefix.\nPing {self.client.user.mention} to check the current prefix.")
            with open(self.client.guild_path, 'w') as file:
                dump(self.client.guild_data, file, indent=4)

    @commands.command(aliases=['status', 'statistics', 'info'])
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def stats(self, ctx):
        """Displays GuhBot's statistics"""

        def strfdelta(tdelta, fmt):
            d = {'days': tdelta.days}
            d['hours'], rem = divmod(tdelta.seconds, 3600)
            d['minutes'], d['seconds'] = divmod(rem, 60)
            return fmt.format(**d)

        prefix = self.client.prefix(self.client, ctx.message)
        botUsername = self.client.user.name
        websocketLatency = round(self.client.latency * 1000, 3)
        serverCount = len(self.client.guilds)
        memberCount = len(set(self.client.get_all_members()))
        botVersion = self.client.version
        pythonVer = python_version()
        dpyVer = discord.__version__
        proc = Process()
        with proc.oneshot():
            uptime = timedelta(seconds=time()-proc.create_time())
            cpu_time = timedelta(seconds=(proc.cpu_times()).system + proc.cpu_times().user)
            cpu_usage = f"**{cpu_percent()}%**"
            mem_total = virtual_memory().total / (1024**2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)

        ping_title = choice(['🏓 Pong', '🏓 Ping'])
        content = ''
        content += f"Websocket Latency: **{websocketLatency}ms**\n"
        loading = discord.Embed(description='Loading...', colour=ctx.author.colour)

        start = time()
        message = await ctx.send(embed=loading)
        end = time()

        commandLatency = round((end-start)*1000, 3)
        content += f"Command Latency: **{commandLatency}ms**"

        embed = discord.Embed(title=f"📊 Stats",
                              description=f"List of {botUsername}'s statistics",
                              colour=ctx.author.colour,
                              timestamp=ctx.message.created_at)
        fields = [('🔢 Server Count', f"Working in **{serverCount:,d}** servers.", True),
                  ('👥 Member Count', f"Serving **{memberCount:,d}** members.", True),
                  ('🌐 Version', f"GuhBot Version **{botVersion}**", True),
                  ('💬 Server Prefix', f"This server's prefix is `{prefix}`", True),
                  ('🐍 Python Version', f"{botUsername} runs on **Python {pythonVer}**.", True),
                  ('📜 Discord.py Version',
                   f"{botUsername} runs on **Discord.py {dpyVer}**.", True),
                  (f"{ping_title}", content, True),
                  ('⏰ Uptime', strfdelta(uptime, "{days} day(s)\n{hours} hour(s)\n{minutes} minute(s)\n{seconds} second(s)"), True),
                  ('💾 CPU Time', strfdelta(cpu_time, "{days} day(s)\n{hours} hour(s)\n{minutes} minute(s)\n{seconds} second(s)"), True),
                  ('⚙️ CPU Usage', cpu_usage, True),
                  ('💽 Memory Usage', f"{mem_usage:,.3f} / {mem_total:,.0f} MiB ({mem_of_total:.0f}%)", True),
                  ('🙋 Support Server', f"[Support Server]({self.client.support_url})", True),
                  ('🤖 Bot Invite', f"[{self.client.user.name} Invite]({self.client.invite_url})", True),
                  (f"🔗 {self.client.user.name} Website", f"[{self.client.user.name} Website]({self.client.official_url})", True),
                  ('Command List', '***COMING SOON***', True)]
        
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text=f"GuhBean#8433 | {botUsername}")
        embed.set_author(name=botUsername, icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await message.edit(embed=embed)

    @commands.command(aliases=['latency'])
    @commands.cooldown(2, 5, commands.BucketType.user)
    async def ping(self, ctx):
        """Returns the Discord API / Websocket latency"""

        websocketLatency = round(self.client.latency*1000, 3)
        ping_title = choice(['🏓 Pong', '🏓 Ping'])
        content = ''
        content += f"Websocket Latency: **{websocketLatency}ms**\n"
        loading = discord.Embed(description='Loading...', colour=ctx.author.colour)
        start = time()
        message = await ctx.send(embed=loading)
        end = time()

        commandLatency = round((end-start)*1000, 3)
        content += f"Command Latency: **{commandLatency}ms**"
        embed = discord.Embed(colour=ctx.author.colour,
                              timestamp=ctx.message.created_at)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        embed.add_field(name=choice([ping_title]), value=content)
        await message.edit(embed=embed)

    @commands.command(aliases=['invite'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def support(self, ctx):
        """Returns both support server invite and the bot invite hyperlink"""

        embed = discord.Embed(title='Need Help❓',
                              description='Use the hyperlinks below to get access to the GuhBot support server',
                              colour=ctx.author.colour,
                              timestamp=ctx.message.created_at)
        fields = [('🙋 Support Server', f"[Support Server]({self.client.support_url})", True),
                  ('🤖 Bot Invite', f"[{self.client.user.name} Invite]({self.client.invite_url})", True),
                  (f"🔗 {self.client.user.name} Website", f"[{self.client.user.name} Website]({self.client.official_url})", True)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url='https://media.giphy.com/media/9ZOyRdXL7ZVKg/giphy.gif')
        embed.set_footer(text='GuhBean#8433 | GuhBot')
        await ctx.send(embed=embed)

    @commands.command(aliases=['vote'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def upvote(self, ctx):
        """Support GuhBot? Upvote using this command!"""

        embed = discord.Embed(title='🔺 Upvote GuhBot',
                              description='Provided hyperlinks bring you to GuhBot\'s upvote links.\nUpvoting the bot gets us more users 😀',
                              colour=ctx.author.colour,
                              timestamp=ctx.message.created_at)
        fields = [('Top Discord Bots', '[top.gg](https://top.gg/bot/624754986248831017/vote)', True),
                  ('Discord Bot List', '[discordbotlist.com](https://discordbotlist.com/bots/guhbot/upvote)', True),
                  ('Bots For Discord', '[botsfordiscord.com](https://botsfordiscord.com/bot/624754986248831017/vote)', True),
                  ('Top-Bots', '[top-bots.xyz](https://top-bots.xyz/bot/624754986248831017)', True),
                  ('Discord Boats (rate)', '[discord.boats](https://discord.boats/bot/624754986248831017/rate)', True),
                  ('Discord Boats (vote)', '[discord.boats](https://discord.boats/bot/624754986248831017/vote)', True)]
                  # ('\u200b', '\u200b', True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url='https://media.giphy.com/media/4eQFLKTo1Tymc/giphy.gif')
        embed.set_footer(text='Thanks for upvoting GuhBot!👍')
        await ctx.send(embed=embed)

    # @commands.command()
    # @commands.cooldown(1, 5, commands.BucketType.guild)
    # @commands.has_permissions(administrator=True)
    # async def disable(self, ctx, channel: Optional[discord.TextChannel]):
    #     """Keep GuhBot out of specific channels"""

    #     if not channel:
    #         channel = ctx.channel

    #     embed = discord.Embed(title='❌ Channel Disabled',
    #                           description=f"Disabled {self.client.user.name} commands for {channel.mention}.",
    #                           colour=self.client.colours['RED'],
    #                           timestamp=ctx.message.created_at)
    #     embed.add_field(name='❓ How to re-enable a channel', value=f"If you wish to re-enable a channel so that {self.client.user.name}'s commands will register, do\n`{self.client.prefix(self.client, ctx.message)}enable <channel>`")
    #     embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
    #                      icon_url=ctx.author.avatar_url)

    #     try:
    #         if str(channel.id) in self.client.guild_data[str(ctx.message.guild.id)]['ignored']['channels']:
    #             await ctx.send(f"{ctx.author.mention}, {channel.mention} is already disabled", delete_after=15)

    #         elif str(channel.id) not in self.client.guild_data[str(ctx.message.guild.id)]['ignored']['channels']:
    #             self.client.guild_data[str(ctx.message.guild.id)]['ignored']['channels'].append(str(channel.id))
    #             await channel.send(embed=embed)

    #     except KeyError:
    #         self.client.guild_data[str(ctx.message.guild.id)] = {'ignored': {'channels': [str(channel.id)]}}
    #         await channel.send(embed=embed)

    #     with open(self.client.guild_path, 'w') as file:
    #         dump(self.client.guild_data, file, indent=4)

    # @commands.command()
    # @commands.cooldown(1, 5, commands.BucketType.guild)
    # @commands.has_permissions(administrator=True)
    # async def enable(self, ctx, channel: Optional[discord.TextChannel]):
    #     """Re-activate GuhBot in a specific channel"""

    #     if not channel:
    #         channel = ctx.channel

    #     embed = discord.Embed(title='✅ Channel Enabled',
    #                           description=f"Enabled {self.client.user.name} commands for {channel.mention}.",
    #                           colour=self.client.colours['GREEN'],
    #                           timestamp=ctx.message.created_at)
    #     embed.add_field(name='❓ How to disable a channel', value=f"If you wish to disable a channel so that {self.client.user.name}'s commands won\'t register, do\n`{self.client.prefix(self.client, ctx.message)}disable <channel>`")
    #     embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
    #                      icon_url=ctx.author.avatar_url)

    #     try:
    #         if str(channel.id) in self.client.guild_data[str(ctx.message.guild.id)]['ignored']['channels']:
    #             for chnl in self.client.guild_data[str(ctx.message.guild.id)]['ignored']['channels']:
    #                 if chnl == str(channel.id):
    #                     self.client.guild_data[str(ctx.message.guild.id)]['ignored']['channels'].remove(str(channel.id))
    #                     if not self.client.guild_data[str(ctx.message.guild.id)]['ignored']['channels']:
    #                         self.client.guild_data[str(ctx.message.guild.id)]['ignored'].pop('channels', None)
    #                         if not self.client.guild_data[str(ctx.message.guild.id)]['ignored']:
    #                             self.client.guild_data[str(ctx.message.guild.id)].pop('ignored', None)
    #                     await channel.send(embed=embed)

    #         elif str(channel.id) not in self.client.guild_data[str(ctx.message.guild.id)]['ignored']['channels']:
    #             await ctx.send(f"{ctx.author.mention}, {channel.mention} is already enabled", delete_after=15)
    #             if not self.client.guild_data[str(ctx.message.guild.id)]['ignored']['channels']:
    #                 self.client.guild_data[str(ctx.message.guild.id)].pop('ignored', None)

    #     except KeyError:
    #         await ctx.send(f"{ctx.author.mention}, {channel.mention} is already disabled", delete_after=15)

    #     with open(self.client.guild_path, 'w') as file:
    #         dump(self.client.guild_data, file, indent=4)

    @commands.command(aliases=['close', 'disconnect'], hidden=True)
    @commands.is_owner()
    async def logout(self, ctx):
        """This command disconnects the bot from all services."""

        await ctx.send(f":wave: Goodbye {ctx.author.mention}! I'm shutting dow...")
        await self.client.logout()
        print(f"{self.client.user.name} was logged out.")

    @logout.error
    async def logout_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            rickroll = 'https://media.giphy.com/media/lgcUUCXgC8mEo/giphy.gif'

            embed = discord.Embed(colour=ctx.author.colour,
                                  timestamp=ctx.message.created_at)
            embed.add_field(name='You Silly Billy 😜',
                            value=f"You thought you can actually use the logout command!")
            embed.set_image(url=rickroll)
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            raise error

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog):
        """Cog loader"""

        self.client.load_extension(f"lib.cogs.{cog}")
        await ctx.send(f"`{cog} loaded successfully.`")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog):
        """Cog unloader"""

        self.client.unload_extension(f"lib.cogs.{cog}")
        await ctx.send(f"`{cog} unloaded successfully.`")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog):
        """Cog reloader. Unload then reload"""

        self.client.unload_extension(f"lib.cogs.{cog}")
        self.client.load_extension(f"lib.cogs.{cog}")
        await ctx.send(f"`{cog} reloaded successfully.`")

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.client.ready:
            self.client.cogs_ready.ready_up('Meta')


def setup(client):
    client.add_cog(Meta(client))
