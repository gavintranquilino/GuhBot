# 3rd party modules
import discord
from discord.ext import commands
from apscheduler.triggers.cron import CronTrigger

# Builtin modules
import platform


class Meta(commands.Cog):

    """About the bot"""

    def __init__(self, client):
        self.client = client
        self._message = 'watching @GuhBot help | {guilds:,} servers & {users:,} users | version {version:s}'

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

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.client.ready:
            self.client.cogs_ready.ready_up('Meta')

def setup(client):
    client.add_cog(Meta(client))
