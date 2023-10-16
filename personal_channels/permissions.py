from discord.ui import button,select,Select,Button,InputText,mentionable_select
from pydantic import BaseModel
from utils.classes import EmptyView,CustomModal
from client import Client
from discord import Interaction,Embed,SelectOption,TextChannel,Member,Role,PermissionOverwrite
from utils.db.documents.channel import Channel
from asyncio import sleep

configurable_permissions = [
	'view_channel',
	'send_messages',
	'attach_files',
	'add_reactions',
	'read_message_history']



class ManagerPermissions(EmptyView):
	def __init__(self,client:Client,cog,channel:TextChannel,channel_data:Channel) -> None:
		super().__init__()
		self.client = client
		self.cog = cog
		self.channel = channel
		self.channel_data = channel_data
		self.embed:Embed
		self.selected_mentionable:Member|Role|None = None
		self.initalize_embed()
		self.add_items(self.select_mentionable) # type: ignore

	async def current_permission_overwrite(self) -> PermissionOverwrite:
		self.channel = await self.client.fetch_channel(self.channel.id) # type: ignore
		return self.channel.overwrites_for(self.selected_mentionable)  # type: ignore

	async def reload_button_colors(self) -> None:
		current_permissions = await self.current_permission_overwrite()
		for permission in configurable_permissions:
			self.get_item(f'button_{permission}').style = 3 if getattr(current_permissions,permission) in [True,None] else 4 # type: ignore

	def initalize_embed(self) -> None:
		existing_permissions = self.channel_data.permissions
		roles_and_members = [m for m in ((self.channel.guild.get_role(r) or self.channel.guild.get_member(r)) for r in existing_permissions)] # type: ignore
		self.embed = Embed(
			title='personal channel permission manager',
			description='\n'.join([m.mention for m in roles_and_members if m is not None]) or 'no custom permissions set',
			color=0x6969ff)
		if self.selected_mentionable is None: return
		permissions = self.channel.permissions_for(self.selected_mentionable) # type: ignore
		for permission in configurable_permissions:
			self.embed.add_field(name=permission.replace('_',' '),value=str(getattr(permissions,permission)))
	
	@mentionable_select(
		custom_id='select_mentionable',row=0,
		placeholder='select a role/user')
	async def select_mentionable(self,select:Select,interaction:Interaction) -> None:
		if select.values[0].id == self.channel_data.owner: # type: ignore
			await interaction.response.send_message(embed=Embed(title='you cannot modify your own permissions!',color=0xff6969),ephemeral=True)
			return
		if select.values[0].id in self.client.project.bot.immutable_roles: # type: ignore
			await interaction.response.send_message(embed=Embed(title='you cannot modify the permissions of this role!',color=0xff6969),ephemeral=True)
			return
		if isinstance(select.values[0],Member): # type: ignore
			if select.values[0].guild_permissions.administrator: # type: ignore
				await interaction.response.send_message(embed=Embed(title='you cannot modify the permissions of this user!',description='this user has the administrator permission, there would be no point',color=0xff6969),ephemeral=True)
				return
		if isinstance(select.values[0],Role): # type: ignore
			if select.values[0].permissions.administrator: # type: ignore
				await interaction.response.send_message(embed=Embed(title='you cannot modify the permissions of this role!',description='this role has the administrator permission, there would be no point',color=0xff6969),ephemeral=True)
				return
		self.selected_mentionable = select.values[0] # type: ignore
		self.initalize_embed()
		self.add_items(self.button_view_channel,self.button_send_messages,self.button_attach_files,self.button_add_reactions,self.button_read_message_history) # type: ignore
		await self.reload_button_colors()
		await interaction.response.edit_message(embed=self.embed,view=self)

	@button(
		custom_id='button_view_channel',
		label='view channel',
		style=1,row=1) # type: ignore
	async def button_view_channel(self,button:Button,interaction:Interaction) -> None:
		permissions = await self.current_permission_overwrite()

		permissions.view_channel = not permissions.view_channel in [True,None]
		await self.channel.set_permissions(self.selected_mentionable,overwrite=permissions) # type: ignore
		self.initalize_embed()
		await self.reload_button_colors()
		await interaction.response.edit_message(embed=self.embed,view=self)
	
	@button(
		custom_id='button_send_messages',
		label='send messages',
		style=1,row=1) # type: ignore
	async def button_send_messages(self,button:Button,interaction:Interaction) -> None:
		permissions = await self.current_permission_overwrite()
		permissions.send_messages = not permissions.send_messages in [True,None]
		await self.channel.set_permissions(self.selected_mentionable,overwrite=permissions) # type: ignore
		self.initalize_embed()
		await self.reload_button_colors()
		await interaction.response.edit_message(embed=self.embed,view=self)
	
	@button(
		custom_id='button_attach_files',
		label='attach files',
		style=1,row=1) # type: ignore
	async def button_attach_files(self,button:Button,interaction:Interaction) -> None:
		permissions = await self.current_permission_overwrite()
		permissions.attach_files = not permissions.attach_files in [True,None]
		await self.channel.set_permissions(self.selected_mentionable,overwrite=permissions) # type: ignore
		self.initalize_embed()
		await self.reload_button_colors()
		await interaction.response.edit_message(embed=self.embed,view=self)
	
	@button(
		custom_id='button_add_reactions',
		label='add reactions',
		style=1,row=1) # type: ignore
	async def button_add_reactions(self,button:Button,interaction:Interaction) -> None:
		permissions = await self.current_permission_overwrite()
		permissions.add_reactions = not permissions.add_reactions in [True,None]
		await self.channel.set_permissions(self.selected_mentionable,overwrite=permissions) # type: ignore
		self.initalize_embed()
		await self.reload_button_colors()
		await interaction.response.edit_message(embed=self.embed,view=self)
	
	@button(
		custom_id='button_read_message_history',
		label='read message history',
		style=1,row=1) # type: ignore
	async def button_read_message_history(self,button:Button,interaction:Interaction) -> None:
		permissions = await self.current_permission_overwrite()
		permissions.read_message_history = not permissions.read_message_history in [True,None]
		await self.channel.set_permissions(self.selected_mentionable,overwrite=permissions) # type: ignore
		self.initalize_embed()
		await self.reload_button_colors()
		await interaction.response.edit_message(embed=self.embed,view=self)
		