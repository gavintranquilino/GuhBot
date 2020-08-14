# 3rd party modules
import discord
from discord.ext import commands

# Builtin modules
import random
from aiohttp import request


class Fun(commands.Cog):
    """What more can I say? They're fun commands."""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['say', 'repeat'])
    @commands.has_permissions(mention_everyone=True, embed_links=True,
                              manage_messages=True, attach_files=True)
    async def echo(self, ctx, *, msg):
        """This command repeats what you say."""

        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command(aliases=['decision'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def decide(self, ctx, *, question):
        """Answers your questions with a yes or a no"""

        responses = random.choice(['Yes', 'No'])
        embed = discord.Embed(title='🍀 Decision Maker',
                              description=f"{self.client.user.name} will make a yes or no decision for you.",
                              colour=ctx.author.colour,
                              timestamp=ctx.message.created_at)
        fields = [('From:', ctx.author.mention, True),
                  ('Question:', f"{question}", True),
                  ('Answer:', f"`{responses}`", True)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['heads', 'tails', 'coin', 'cf'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def coinflip(self, ctx):
        """Coinflip simulation. Heads or Tails"""

        responses = random.choice(['Heads', 'Tails'])
        embed = discord.Embed(title='🤑 Coin Flip Simulator',
                              description=f"{self.client.user.name} will flip a digital coin for you",
                              colour=ctx.author.colour,
                              timestamp=ctx.message.created_at)
        embed.add_field(name='From:', value=ctx.author.mention)
        embed.add_field(name='Result:', value=f"The coin landed on `{responses}`")
        embed.set_thumbnail(url='https://media.giphy.com/media/6jqfXikz9yzhS/giphy.gif')
        await ctx.send(embed=embed)

    @commands.command(aliases=['animalfact', 'animal_fact'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def animal(self, ctx, animal: str):
        """Random animal facts! Choose from a Dog, Cat, Racoon, Whale, Bird, Panda, Kangaroo, Fox, and Koala facts."""

        if (animal := animal.lower()) in ('dog', 'cat', 'bird', 'panda', 'fox', 'koala', 'kangaroo', 'racoon', 'whale'):
            fact_url = f"https://some-random-api.ml/facts/{animal.lower()}"
            img_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

            await ctx.send(f"🔎 **Searching for {animal} online...**")
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
                    await ctx.send(f"API returned a {response.status} status.")

        else:
            await ctx.send(f"Sorry {ctx.author.mention}, but I don\'t know any {animal} facts.")

    @commands.command(aliases=['dice', 'dice_roll'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def roll(self, ctx, dice='d6'):
        """Roll different types of dice from D4 to D20."""

        found = True
        if dice.upper() == 'D4':
            number = random.randint(1, 4)
            url = 'https://media.giphy.com/media/fiqcUhBNj6jWgJnRlu/giphy.gif'

        elif dice.upper() == 'D6':
            number = random.randint(1, 6)
            url = 'https://media.giphy.com/media/1inmH7UuBPbUGWteWb/giphy.gif'

        elif dice.upper() == 'D8':
            number = random.randint(1, 8)
            url = 'https://media.giphy.com/media/TJla6Pfq8AXHFfeDf0/giphy.gif'

        elif dice.upper() == 'D10':
            number = random.randint(1, 10)
            url = 'https://media.giphy.com/media/dZAD46L9Ph3zHcjXZA/giphy.gif'

        elif dice.upper() == 'D00':
            number = f"{random.randint(0, 100)}%"
            url = 'https://media.giphy.com/media/dZAD46L9Ph3zHcjXZA/giphy.gif'

        elif dice.upper() == 'D12':
            number = random.randint(1, 12)
            url = 'https://media.giphy.com/media/j5Eo80qWJO79MbDUxr/giphy.gif'

        elif dice.upper() == 'D20':
            number = random.randint(1, 20)
            url = 'https://media.giphy.com/media/3oriNPdeu2W1aelciY/giphy.gif'

        else:
            found = False

        if found:
            embed = discord.Embed(title='🎲 Dice Roll',
                                  description=f"{self.client.user.name} will roll a digital dice",
                                  colour=ctx.author.colour,
                                  timestamp=ctx.message.created_at)
            embed.add_field(name='From:', value=ctx.author.mention)
            embed.add_field(name='Result:', value=f"`You rolled a {number}!`")

            embed.set_thumbnail(url=url)
        else:
            embed = discord.Embed(title='🚫 Error!',
                                  description=f"{self.client.user.name} says something went wrong.",
                                  colour=ctx.author.colour,
                                  timestamp=ctx.message.created_at)
            embed.add_field(name='Bad Argument',
                            value='Specify the dice you want to roll. Choose from `D00`, `D4`, `D6`, `D8`, `D10`, `D12`, `D20`.')
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=['8_ball', '8ball'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def eightball(self, ctx, *, question):
        """Digital 8ball. Answers to yes or no questions."""

        responses = random.choice(['As I see it, yes.', 'Ask again later.', 'Better not tell you now.',
                               'Cannot predict now.', 'Concentrate and ask again.', 'Don’t count on it.',
                               'It is certain.', 'It is decidedly so.', 'Most likely.', 'My reply is no.',
                               'My sources say no.', 'Outlook not so good.', 'Outlook good.',
                               'Reply hazy, try again.', 'Signs point to yes.', 'Very doubtful.',
                               'Without a doubt.', 'Yes.', 'Yes, definitely.', 'You may rely on it.',
                               'Yesn\'t', 'Idk man you tell me.', 'LMAO don\'t keep your hopes up',
                               'uhm, I don\'t think so...', 'hell yeah', 'wtf obviously not', '👍', '👎',
                               'C3 approves', 'Koegawa doesn\'t approve'
        ])

        embed = discord.Embed(title='🎱 8ball Simulator',
                              description=f"{self.client.user.name} will simulate a digital 8ball.",
                              colour=ctx.author.colour,
                              timestamp=ctx.message.created_at)
        fields = [('From:', ctx.author.mention, True),
                  ('Question:', f"*{question}*", True),
                  ('Result:', f"`{responses}`", True)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_thumbnail(url='https://media.giphy.com/media/ZxblomRBRsdDkSSK9v/giphy.gif')
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

    @commands.command(aliases=['penis', 'howbig', 'peepee', 'pickle', 'schlong', 'glizzy'], hidden=True)
    @commands.cooldown(3, 5, commands.BucketType.user)
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
    @commands.cooldown(3, 5, commands.BucketType.user)
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
    @commands.cooldown(3, 5, commands.BucketType.user)
    async def wink(self, ctx, member: discord.Member=None, *, reason='for no reason.'):
        """<Wink Gif Here>"""

        if not member:
            member =  self.client.user

        api_url = "https://some-random-api.ml/animu/wink"
        await ctx.send('🔎 **Searching for gifs online...**')
        async with request('GET', api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                img = data["link"]

            else:
                await ctx.send(f"API returned a {response.status} status.")

            embed = discord.Embed(description=f"*{ctx.author.mention} winks at {member.mention} {reason}*",
                                  colour=ctx.author.colour,
                                  timestamp=ctx.message.created_at)
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url)
            embed.set_image(url=img)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(3, 5, commands.BucketType.user)
    async def pat(self, ctx, member: discord.Member=None, *, reason='for no reason.'):
        """Pat like you would a dog."""

        if not member:
            member = self.client.user

        api_url = "https://some-random-api.ml/animu/pat"
        await ctx.send('🔎 **Searching for gifs online...**')
        async with request('GET', api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                img = data["link"]

            else:
                await ctx.send(f"API returned a {response.status} status.")

            embed = discord.Embed(description=f"*{ctx.author.mention} pats {member.mention} {reason}*",
                                  colour=ctx.author.colour,
                                  timestamp=ctx.message.created_at)
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url)
            embed.set_image(url=img)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(3, 5, commands.BucketType.user)
    async def hug(self, ctx, member: discord.Member=None, *, reason='for no reason.'):
        """XOXO without the Xs"""

        if not member:
            member = self.client.user

        api_url = "https://some-random-api.ml/animu/hug"
        await ctx.send('🔎 **Searching for gifs online...**')
        async with request('GET', api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                img = data["link"]

            else:
                await ctx.send(f"API returned a {response.status} status.")

            embed = discord.Embed(description=f"*{ctx.author.mention} hugs {member.mention} {reason}*",
                                  colour=ctx.author.colour,
                                  timestamp=ctx.message.created_at)
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url)
            embed.set_image(url=img)
            await ctx.send(embed=embed)

    @commands.command(aliases=['face_palm', 'facepalms'])
    @commands.cooldown(3, 5, commands.BucketType.user)
    async def facepalm(self, ctx, *, reason=' '):
        """For those frustrating moments"""

        api_url = "https://some-random-api.ml/animu/face-palm"
        await ctx.send('🔎 **Searching for gifs online...**')
        async with request('GET', api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                img = data["link"]

            else:
                await ctx.send(f"API returned a {response.status} status.")

            embed = discord.Embed(description=f"{ctx.author.mention} facepalms {reason}",
                                  colour=ctx.author.colour,
                                  timestamp=ctx.message.created_at)
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url)
            embed.set_image(url=img)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(3, 5, commands.BucketType.user)
    async def pikachu(self, ctx, *, reason=' '):
        """Random gifs and images of your electric, yellow friend"""

        api_url = "https://some-random-api.ml/img/pikachu"
        await ctx.send('🔎 **Searching for Pikachu online...**')
        async with request('GET', api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                img = data["link"]

            else:
                await ctx.send(f"API returned a {response.status} status.")

            embed = discord.Embed(title='Pikachu Pics',
                                  url='https://some-random-api.ml/',
                                  colour=ctx.author.colour,
                                  timestamp=ctx.message.created_at)
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url)
            embed.set_image(url=img)
            await ctx.send(embed=embed)

    @commands.command(aliases=['memes', 'joke', 'jokes', 'funny'])
    @commands.cooldown(5, 3, commands.BucketType.user)
    async def meme(self, ctx):
        """Meme Generator ( ͡° ͜ʖ ͡°)"""

        api_url = 'https://meme-api.herokuapp.com/gimme'
        await ctx.send('🔎 **Locating the funny...**')
        async with request('GET', api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                source = data['postLink']
                subreddit = data['subreddit']
                caption = data['title']
                meme = data['url']

            else:
                await ctx.send(f"API returned a {response.status} status.")

            embed = discord.Embed(title=caption,
                                  url=source,
                                  description=f"**Subreddit:** [r/{subreddit}](https://www.reddit.com/r/{subreddit}/)",
                                  colour=ctx.author.colour,
                                  timestamp=ctx.message.created_at)
            embed.set_image(url=meme)
            embed.set_footer(text='PS: Click on the meme above to read small text')
            await ctx.send(embed=embed)

    @commands.command(aliases=['chat', 'guhbot', 'reply', 'guhbot,', 'guh,'])
    @commands.cooldown(5, 3, commands.BucketType.user)
    async def chatbot(self, ctx, *, message: str=None):
        """Have a simple conversation with GuhBot"""

        api_url = f"https://some-random-api.ml/chatbot/?message={message}"
        await ctx.send('🧠 **Thinking of a response...**', delete_after=3)
        async with request('GET', api_url, headers={}) as response:
            if response.status == 200:
                data = await response.json()
                reply = data['response']

                await ctx.send(reply)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.client.ready:
            self.client.cogs_ready.ready_up('Fun')

def setup(client):
    client.add_cog(Fun(client))
