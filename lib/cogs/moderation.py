# 3rd party modules
import discord
from discord.ext import commands


class Moderation(commands.Cog):
    """Commands for your Moderators"""

    def __init__(self, client):
        self.client = client

    class BannedMember(commands.Converter):
        async def convert(self, ctx, argument):
            if argument.isdigit():
                member_id = int(argument, base=10)
                try:
                    return await ctx.guild.fetch_ban(discord.Object(id=member_id))
                except discord.NotFound:
                    raise commands.BadArgument('This member has not been banned before.') from None

            ban_list = await ctx.guild.bans()
            entity = discord.utils.find(lambda u: str(u.user) == argument, ban_list)

            if entity is None:
                raise commands.BadArgument('This member has not been banned before.')
            return entity


    @commands.command(aliases=['delete', 'purge'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=6):
        """Deletes messsages in a channel."""

        embed = discord.Embed(
                              description=f"Deleted {amount} messages.",
                              colour=ctx.message.author.colour,
                              timestamp=ctx.message.created_at
                              )
        embed.set_author(
                         name=f"{ctx.message.author.name}#{ctx.message.author.discriminator}",
                         icon_url=ctx.message.author.avatar_url
                         )
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        await ctx.send(embed=embed, delete_after=5.0)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks members from the server (They can still join back)"""

        await member.kick(reason=reason)
        embed = discord.Embed(
                              title='⚽Kick Command',
                              description='GuhBot will kick specified member from the server.',
                              colour=ctx.message.author.colour,
                              timestamp=ctx.message.created_at
                              )
        embed.add_field(name='Kicked Member:', value=f"`{member.name}#{member.discriminator}\nID:{member.id}`", inline=False)
        embed.add_field(name='Punisher:', value=f"`{ctx.message.author.name}#{ctx.message.author.discriminator}\nID:{ctx.message.author.id}`", inline=False)
        embed.add_field(name='Reason:', value=f"`{reason}`", inline=False)
        embed.set_thumbnail(url='https://media.giphy.com/media/cb4Pg4jau2SEE/giphy.gif')
        embed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url)
        embed.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)
        await member.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban members from the server"""

        await member.ban(reason=reason)
        embed = discord.Embed(
                              title='🔨Ban Command',
                              description='GuhBot will ban the specified member from the server.',
                              colour=ctx.message.author.colour,
                              timestamp=ctx.message.created_at
                              )
        embed.add_field(name='Banned Member:', value=f"`{member.name}#{member.discriminator}\nID:{member.id}`", inline=False)
        embed.add_field(name='Punisher:', value=f"`{ctx.message.author.name}#{ctx.message.author.discriminator}\nID:{ctx.message.author.id}`", inline=False)
        embed.add_field(name='Reason:', value=f"`{reason}`")
        embed.set_thumbnail(url='https://media.giphy.com/media/C51woXfgJdug/giphy.gif')
        embed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url)
        embed.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)
        await member.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: BannedMember, *, reason = None):

        """Unban previously banned members from the server"""

        await ctx.guild.unban(member.user, reason=reason)
        embed = discord.Embed(
                              title='😅Unban Command',
                              description='GuhBot will unban previously banned members from the server.',
                              colour=ctx.message.author.colour,
                              timestamp=ctx.message.created_at
                              )
        embed.add_field(name='Unbanned Member:', value=f"`{member.user}\nID:{member.user.id}`", inline=False)
        embed.add_field(name='Unbanned by:', value=f"`{ctx.message.author.name}#{ctx.message.author.discriminator}\nID:{ctx.message.author.id}`", inline=False)
        embed.add_field(name='Reason', value=f"`{reason}`", inline=False)
        embed.set_thumbnail(url='https://media.giphy.com/media/kz0qWS2lAqtdAnEmEM/giphy.gif')
        embed.set_author(name=f"{member.user}")
        embed.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def unkick(self, ctx, member: discord.Member = None, *, reason='Because \"Erdem\" said so.'):

        """Wait what? Unkick?"""

        if not member:
            name = 'Da Vibin Mexican Green Van'
            discriminator = '1469'
            id = '353866653622337536'
            avatar_url = 'https://cdn.discordapp.com/avatars/718438151848329217/609d63f182beeed1c5c840ca5d0b1545.webp?size=1024'
        else:
            name = member.name
            discriminator = member.discriminator
            id = member.id
            avatar_url = member.avatar_url
        embed = discord.Embed(
                              title='😕Unkick Command',
                              description='Don\'t worry, this command doesn\'t do anything. By default, kicked members are able to join back to the server anyways.',
                              colour=ctx.message.author.colour,
                              timestamp=ctx.message.created_at
                              )
        embed.add_field(name='Unkicked Member:', value=f"`{name}#{discriminator}\nID:{id}`", inline=False)
        embed.add_field(name='Punisher:', value=f"`{ctx.message.author.name}#{ctx.message.author.discriminator}\nID:{ctx.message.author.id}`", inline=False)
        embed.add_field(name='Reason:', value=f"`{reason}`", inline=False)
        embed.set_thumbnail(url='https://media.giphy.com/media/WRQBXSCnEFJIuxktnw/giphy.gif')
        embed.set_author(name=f"{name}#{discriminator}", icon_url=avatar_url)
        embed.set_footer(text=f"this joke was made by green van", icon_url='https://cdn.discordapp.com/avatars/718438151848329217/609d63f182beeed1c5c840ca5d0b1545.webp?size=1024')
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.client.ready:
            self.client.cogs_ready.ready_up('Moderation')

def setup(client):
    client.add_cog(Moderation(client))
