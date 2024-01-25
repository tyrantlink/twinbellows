from discord.ui import button,select,Select,Button,InputText
from pydantic import BaseModel
from utils.classes import EmptyView,CustomModal
from client import Client
from discord import Interaction,Embed,SelectOption,TextChannel
from utils.db.documents.channel import Channel
from asyncio import sleep
from .permissions import ManagerPermissions

slowmode_map = {
	0    :'slowmode: off',
	5    :'slowmode: 5 seconds',
	10   :'slowmode: 10 seconds',
	15   :'slowmode: 15 seconds',
	30   :'slowmode: 30 seconds',
	60   :'slowmode: 1 minute',
	120  :'slowmode: 2 minutes',
	300  :'slowmode: 5 minutes',
	600  :'slowmode: 10 minutes',
	900  :'slowmode: 15 minutes',
	1800 :'slowmode: 30 minutes',
	3600 :'slowmode: 1 hour',
	7200 :'slowmode: 2 hours',
	21600:'slowmode: 6 hours'}


class ManagerHome(EmptyView):
	def __init__(self,client:Client,cog,channel:TextChannel,channel_data:Channel) -> None:
		super().__init__()
		self.client = client
		self.cog = cog
		self.channel = channel
		self.channel_data = channel_data
		self.embed:Embed
		self.initalize_embed()
		self.add_items(self.select_slowmode,self.button_name,self.button_topic,self.button_nsfw,self.button_permissions) # type: ignore
		self.get_item('select_slowmode').options = [SelectOption(label=v,value=str(k),default=k == self.channel.slowmode_delay) for k,v in slowmode_map.items()] # type: ignore

	def initalize_embed(self) -> None:
		self.embed = Embed(title='personal channel manager',color=0x6969ff)
		self.embed.add_field(name='name',value=self.channel.name,inline=False) # type: ignore
		self.embed.add_field(name='topic',value=self.channel.topic or '{unset}',inline=False) # type: ignore
		self.embed.add_field(name='slowmode',value=slowmode_map[self.channel.slowmode_delay],inline=False) # type: ignore
		self.embed.add_field(name='age-restricted?',value=str(self.channel.is_nsfw()),inline=False) # type: ignore
	
	def sanitize_name(self,name:str) -> str:
		return name.replace(' ','-').lower()

	@select(
		custom_id='select_slowmode',
		placeholder='select slowmode',row=0,
		options=[SelectOption(label='placeholder')]) # type: ignore
	async def select_slowmode(self,select:Select,interaction:Interaction) -> None:
		self.channel = await self.channel.edit(slowmode_delay=int(select.values[0])) # type: ignore
		self.initalize_embed()
		select.options = [SelectOption(label=v,value=str(k),default=k == self.channel.slowmode_delay) for k,v in slowmode_map.items()] # type: ignore
		await interaction.response.edit_message(embed=self.embed,view=self)

	@button(
		custom_id='button_name',
		label='edit name',
		style=1,row=1) # type: ignore
	async def button_name(self,button:Button,interaction:Interaction) -> None:
		modal = CustomModal(self,'change channel name',[InputText(label='name',value=self.channel.name,min_length=1,max_length=100)]) # type: ignore
		await interaction.response.send_modal(modal)
		await modal.wait()
		self.channel = await self.channel.edit(name=self.sanitize_name(modal.children[0].value)) # type: ignore
		self.initalize_embed()
		await modal.interaction.response.edit_message(embed=self.embed) # type: ignore

	@button(
		custom_id='button_topic',
		label='edit topic',
		style=1,row=1) # type: ignore
	async def button_topic(self,button:Button,interaction:Interaction) -> None:
		modal = CustomModal(self,'change channel topic',[InputText(label='topic',value=self.channel.topic or '',min_length=0,max_length=1024)]) # type: ignore
		await interaction.response.send_modal(modal)
		await modal.wait()
		self.channel = await self.channel.edit(topic=modal.children[0].value or None) # type: ignore
		self.initalize_embed()
		await modal.interaction.response.edit_message(embed=self.embed) # type: ignore
	
	@button(
		custom_id='button_nsfw',
		label='swap age-restriction',
		style=1,row=1) # type: ignore
	async def button_nsfw(self,button:Button,interaction:Interaction) -> None:
		self.channel = await self.channel.edit(nsfw=not self.channel.is_nsfw()) # type: ignore
		self.initalize_embed()
		await interaction.response.edit_message(embed=self.embed)
	
	@button(
		custom_id='button_permissions',
		label='manage permissions',
		style=1,row=2) # type: ignore
	async def button_permissions(self,button:Button,interaction:Interaction) -> None:
		new_view = ManagerPermissions(self.client,self.cog,await self.client.fetch_channel(self.channel.id),self.channel_data) # type: ignore
		await interaction.response.edit_message(embed=new_view.embed,view=new_view)