# 3rd party modules
import discord
from discord.ext import commands
from typing import Union, Optional
from PIL import Image, ImageOps
from io import BytesIO

# Builtin modules
import random
from aiohttp import request


class Images(commands.Cog):
    """Image manupulation commands"""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['down_under', 'down-under', 'downunder'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def australia(self, ctx, member: Optional[discord.Member]=None):
        """Traveling in a fried-out Kombi"""

        if not member:
            member = ctx.author

        pfp = member.avatar_url_as(size=128)
        data = BytesIO(await pfp.read())
        img = Image.open(data)
        img = img.rotate(180)
        img.save('lib/images/project.png')

        await ctx.send(file=discord.File('lib/images/project.png'))

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def rotate(self, ctx, member: Optional[discord.Member]=None, angle: Optional[int]=0):
        """Rotate a profile picture"""

        if not member:
            member = ctx.author

        pfp = member.avatar_url_as(size=128)
        data = BytesIO(await pfp.read())
        img = Image.open(data)
        img = img.rotate(angle)
        img.save('lib/images/project.png')

        await ctx.send(file=discord.File('lib/images/project.png'))

    @commands.command(aliases=['greyscale', 'grey', 'gray'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def grayscale(self, ctx, member: Optional[discord.Member] = None):
        """Black and white images"""

        if not member:
            member = ctx.author

        pfp = member.avatar_url_as(static_format='png', size=128)
        data = BytesIO(await pfp.read())
        img = Image.open(data)
        img = ImageOps.grayscale(img)
        img.save('lib/images/project.png')

        await ctx.send(file=discord.File('lib/images/project.png'))

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ross(self, ctx, member: Optional[discord.Member] = None):
        """Get a load of this guy"""

        if not member:
            member = ctx.author

        bg = Image.open('lib/images/ross.png')

        raw_pfp = member.avatar_url_as(static_format='png', size=128)
        data = BytesIO(await raw_pfp.read())
        pfp = Image.open(data)
        pfp = pfp.resize((69, 69))
        bg.paste(pfp, (4, 70))
        bg.save('lib/images/project.png')
        
        await ctx.send(file=discord.File('lib/images/project.png'), content='Get a load of this guy') # TODO: add message

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def trash(self, ctx, member: Optional[discord.Member] = None):
        """Recycle bin maybe?"""

        if not member:
            member = ctx.author

        bg = Image.open('lib/images/trash.png')

        raw_pfp = member.avatar_url_as(static_format='png', size=128)
        data = BytesIO(await raw_pfp.read())
        pfp = Image.open(data)
        pfp = pfp.resize((200, 200))
        bg.paste(pfp, (117, 127))
        bg.save('lib/images/project.png')

        await ctx.send(file=discord.File('lib/images/project.png'))

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.client.ready:
            self.client.cogs_ready.ready_up('Images')

def setup(client):
    client.add_cog(Images(client))
