# 3rd party modules
import discord
from aiosqlite import connect
from discord.ext import commands

class Events(commands.Cog):
    """What more can I say? They're fun commands."""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Log deleted message into database"""
        
        cur = await self.client.db.cursor()
        await cur.execute('SELECT * FROM snipe WHERE channel_id = ?', (message.channel.id,))
        is_snipe = await cur.fetchone()

        if is_snipe:
            cur1 = await self.client.db.cursor()
            await cur1.execute('UPDATE snipe SET user_id = ?, time = ?, message = ? WHERE channel_id = ?', 
            (message.author.id, message.created_at, message.content, message.channel.id))
            await cur1.close()
            await self.client.db.commit()

        else:
            cur2 = await self.client.db.cursor()
            await cur2.execute('INSERT INTO snipe (channel_id, user_id, time, message) VALUES (?, ?, ?, ?)', 
            (message.channel.id, message.author.id, message.created_at, message.content))
            await cur2.close()
            await self.client.db.commit()

        await cur.close()

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.client.ready:
            self.client.cogs_ready.ready_up('Events')

def setup(client):
    client.add_cog(Events(client))
