# 3rd Party Imports
import discord
from discord.ext.commands import Cog
import databases

# Local Imports
from utils import load_config

global_config = load_config()
config = global_config

class vip(Cog):
    
	#check if vip is still valid
	#this is probably going to need to be threaded?
	@Cog.listener()
	async def on_message(self, message):

		#vip role
		vip_role = discord.utils.get(message.guild.roles, name="VIP")

		#stop bot from replying to itself :)
		if message.author.bot:
			return
		
		#don't bother checking if they are still a vip if they don't have the role in the first place...
		if vip_role in message.author.roles:

			#connect to xf database
			database = databases.Database(global_config.databases.tf2maps_site)
			await database.connect()

			#check if discord id is linked
			query = "SELECT user_id FROM xf_user_field_value WHERE field_id = :field_id AND field_value = :field_value"
			values = {"field_id": "discord_user_id", "field_value": message.author.id}
			result = await database.fetch_one(query=query, values=values)

			#check if they are vip
			query = "SELECT secondary_group_ids FROM xf_user WHERE user_id = :user_id AND find_in_set(:vip_gid, secondary_group_ids)"
			values = {"user_id": result[0], "vip_gid": 19}
			result = await database.fetch_one(query=query, values=values)
			
			#if not remove vip role otherwise do nothing :)
			if not result:
				await message.channel.send("<@" + str(message.author.id) + "> Your VIP status has expired. Upgrade to VIP https://tf2maps.net/account/upgrades")
				await message.author.remove_roles(vip_role)
				return
