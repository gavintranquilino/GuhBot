# 3rd party modules
import discord
from discord.ext import commands


class Errors(commands.Cog):
    """Error handling module"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
                # If the command is currently on cooldown trip this
                m, s = divmod(error.retry_after, 60)
                h, m = divmod(m, 60)
                if int(h) is 0 and int(m) is 0:
                    value = f"You must wait `{round(float(s), 2)} seconds` to use this command!"
                elif int(h) is 0 and int(m) is not 0:
                    value = f"You must wait `{int(m)} minutes and {int(s)} seconds` to use this command!"
                else:
                    value = f"You must wait `{int(h)} hours, {int(m)} minutes and {int(s)} seconds` to use this command!"
                embed = discord.Embed(
                                      title='🛑Stop!',
                                      description=f"Sorry {ctx.author.mention}, but you\'re on a cooldown.",
                                      colour=discord.Colour.red(),
                                      timestamp=ctx.message.created_at
                                      )
                embed.set_thumbnail(url='https://media.giphy.com/media/3oz8xKaR836UJOYeOc/giphy.gif')
                embed.set_author(
                                 name=f"{ctx.author.name}#{ctx.author.discriminator}",
                                 icon_url=ctx.author.avatar_url
                                 )
                embed.add_field(name='Slow Down!!!', value=value)
                await ctx.send(embed=embed)


        elif isinstance(error, commands.CommandNotFound):
            pass

        else:
            embed = discord.Embed(
                                  title='⛔Error!',
                                  description=f"Sorry {ctx.author.mention}, but {self.client.user.name} found an error.",
                                  colour=discord.Colour.red(),
                                  timestamp=ctx.message.created_at
                                  )
            embed.set_thumbnail(url='https://media.giphy.com/media/8L0Pky6C83SzkzU55a/giphy.gif')
            embed.set_author(
                             name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url
                             )
            try:
                if hasattr(ctx.command, 'on_error'):
                    return
                else:
                    embed.add_field(name=f"Error in {ctx.command}", value=f"`{ctx.command.qualified_name} {ctx.command.signature}` \n{error}")
            except:
                embed.add_field(name=f"Error in {ctx.command}", value=f"{error}")
            await ctx.send(embed=embed)
        raise error
        print(f"{error}")

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.client.ready:
            self.client.cogs_ready.ready_up('Errors')

def setup(client):
    client.add_cog(Errors(client))
