# 3rd party modules
import discord
from discord.ext import commands
from typing import Union, Optional
from akinator.async_aki import Akinator

# Builtin modules
import random
from aiohttp import request

class Roleplay(commands.Cog):
    """Roleplay Commands!!!"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dab(self, ctx, member : discord.Member = None):
        """A member of your choice will do an epic dab. 2015 much?"""

        if not member:
            member = ctx.author

        responses = random.choice(['with great force',
                                   'with everlasting power',
                                   'with passion',
                                   'in fear',
                                   'very epicly',
                                   'like ChroniC BlazE'])
        dabs = random.choice(['https://media.giphy.com/media/d4blihcFNkwE3fEI/giphy.gif',
                              'https://media.giphy.com/media/wIyvbQa4g7CajwxkD5/giphy.gif',
                              'https://media.giphy.com/media/l0K4mbH4lKBhAPFU4/giphy.gif',
                              'https://media.giphy.com/media/lae7QSMFxEkkE/giphy.gif'])
        embed = discord.Embed(description=f"*dabs {responses}*",
                              colour=member.colour,
                              timestamp=ctx.message.created_at)
        embed.set_image(url=dabs)
        embed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wink(self, ctx, member: discord.Member=None, *, reason='for no reason.'):
        """<Wink Gif Here>"""

        if not member:
            member =  self.client.user

        api_url = "https://some-random-api.ml/animu/wink"

        await ctx.trigger_typing()

        async with request('GET', api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                img = data["link"]

            else:
                await ctx.send(f"API returned a `{response.status} status.` Try again.")

            embed = discord.Embed(description=f"*{ctx.author.mention} winks at {member.mention} {reason}*",
                                  colour=ctx.author.colour,
                                  timestamp=ctx.message.created_at)
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url)
            embed.set_image(url=img)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pat(self, ctx, member: discord.Member=None, *, reason='for no reason.'):
        """Pat like you would a dog."""

        if not member:
            member = self.client.user

        api_url = "https://some-random-api.ml/animu/pat"

        await ctx.trigger_typing()

        async with request('GET', api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                img = data["link"]

            else:
                await ctx.send(f"API returned a `{response.status} status.` Try again.")

            embed = discord.Embed(description=f"*{ctx.author.mention} pats {member.mention} {reason}*",
                                  colour=ctx.author.colour,
                                  timestamp=ctx.message.created_at)
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url)
            embed.set_image(url=img)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx, member: discord.Member=None, *, reason='for no reason.'):
        """XOXO without the Xs"""

        if not member:
            member = self.client.user

        api_url = "https://some-random-api.ml/animu/hug"

        await ctx.trigger_typing()

        async with request('GET', api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                img = data["link"]

            else:
                await ctx.send(f"API returned a `{response.status} status.` Try again.")

            embed = discord.Embed(description=f"*{ctx.author.mention} hugs {member.mention} {reason}*",
                                  colour=ctx.author.colour,
                                  timestamp=ctx.message.created_at)
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url)
            embed.set_image(url=img)
            await ctx.send(embed=embed)

    @commands.command(aliases=['face_palm', 'facepalms'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def facepalm(self, ctx, *, reason=' '):
        """For those frustrating moments"""

        api_url = "https://some-random-api.ml/animu/face-palm"

        await ctx.trigger_typing()

        async with request('GET', api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                img = data["link"]

            else:
                await ctx.send(f"API returned a `{response.status} status.` Try again.")

            embed = discord.Embed(description=f"{ctx.author.mention} facepalms {reason}",
                                  colour=ctx.author.colour,
                                  timestamp=ctx.message.created_at)
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url)
            embed.set_image(url=img)
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.client.ready:
            self.client.cogs_ready.ready_up('Roleplay')

def setup(client):
    client.add_cog(Roleplay(client))
