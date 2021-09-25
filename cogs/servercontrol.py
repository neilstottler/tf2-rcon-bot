import discord
from discord.ext.commands import Cog, command, has_any_role
from utils import load_config
import asyncssh
import subprocess
import os
import nmap



global_config = load_config()
config = global_config.sftp

class server(Cog):

    #server command: start, stop, restart, update
    @command()
    @has_any_role('staff', 'server mods', 'senior staff', 'fub')
    async def server(self, ctx, server, command):

        servers = ["eu", "us", "eumvm", "usmvm"]
        commands = ["start", "stop", "restart", "update"]

        if server in servers:
            #eu
            if server == "eu":
                async with asyncssh.connect(
                    host= config.euimp.hostname,
                    port=config.euimp.port, 
                    username=config.euimp.username, 
                    password=config.euimp.password,
                    known_hosts=None
                    ) as conn:
                        if command in commands:
                            if command == "start":

                                await conn.run('./server start')
                                await ctx.send("Server starting.")
                                
                                #be smart and actually check if the server went down :)
                                ping = nmap.PortScanner.scan(hosts='eu.tf2maps.net', ports='27015')
                                if ping == 1:
                                    await ctx.send("Server is up.")
                                else:
                                    await ctx.send("Server did not boot.")

                            elif command == "stop":

                                await conn.run('./server stop')
                                await ctx.send("Stopping server.")
 
                                #be smart and actually check if the server went down :)
                                ping = nmap.PortScanner.scan(hosts='eu.tf2maps.net', ports='27015')
                                if ping == 0:
                                    await ctx.send("Server is offline.")
                                else:
                                    await ctx.send("Server is still up.")
                            elif command == "restart":

                                await conn.run('./server restart')                                
                                await ctx.send("Restart")

                            elif command == "update":

                                await conn.run('./server update')
                                await ctx.send("Updating server.") 

                            else:
                                await ctx.send("How did you manage to break this after a checksum?")    

                        else:
                            await ctx.send("Invalid command. Check `?commands`.")

            #us
            elif server == "us":
                async with asyncssh.connect(
                    host= config.usimp.hostname,
                    port=config.usimp.port, 
                    username=config.usimp.username, 
                    password=config.usimp.password,
                    known_hosts=None
                    ) as conn:
                        if command in commands:
                            if command == "start":

                                await conn.run('./server start')
                                await ctx.send("Server starting.")

                            elif command == "stop":

                                await conn.run('./server stop')
                                await ctx.send("Stopping server.")
 
                            elif command == "restart":

                                await conn.run('./server restart')                                
                                await ctx.send("Restart")

                            elif command == "update":

                                await conn.run('./server update')
                                await ctx.send("Updating server.") 

                            else:
                                await ctx.send("How did you manage to break this after a checksum?")    

                        else:
                            await ctx.send("Invalid command. Check `?commands`.")
            #eumvm
            elif server == "eumvm":
                async with asyncssh.connect(
                    host= config.eumvm.hostname,
                    port=config.eumvm.port, 
                    username=config.eumvm.username, 
                    password=config.eumvm.password,
                    known_hosts=None
                    ) as conn:
                        if command in commands:
                            if command == "start":

                                await conn.run('./server start')
                                await ctx.send("Server starting.")

                            elif command == "stop":

                                await conn.run('./server stop')
                                await ctx.send("Stopping server.")
 
                            elif command == "restart":

                                await conn.run('./server restart')                                
                                await ctx.send("Restart")

                            elif command == "update":

                                await conn.run('./server update')
                                await ctx.send("Updating server.") 

                            else:
                                await ctx.send("How did you manage to break this after a checksum?")    

                        else:
                            await ctx.send("Invalid command. Check `?commands`.")
            #usmvm
            elif server == "usmvm":
                async with asyncssh.connect(
                    host= config.usmvm.hostname,
                    port=config.usmvm.port, 
                    username=config.usmvm.username, 
                    password=config.usmvm.password,
                    known_hosts=None
                    ) as conn:
                        if command in commands:
                            if command == "start":

                                await conn.run('./server start')
                                await ctx.send("Server starting.")

                            elif command == "stop":

                                await conn.run('./server stop')
                                await ctx.send("Stopping server.")
 
                            elif command == "restart":

                                await conn.run('./server restart')                                
                                await ctx.send("Restart")

                            elif command == "update":

                                await conn.run('./server update')
                                await ctx.send("Updating server.") 

                            else:
                                await ctx.send("How did you manage to break this after a checksum?")    

                        else:
                            await ctx.send("Invalid command. Check `?commands`.")
            else:
                await ctx.send("How did it reach this part?")
        else:
            await ctx.trigger_typing()
            await ctx.send("Server not found. Check `?servers`.")

    #command to see commands for ?server
    @command()
    @has_any_role('staff', 'server mods', 'senior staff', 'fub')
    async def commands(self, ctx):

        await ctx.trigger_typing()

        embed=discord.Embed()
        embed.add_field(name="Availible Servers", value="start, stop, restart, update")
        embed.set_footer(text="TF2M RCON v1")

        await ctx.send(embed=embed)