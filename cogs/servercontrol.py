import asyncio
import socket
import discord
from discord.ext.commands import Cog, command, has_any_role
from utils import load_config
import asyncssh

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
                    await ctx.send(await server_connection("tf", "eu.tf2maps.net", 27015, command))
                #us
                elif server == "us":
                    await ctx.send(await server_connection("tf", "us.tf2maps.net", 27015, command))

                #eumvm
                elif server == "eumvm":
                    await ctx.send(await server_connection("mvm", "eu.tf2maps.net", 27016, command))

                #usmvm
                elif server == "usmvm":
                    await ctx.send(await server_connection("mvm", "us.tf2maps.net", 27016, command))

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

    #ping gameserver
    @command()
    @has_any_role('Staff', 'Server Mods', 'Senior Staff', 'Fub')
    async def ping(self, ctx):
        pass

#server connecting
async def server_connection(user, hostname, port, command):

    commands = ["start", "stop", "restart", "update"]

    async with asyncssh.connect(
        hostname,
        port=22, 
        username=user, 
        password=config.master.password,
        known_hosts=None
    ) as conn:
        if command in commands:
            if command == "start":

                await conn.run('./server start')

                #check if server is up
                await asyncio.sleep(5)
                if await check_port(hostname, port):
                    return "Server started."
                else:
                    return "Server not started."

            elif command == "stop":

                await conn.run('./server stop')

                #check if server is running
                await asyncio.sleep(5)
                if await check_port(hostname, port):
                    return "Server not stopped."
                else:
                    return "Server is stopped."
 
            elif command == "restart":

                #stop server and update
                await conn.run('./server stop') 
                await asyncio.sleep(5)
                await conn.run('./server update')

                #check if server is up
                await asyncio.sleep(8)
                if await check_port(hostname, port):
                    return "Server restarted."
                else:
                    return "Server not restarted."

            elif command == "update":
                
                await conn.run('./server update')

                #check if server is up
                await asyncio.sleep(10)
                if await check_port(hostname, port):
                    return "Server online and updated."
                else:
                    return "Server offline."

            else:
                return "How did you manage to break this after a checksum?" 

        else:
            return "Invalid command. Check `?commands`."

#semi dirty way to check if the server is up
async def check_port(hostname, port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    location = (hostname, port)

    result_of_check = a_socket.connect_ex(location)

    if result_of_check == 0:
        return True
    else:
        return False
    pass