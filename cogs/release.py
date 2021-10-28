import discord
from discord.ext.commands import Cog, command, has_any_role
from utils import load_config

global_config = load_config()
config = global_config

class twitter(Cog):

    @command()
    @has_any_role('Staff', 'Server Mods', 'Senior Staff', 'Fub')
    async def release(self, ctx):

        #delete message in channel it was sent
        await ctx.message.delete()

        