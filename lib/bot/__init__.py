# 3rd party modules
from discord import Embed
from aiosqlite import connect
from discord.ext.commands import Bot
from asyncio import sleep, get_event_loop
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

# DB files
DB_PATH = "./data/db/database.db"
BUILD_PATH = "./data/db/build.sql"

async def get_prefix(client, message):
    cur = await client.db.cursor()
    await cur.execute('SELECT prefix FROM prefixes WHERE id = ?', (message.guild.id,))
    prefix = await cur.fetchone()
    await cur.close()
    if not prefix: 
        return when_mentioned_or('guh ')(client, message)
    else:
        return when_mentioned_or(prefix[0])(client, message)

async def guild_prefix(message):
    cur = await client.db.cursor()
    await cur.execute('SELECT prefix FROM prefixes WHERE id = ?', (message.guild.id,))
    prefix = await cur.fetchone()
    await cur.close()
    if not prefix:
        return 'guh '
    else:
        return prefix[0]

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

client = Bot(command_prefix=get_prefix, case_insensitive=True, help_command=None)

client.prefix = guild_prefix
client.ready = False
client.cogs_ready = Ready()
client.support_url = 'https://discord.gg/PBmfvpU'
client.official_url = 'https://guhbean.github.io/guhbot'
client.invite_url = 'https://discord.com/api/oauth2/authorize?client_id=624754986248831017&permissions=536210679&scope=bot'
client.scheduler = AsyncIOScheduler()
client.cooldown = CooldownMapping.from_cooldown(1, 5, BucketType.user)
client.colours = {'WHITE': 0xFFFFFF,
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
client.colour_list = [c for c in client.colours.values()]

def setup():
    """Initial Cog loader"""

    for cog in COGS:
        client.load_extension(f"lib.cogs.{cog}")
        print(f"Initial setup for {cog}.py")

    print('Cog setup complete')

def launch(version):
    """Run the bot using the API token"""

    client.version = version
    print('Running setup...')
    setup()
    with open('./lib/bot/token.0', 'r', encoding='utf-8') as tf:
        client.TOKEN = tf.read()

    print(f"Running your bot on version {client.version}...")

    client.run(client.TOKEN, reconnect=True)

@client.event
async def on_ready():

    client.scheduler.start()

    # status_channel = client.get_channel(735332260559061042)
    # await status_channel.send(':wave: Hello everyone! I\'m back online!')

    while not client.cogs_ready.all_ready():
        await sleep(0.5)
    print(f"Your bot is online and ready to go!")
    client.ready = True
    client.scheduler.start()

    meta = client.get_cog('Meta')
    await meta.set()

async def connect_db():

    client.db = await connect(DB_PATH)


get_event_loop().run_until_complete(connect_db())

@client.event
async def on_message(message):

    if not message.author.bot and message.guild:
        cur0 = await client.db.cursor() 
        await cur0.execute('SELECT * FROM afk WHERE id = ?', (message.author.id,)) # Select row with author id
        author_afk = await cur0.fetchone()
        
        if author_afk: # Check if row exists
            await cur0.execute('DELETE FROM afk WHERE id = ?', (message.author.id,)) # Delete row

            embed = Embed(title='🟢 Cleared AFK Status',
            description=f"You have **automatically** been marked as **no longer AFK**, you had **{author_afk[1]} mention(s)** while you were **AFK** for: **{author_afk[2]}**",
            colour=client.colours['GREEN'],
            timestamp=message.created_at)
            embed.set_author(name=f"{message.author.name}#{message.author.discriminator}",
                                icon_url=message.author.avatar_url)
        
            await message.channel.send(embed=embed, delete_after=15)

        await cur0.close()
        await client.db.commit()
            
        if message.mentions: # If the message has any mentions
            for user in message.mentions: # Get all users from mention list
                if not user.bot: 
                    cur1 = await client.db.cursor()
                    await cur1.execute('SELECT * FROM afk WHERE id = ?', (user.id,)) # Select row with user id
                    user_afk = await cur1.fetchone()
                    if user_afk:
                        new_counter = int(user_afk[1]) + 1
                        await cur1.execute('UPDATE afk SET mentions = ? WHERE id = ?', (new_counter, user.id)) # Add to mention counter

                        embed = Embed(name='🔴 AFK',
                                        description=f"{user.mention} is currently set as **AFK** for: **{user_afk[2]}**",
                                        colour=client.colours['RED'],
                                        timestamp=message.created_at)
                        embed.set_author(name=f"{user.name}#{user.discriminator}",
                                            icon_url=user.avatar_url)
                        await message.channel.send(embed=embed, delete_after=15) 

                        await cur1.close()
                        await client.db.commit()

        if message.content.startswith(f"<@!{client.user.id}>") and \
            len(message.content) == len(f"<@!{client.user.id}>"
        ):

            bucket = client.cooldown.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            if retry_after:
                await message.channel.send(f"Slow Down {message.author.mention}! Please wait {round(retry_after, 3)} seconds.")
            else:
                await message.channel.send(f"Hey {message.author.mention}! My prefix here is `{await client.prefix(message)}`\nDo `{await client.prefix(message)}help` to get started.", delete_after=10)

        await client.process_commands(message)

@client.event
async def on_guild_remove(self, guild):
    print(f"Removed from server {guild.name}: {guild.id}")

    cur = await self.db.cursor()
    await cur.execute('SELECT prefix FROM prefixes WHERE id = ?', (guild.id,))
    prefix = await cur.fetchone()

    if prefix:
        await cur.execute('DELETE FROM prefixes WHERE id = ?', (guild.id,))

    await self.db.commit()
