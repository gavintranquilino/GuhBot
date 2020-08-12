# 3rd party modules
from discord.ext.commands import when_mentioned_or
from discord.ext.commands import Bot as BotBase

# Builtin modules
import logging
import os
from pathlib import Path
from glob import glob

# Local modules


# Logging
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")
logging.basicConfig(level=logging.INFO)

class Bot(BotBase):
    def __init__(self):
        self.prefix = 'guh '
        self.ready = False

        super().__init__(command_prefix=self.prefix,
                         case_insensitive=True)

    def run(self, version):
        self.version = version

        with open('./lib/bot/token.0', 'r', encoding='utf-8') as tf:
            self.TOKEN = tf.read()

        print(f"Running your bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_ready(self):

        if not self.ready:

            print(f"Your bot is online and ready to go!")
            self.ready = True

        else:
            print(f"Reconnecting...")

    async def on_connect(self):
        print(f"Connected")

    async def on_disconnect(self):
        print(f"Disconnected")

    async def on_message(self, message):
        if message.content.startswith(f"<@!{self.user.id}>") and \
            len(message.content) == len(f"<@!{self.user.id}>"
        ):

            await message.channel.send(f"My prefix here is `{self.prefix}`", delete_after=10)

        await self.process_commands(message)

client = Bot()
