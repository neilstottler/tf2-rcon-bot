import discord
from discord.ext.commands import Cog, command, has_any_role
from utils import load_config
import asyncssh
import asyncio

global_config = load_config()
config = global_config.sftp

class server(Cog):

    #server command: start, stop, restart, update
    @command()
    @has_any_role('Staff', 'Server Mods', 'Senior Staff', 'Fub')
    async def server(self, ctx, server, command):

        servers = ["eu", "us", "eumvm", "usmvm"]
        commands = ["start", "stop", "restart", "update"]

        if command in commands:
            if server in servers:
                #eu
                if server == "eu":
                    await ctx.send(await server_connection("tf", "eu.tf2maps.net", 22, command))
                #us
                elif server == "us":
                    await ctx.send(await server_connection("tf", "us.tf2maps.net", 22, command))

                #eumvm
                elif server == "eumvm":
                    await ctx.send(await server_connection("mvm", "eu.tf2maps.net", 22, command))

                #usmvm
                elif server == "usmvm":
                    await ctx.send(await server_connection("mvm", "us.tf2maps.net", 22, command))

                else:
                    await ctx.send("How did it reach this part?")

            else:
                await ctx.trigger_typing()
                await ctx.send("Server not found. Check `?servers`.")

        else:
            await ctx.send("Invalid command argument. See ?commands.")
        
    #command to see commands for ?server
    @command()
    @has_any_role('Staff', 'Server Mods', 'Senior Staff', 'Fub')
    async def commands(self, ctx):

        await ctx.trigger_typing()

        embed=discord.Embed()
        embed.add_field(name="Availible Servers", value="start, stop, restart, update")
        embed.set_footer(text="TF2M RCON v1")

        await ctx.send(embed=embed)

#server connecting
async def server_connection(user, hostname, port, command):

    commands = ["start", "stop", "restart", "update"]

    async with asyncssh.connect(
        hostname,
        port=port, 
        username=user, 
        password=config.master.password,
        known_hosts=None
    ) as conn:
        if command in commands:
            if command == "start":

                await conn.run('./server start')
                return "Server starting."

            elif command == "stop":

                await conn.run('./server stop')
                return "Stopping server."
 
            elif command == "restart":

                await conn.run('./server restart')                                
                return "Restarting server"

            elif command == "update":
                
                await conn.run('./server update')
                return "Updating server."

            else:
                return "How did you manage to break this after a checksum?" 

        else:
            return "Invalid command. Check `?commands`."