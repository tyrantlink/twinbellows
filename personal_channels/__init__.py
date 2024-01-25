from client import Client,guild_id
from discord import Cog,slash_command,ApplicationContext,TextChannel
from aiofiles import open as aopen
from discord.ext.tasks import loop
from .config import Config,ConfigView
from json import loads
from .manager import ManagerHome
from .morber import Morb


class PersonalChannels(Cog):
	def __init__(self,client:Client) -> None:
		self.client = client
		self.config = self.load_config()
	
	def load_config(self) -> Config:
		with open('config.json','r') as f:
			return Config(**loads(f.read()))
	
	@slash_command(
		name='config',
		description='set personal channel manager config',
		guild_ids=[guild_id],guild_only=True)
	async def slash_config(self,ctx:ApplicationContext) -> None:
		view = ConfigView(self.client,self)
		await ctx.response.send_message(embed=view.embed,view=view,ephemeral=True)

	@Cog.listener()
	async def on_ready(self) -> None:
		...
		# m = Morb(self.client,self.config)
		# await m.morb()
	
	@slash_command(
		name='manage',
		description='manage your personal channel',
		guild_ids=[guild_id],guild_only=True)
	async def slash_manage(self,ctx:ApplicationContext) -> None:
		if not isinstance(ctx.channel,TextChannel):
			await ctx.response.send_message('this command can only be used in a normal text channel!',ephemeral=True)
			return
		channel_data = await self.client.db.channel(ctx.channel_id) # type: ignore
		if channel_data is None:
			await ctx.response.send_message('this channel is not a personal channel!',ephemeral=True)
			return

		if ctx.author.id not in [*channel_data.owners,*self.client.project.bot.admins]: # type: ignore
			await ctx.response.send_message('you do not own this channel!',ephemeral=True)
			return

		view = ManagerHome(self.client,self,ctx.channel,channel_data)
		await ctx.response.send_message(embed=view.embed,view=view,ephemeral=True) # type: ignore





def setup(client:Client) -> None:
	client.add_cog(PersonalChannels(client))
	print('loaded personal_channels')