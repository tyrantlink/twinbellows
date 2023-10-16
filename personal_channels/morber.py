# if last message greater than 90 days, move to archive category, and send message in channel and logging channel, and send owner dm
# if last message == 166 days, dm channel owner with two week warning
# if last message == 173 days, dm channel owner with one week warning
# if last message >= 180 days, dump channel, delete channel, host under channel id
# if last message >= 360 days, delete dump

from client import Client
from utils.db.documents import Channel
from time import time
from discord import TextChannel,PermissionOverwrite
from .config import Config

#! dealing with this later


class Morb:
	def __init__(self,client:Client,config:Config) -> None:
		self.client = client
		self.config = config
		self.logging_channel = client.get_channel(config.logging_channel)

	async def _archive_channel(self,db_channel:Channel,disc_channel:TextChannel) -> None:
		print(disc_channel.overwrites)
		db_channel.permissions = {str(k.id):v._values for k,v in disc_channel.overwrites.items()} # type: ignore
		await db_channel.save() # type: ignore
		await disc_channel.edit(
			category=self.client.get_channel(self.config.archive_category),
			overwrites={
				self.client.project.bot.guild_id:PermissionOverwrite(view_channel=True,send_messages=False),
				db_channel.owner:PermissionOverwrite(view_channel=True,send_messages=True)}) # type: ignore
		print(f'archived channel {disc_channel.name}')
		exit()
	
	async def _restore_channel(self,db_channel:Channel,disc_channel:TextChannel) -> None:
		print(f'restore channel {disc_channel.name}')
		...

	async def _send_warning_dm(self,db_channel:Channel,disc_channel:TextChannel) -> None:
		print(f'send warning dm to {disc_channel.owner}')
		...

	async def _dump_channel(self,db_channel:Channel,disc_channel:TextChannel) -> None:
		print(f'dump channel {disc_channel.name}')
		...

	async def _delete_dump(self,db_channel:Channel,disc_channel:TextChannel) -> None:
		print(f'delete dump {disc_channel.dump}')
		...

	async def morb(self) -> None:
		async for db_channel in Channel.find_all():

			if db_channel.id != 816574410315005970: continue

			discord_channel = await self.client.fetch_channel(db_channel.id) # type: ignore
			async for message in discord_channel.history(limit=1): # type: ignore
				await self._archive_channel(db_channel,discord_channel)
				match round((time()-message.created_at.timestamp())/86400):
					case t if t >= 90:
						await self._archive_channel(client,discord_channel) # type: ignore
					case t if t == 166:
						await self._send_warning_dm(client,db_channel)
					case t if t == 173:
						await self._send_warning_dm(client,db_channel)
					case t if t >= 180:
						hosted_url = await _dump_channel(client,discord_channel) # type: ignore
						print(f'delete channel {discord_channel.name}')#await discord_channel.delete() # type: ignore
					case t if t >= 360:
						await self._delete_dump(client,db_channel)
					case _:
						print(f'channel {discord_channel.name} is ok')
						continue


