# 3rd party modules
import discord
from discord.ext import commands

# Builtin modules
from aiohttp import request


class Misc(commands.Cog):
    """Miscellaneous Commands"""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['corona', 'coronavirus'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def covid(self, ctx, *, country: str=None):
        """Daily COVID-19 summary"""

        api_url = 'https://api.covid19api.com/summary'
        await ctx.send('🔎 **Fetching COVID-19 stats online...**')
        async with request('GET', api_url, headers={}) as response:

            if not country:
                country = 'Global'
                if response.status == 200:
                    data = await response.json()
                    newConfirmed = f"{data[country]['NewConfirmed']:,d}"
                    totalConfirmed = f"{data[country]['TotalConfirmed']:,d}"
                    newDeaths = f"{data[country]['NewDeaths']:,d}"
                    totalDeaths = f"{data[country]['TotalDeaths']:,d}"
                    newRecovered = f"{data[country]['NewRecovered']:,d}"
                    totalRecovered = f"{data[country]['TotalRecovered']:,d}"

                else:
                    await ctx.send(f"API returned a {response.status} status.")

            else:
                country = country.title()
                if response.status == 200:
                    data = await response.json()
                    for element in data['Countries']:
                        if element['Country'] == country:
                            newConfirmed = f"{element['NewConfirmed']:,d}"
                            totalConfirmed = f"{element['TotalConfirmed']:,d}"
                            newDeaths = f"{element['NewDeaths']:,d}"
                            totalDeaths = f"{element['TotalDeaths']:,d}"
                            newRecovered = f"{element['NewRecovered']:,d}"
                            totalRecovered = f"{element['TotalRecovered']:,d}"

                else:
                    await ctx.send(f"API returned a {response.status} status.")

            embed = discord.Embed(title=f"{country} COVID-19 Stats",
                                  url='https://covid19api.com/',
                                  description='Get current [COVID-19 statistics](https://covid19api.com/). Data updated multiple times a day.',
                                  colour=ctx.author.colour,
                                  timestamp=ctx.message.created_at)
            fields = [('New Confirmed Cases', newConfirmed, True),
                      ('Total Confirmed Cases', totalConfirmed, True),
                      ('New Deaths', newDeaths, False),
                      ('Total Deaths', totalDeaths, True),
                      ('New Recoveries', newRecovered, True),
                      ('Total Recoveries', totalRecovered, False),
                      ('Help Stop COVID-19', '[Advice to the Public](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public)', True)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/239446877953720321/691020838379716698/unknown.png')
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                             icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.client.ready:
            self.client.cogs_ready.ready_up('Misc')

def setup(client):
    client.add_cog(Misc(client))
