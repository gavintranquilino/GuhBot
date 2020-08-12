# 3rd party modules
from asyncio import sleep
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import when_mentioned_or
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Builtin modules
import os
import logging
from glob import glob
from pathlib import Path


# Logging
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")
logging.basicConfig(level=logging.INFO)

# Locate all Cogs
COGS = [path.split('\\')[-1][:-3] for path in glob('./lib/cogs/*.py')]

class Ready(object):
    """Cog console logging on startup"""

    def __init__(self):
        for cog in COGS:
            # commands.cog = False, fun.cog = False
            setattr(self, cog, False)

    def ready_up(self, cog):
        """Singular Cog ready"""

        setattr(self, cog, True)
        print(f"{cog} cog ready")

    def all_ready(self):
        """All Cogs ready"""

        return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    """Bot subclass"""

    def __init__(self):
        self.prefix = 'bruh '
        self.ready = False
        self.cogs_ready = Ready()
        self.scheduler = AsyncIOScheduler()

        super().__init__(command_prefix=self.prefix,
                         case_insensitive=True,
                         help_command=None)

    def setup(self):
        """Initial Cog loader"""

        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"Initial setup for {cog}.py")

        print('Cog setup complete')

    def run(self, version):
        """Run the bot using the API token"""

        self.version = version
        print('Running setup...')
        self.setup()
        with open('./lib/bot/token.0', 'r', encoding='utf-8') as tf:
            self.TOKEN = tf.read()

        print(f"Running your bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_ready(self):
        self.scheduler.start()

        if not self.ready:
            while not self.cogs_ready.all_ready():
                await sleep(0.5)
            print(f"Your bot is online and ready to go!")
            self.ready = True
            self.scheduler.start()

            meta = self.get_cog('Meta')
            await meta.set()

        else:
            print(f"Reconnecting...")

    async def on_connect(self):
        print('Connected')

    async def on_disconnect(self):
        print('Disconnected')

    async def on_message(self, message):
        if message.author.bot:
            pass

        # Mentionable prefix
        elif message.content.startswith(f"<@!{self.user.id}>") and \
            len(message.content) == len(f"<@!{self.user.id}>"
        ):
            await message.channel.send(f"Hey {message.author.mention}! My prefix here is `{self.prefix}`", delete_after=10)

        await self.process_commands(message)

client = Bot()
