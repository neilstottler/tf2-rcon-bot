from asyncio.windows_events import NULL
import discord
from discord import client
from discord.ext.commands import Cog, command, has_any_role
from discord.ext import commands
from utils import load_config

global_config = load_config()
config = global_config

# TWITTER KEYS (...would go here)
consumer_key = None
consumer_secret = None
access_token = None
access_token_secret = None

class twitter(Cog):

    @commands.command()
    @has_any_role('Staff', 'Server Mods', 'Senior Staff', 'Fub')
    async def release(self, ctx):

        #delete message in channel it was sent
        await ctx.message.delete()
        #sends message as dm
        msg = await ctx.author.send("Please enter your steam workshop link. Type cancel at anytime to stop the submission.")
        def check(message):
            return message.author == ctx.author and message.channel == msg.channel

        msg = await ctx.author.send('**First let me have your item\'s Steam Workshop link.**')
        link = await ctx.bot.wait_for('message', check=check)

        #this prints whatever was said
        print(link.content)