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

class Games(commands.Cog):
    """Some games to play in your server!"""

    def __init__(self, client):
        self.client = client

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

def setup(client):
    client.add_cog(Games(client))
