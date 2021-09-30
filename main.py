import discord
from cogs import *
from utils import load_config
from discord.ext import commands

config = load_config()

def main():

    bot = commands.Bot(command_prefix=config.bot_prefix)

    #load cogs
    bot.add_cog(rcon())
    bot.add_cog(server())

    #say shit in bot channel and set status
    #saying doesnt work????
    @bot.event
    async def on_ready():
        channel = config.bot_channel
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for !rcon"))

    #my attempt at understanding ctrl + c catching and not working
    try:
        bot.run(config.bot_token)
    except KeyboardInterrupt:
        print("test")
        bot.close
        pass

if __name__ == "__main__":
    main()