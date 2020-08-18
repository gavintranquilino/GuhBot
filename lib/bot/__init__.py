# 3rd party modules
from asyncio import sleep
from discord import Embed
from discord.ext.commands import Bot as BotBase
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import when_mentioned_or, CooldownMapping, BucketType

# Builtin modules
from glob import glob
from pathlib import Path
from os import getcwd, sep
from json import load, dump
from logging import basicConfig, INFO

# Logging
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")
basicConfig(level=INFO)

# Locate all Cogs
COGS = [path.split(sep)[-1][:-3] for path in glob('./lib/cogs/*.py')]

def get_prefix(client, message):
    with open(getcwd()+'/lib/config/guilds.json', 'r') as file:
        data = load(file)
    if not str(message.guild.id) in data:
        return when_mentioned_or('guh ')(client, message)
    else:
        prefix = data[str(message.guild.id)]['prefix']
        return when_mentioned_or(prefix)(client, message)

def guild_prefix(client, message):
    with open(getcwd()+'/lib/config/guilds.json', 'r') as file:
        data = load(file)
    if not str(message.guild.id) in data:
        return 'guh '
    else:
        prefix = data[str(message.guild.id)]['prefix']
        return str(prefix)

class Ready(object):
    """Cog console logging on startup"""

    def __init__(self):
        print(COGS)
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
        self.prefix = guild_prefix
        self.ready = False
        self.support_url = 'https://discord.gg/PBmfvpU'
        self.cogs_ready = Ready()
        self.scheduler = AsyncIOScheduler()
        self.cooldown = CooldownMapping.from_cooldown(1, 5, BucketType.user)
        self.colours = {'WHITE': 0xFFFFFF,
                        'AQUA': 0x1ABC9C,
                        'YELLOW': 0xFFFF00,
                        'GREEN': 0x2ECC71,
                        'BLUE': 0x3498DB,
                        'PURPLE': 0x9B59B6,
                        'LUMINOUS_VIVID_PINK': 0xE91E63,
                        'GOLD': 0xF1C40F,
                        'ORANGE': 0xE67E22,
                        'RED': 0xE74C3C,
                        'NAVY': 0x34495E,
                        'DARK_AQUA': 0x11806A,
                        'DARK_GREEN': 0x1F8B4C,
                        'DARK_BLUE': 0x206694,
                        'DARK_PURPLE': 0x71368A,
                        'DARK_VIVID_PINK': 0xAD1457,
                        'DARK_GOLD': 0xC27C0E,
                        'DARK_ORANGE': 0xA84300,
                        'DARK_RED': 0x992D22,
                        'DARK_NAVY': 0x2C3E50}
        self.colour_list = [c for c in self.colours.values()]

        super().__init__(command_prefix=get_prefix,
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

        print(f"Running your bot on version {self.version}...")
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

        path = getcwd()+'/lib/config/users.json'
        with open(path, 'r') as file:
            data = load(file)

        if message.author.bot:
            pass

        elif message.content.startswith(f"<@!{self.user.id}>") and \
            len(message.content) == len(f"<@!{self.user.id}>"
        ):

            bucket = self.cooldown.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            if retry_after:
                await message.channel.send(f"Slow Down {message.author.mention}! Please wait {round(retry_after, 3)} seconds.")
            else:
                await message.channel.send(f"Hey {message.author.mention}! My prefix here is `{self.prefix(self, message)}`\nDo `{self.prefix(self, message)}help` to get started.", delete_after=10)

        if str(message.author.id) in data and data[str(message.author.id)]['afk']['status']:
            embed = Embed(title='🟢 Cleared AFK Status',
                          description=f"You have **automatically** been marked as **no longer AFK**, you had **{data[str(message.author.id)]['afk']['mentions']} mention(s)** while you were **AFK** for: **{data[str(message.author.id)]['afk']['reason']}**",
                          colour=self.colours['GREEN'],
                          timestamp=message.created_at)
            embed.set_author(name=f"{message.author.name}#{message.author.discriminator}",
                             icon_url=message.author.avatar_url)

            await message.channel.send(embed=embed)
            data[str(message.author.id)]['afk'] = {'status': False, 'mentions': 0, 'reason': 'No Reason', 'display_name': str(message.author.display_name)}
            with open(path, 'w') as file:
                dump(data, file, indent=4)

        if message.mentions:
            for user in message.mentions:
                if not str(user.id) in data:
                    pass
                else:
                    if data[str(user.id)]['afk']['status']:
                        data[str(user.id)]['afk']['mentions'] += 1
                        embed = Embed(name='🔴 AFK',
                                      description=f"{user.mention} is currently set as **AFK** for: **{data[str(user.id)]['afk']['reason']}**",
                                      colour=self.colours['RED'],
                                      timestamp=message.created_at)
                        embed.set_author(name=f"{user.name}#{user.discriminator}",
                                         icon_url=user.avatar_url)
                        await message.channel.send(embed=embed)
                        with open(path, 'w') as file:
                            dump(data, file, indent=4)

                    else:
                        pass

        await self.process_commands(message)

    async def on_guild_remove(self, guild):
        print(f"Removed from server {guild.name}: {guild.id}")

        # --When you need to delete json prefixes for servers you aren't in--
        # from json import dump
        # with open(getcwd()+'/lib/config/prefixes.json', 'r') as file:
        #     data = load(file)
        #
        # data.pop(str(guild.id))
        #
        # with open(getcwd()+'/lib/config/prefixes.json', 'w') as file:
        #     dump(data, file, indent=4)

client = Bot()
