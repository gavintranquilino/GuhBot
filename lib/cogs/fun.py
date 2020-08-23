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
    @commands.cooldown(1, 3, commands.BucketType.user)
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

    @commands.command(aliases=['dice', 'dice_roll'])
    @commands.cooldown(3, 8, commands.BucketType.user)
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
    @commands.cooldown(2, 8, commands.BucketType.user)
    async def eightball(self, ctx, *, question):
        """Digital 8ball. Answers to yes or no questions"""

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

    @commands.command(aliases=['aki'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def akinator(self, ctx, sfw: Optional[bool]=False, language: Optional[str]='english'):
        """GuhBot will guess a character you think of"""

        await ctx.trigger_typing()

        aki = Akinator()
        stopped = False

        question = await aki.start_game(child_mode=sfw, language=language.lower())

        while aki.progression <= 80:

            await ctx.trigger_typing()

            question_embed = discord.Embed(title=f"Question #{aki.step + 1}",
                                  colour=ctx.author.colour,
                                  timestamp=ctx.message.created_at)

            question_embed.add_field(name=question,
                            value='[yes (**y**) / no (**n**) / idk (**i**) / probably (**p**) / probably not (**pn**)]\n[back (**b**) / stop (**s**)]')

            question_embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/705081891190997073.gif')

            question_embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url)

            question_embed.set_footer(text='GuhBot is not affiliated, authorized, or endorsed by Akinator.',
                             icon_url='https://cdn.discordapp.com/avatars/356065937318871041/bcbfc8d951e3c75b6f453eec0f978a38.png')

            await ctx.send(embed=question_embed)

            def check(message):
                return message.author == ctx.author and message.channel == ctx.message.channel

            answer = await self.client.wait_for(event='message', check=check, timeout=30)
            answer = answer.content

            try:
                if answer.lower() == 'back' or answer.lower() == 'b':
                    try:
                        question = await aki.back()

                    except akinator.CantGoBackAnyFurther:
                        await ctx.send(f"{ctx.author.mention}, you can\'t go back any further.", delete_after=10)

                elif answer.lower() == 'stop' or answer.lower() == 's':
                    stopped = True
                    stop_embed = discord.Embed(title=f"Stopped Game",
                                               description=f"{ctx.author.mention} has stopped the running Akinator game.",
                                               colour=self.client.colours['RED'],
                                               timestamp=ctx.message.created_at)
                    stop_embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                                     icon_url=ctx.author.avatar_url)

                    stop_embed.set_footer(text='GuhBot is not affiliated, authorized, or endorsed by Akinator.',
                                     icon_url='https://cdn.discordapp.com/avatars/356065937318871041/bcbfc8d951e3c75b6f453eec0f978a38.png')

                    await ctx.send(embed=stop_embed)

                    break

                else:
                    await ctx.trigger_typing()

                    question = await aki.answer(answer)

            except akinator.InvalidAnswerError:
                await ctx.send(f"{ctx.author.mention}, `{answer}` is an Invalid Answer.", delete_after=10)

        if not stopped:
            await aki.win()

            win_embed = discord.Embed(title=f"{ctx.author.name}, Is this your character?",
                                      colour=ctx.author.colour,
                                      timestamp=ctx.message.created_at)
            win_embed.add_field(name=aki.first_guess['name'],
                                value=f"{aki.first_guess['description']}\nRanked #{aki.first_guess['ranking']}")

            win_embed.add_field(name='\u200b',
                                value=f"[yes (**y**) / no (**n**)]",
                                inline=False)

            win_embed.set_image(url=aki.first_guess['absolute_picture_path'])

            win_embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url)

            win_embed.set_footer(text='GuhBot is not affiliated, authorized, or endorsed by Akinator.',
                             icon_url='https://cdn.discordapp.com/avatars/356065937318871041/bcbfc8d951e3c75b6f453eec0f978a38.png')

            await ctx.send(embed=win_embed)

            correct = await self.client.wait_for(event='message', check=check, timeout=30)
            correct = correct.content

            if correct.lower() == "yes" or correct.lower() == "y":
                embed = discord.Embed(title='Great! Guessed right one more time.',
                                      description='I love this game!',
                                      colour=ctx.author.colour,
                                      timestamp=ctx.message.created_at)

            else:
                embed = discord.Embed(title='Aww you beat me!',
                                      description='I\'ll get you next time!',
                                      colour=ctx.author.colour,
                                      timestamp=ctx.message.created_at)

            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.client.ready:
            self.client.cogs_ready.ready_up('Fun')

def setup(client):
    client.add_cog(Fun(client))
