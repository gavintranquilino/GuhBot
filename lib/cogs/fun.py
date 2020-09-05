# 3rd party modules
import discord
import akinator
from discord.ext import commands
from typing import Union, Optional
from asyncio import get_event_loop
from akinator.async_aki import Akinator

# Builtin modules
import random
from aiohttp import request


class Fun(commands.Cog):
    """What more can I say? They're fun commands."""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['say', 'repeat'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(embed_links=True, manage_messages=True)
    async def echo(self, ctx, *, msg):
        """This command repeats what you say."""

        try:
            await ctx.message.delete()
        except:
            pass
        embed = discord.Embed(description=f"{msg}", colour=ctx.author.colour)
        await ctx.send(embed=embed)

    @commands.command(aliases=['animalfact', 'animal_fact'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def animal(self, ctx, animal: str=None):
        """Dog, Cat, Racoon, Whale, Bird, Panda, Kangaroo, Fox, and Koala facts."""

        animal_list = ('dog', 'cat', 'bird', 'panda', 'fox', 'koala', 'kangaroo', 'racoon', 'whale')

        if not animal:
            animal = random.choice(animal_list)

        if (animal := animal.lower()) in animal_list:
            fact_url = f"https://some-random-api.ml/facts/{animal.lower()}"
            img_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

            await ctx.trigger_typing()

            async with request('GET', img_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    img = data["link"]

                else:
                    img = None

            async with request('GET', fact_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = discord.Embed(title=f"{animal.title()} Fact",
                                          url='https://some-random-api.ml/',
                                          description=f"{data['fact']}",
                                          colour=ctx.author.colour,
                                          timestamp=ctx.message.created_at)
                    embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                                     icon_url=ctx.author.avatar_url)
                    embed.set_image(url=img)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"API returned a `{response.status} status.` Try again.")

        else:
            await ctx.send(f"Sorry {ctx.author.mention}, but I don\'t know any {animal} facts.")

    @commands.command(aliases=['penis', 'howbig', 'peepee', 'pickle', 'schlong', 'glizzy'], hidden=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pp(self, ctx, member: discord.Member=None):
        """Revolutionary peepee measurement system. 100% accuracy"""

        length = random.randint(0, 20)
        size = ''
        inches = 0
        for x in range(length):
            size += '='
            inches += 1
        if not member:
            member = ctx.author
        embed = discord.Embed(title='🌭Glizzy Machine',
                              description='With outstanding accuracy, GuhBot measures your *schlong*',
                              colour=member.colour,
                              timestamp=ctx.message.created_at)
        embed.add_field(name=f"🍆{member}'s penis", value=f"8{size}D")
        embed.add_field(name='📏Size Check', value=f"A whopping {inches} inches!")
        embed.set_thumbnail(url='https://media.giphy.com/media/qLa4BxKoJphYI/giphy.gif')
        embed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pikachu(self, ctx):
        """Random gifs and images of your electric, yellow friend"""

        api_url = "https://some-random-api.ml/img/pikachu"

        await ctx.trigger_typing()

        async with request('GET', api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                img = data["link"]

            else:
                await ctx.send(f"API returned a `{response.status} status.` Try again.")

            embed = discord.Embed(title='Pikachu Pics',
                                  url='https://some-random-api.ml/',
                                  colour=ctx.author.colour,
                                  timestamp=ctx.message.created_at)
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url)
            embed.set_image(url=img)
            await ctx.send(embed=embed)

    @commands.command(aliases=['memes', 'joke', 'jokes', 'funny'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meme(self, ctx):
        """Meme Generator \n( ͡° ͜ʖ ͡°)"""

        api_url = 'https://meme-api.herokuapp.com/gimme'

        await ctx.trigger_typing()

        async with request('GET', api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                source = data['postLink']
                subreddit = data['subreddit']
                caption = data['title']
                meme = data['url']

            else:
                await ctx.send(f"API returned a `{response.status} status.` Try again.")

            embed = discord.Embed(title=caption,
                                  url=source,
                                  description=f"**Subreddit:** [r/{subreddit}](https://www.reddit.com/r/{subreddit}/)",
                                  colour=ctx.author.colour,
                                  timestamp=ctx.message.created_at)
            embed.set_image(url=meme)
            embed.set_footer(text='PS: Click on the meme above to read small text')
            await ctx.send(embed=embed)

    @commands.command(aliases=['chat', 'guhbot', 'reply', 'guhbot,', 'guh,'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def chatbot(self, ctx, *, message: str=None):
        """Have a simple conversation with GuhBot"""

        api_url = f"https://some-random-api.ml/chatbot/?message={message}"

        await ctx.trigger_typing()

        async with request('GET', api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                reply = data['response']

                await ctx.send(reply)

    @commands.command(aliases=['emote'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def emoji(self, ctx, *, emoji: discord.Emoji):
        """Send animated server emojis"""

        if emoji.is_usable:
            try:
                await ctx.message.delete()
            except:
                pass
            await ctx.send(f"<{'a' if emoji.animated else ''}:{emoji.name}:{emoji.id}>")
        else:
            await ctx.send(f"{ctx.author.mention}, I can\'t use that emoji.")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def enlarge(self, ctx, *, emoji: discord.Emoji):
        """Get a gif or image version of a custom emoji"""

        if emoji.is_usable:
            await ctx.send(emoji.url)

    @commands.command(hidden=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def guh(self, ctx):
        """Goo Goo"""

        embed = discord.Embed(title='👶 GAH GAH',
                              colour=ctx.author.colour,
                              timestamp=ctx.message.created_at)
        embed.set_image(url='https://media.giphy.com/media/14kqI3Y4urS3rG/giphy.gif')
        embed.set_footer(text='GuhBoyooo')

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.client.ready:
            self.client.cogs_ready.ready_up('Fun')

def setup(client):
    client.add_cog(Fun(client))
