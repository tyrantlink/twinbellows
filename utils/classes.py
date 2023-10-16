from discord import Interaction,Embed
from discord.ui import View,Item,Modal,InputText
from functools import partial

class EmptyView(View):
	def __init__(self,*items:Item,timeout:float|None=None,disable_on_timeout:bool=False):
		self.embed:Embed
		tmp,self.__view_children_items__ = self.__view_children_items__,[] # type: ignore
		super().__init__(*items,timeout=timeout,disable_on_timeout=disable_on_timeout)
		self.__view_children_items__ = tmp # type: ignore
		for func in self.__view_children_items__:
			item: Item = func.__discord_ui_model_type__(**func.__discord_ui_model_kwargs__)
			item.callback = partial(func,self,item) # type: ignore
			item._view = self
			setattr(self,func.__name__,item)

	def add_items(self,*items:Item) -> None:
		for item in items:
			if item not in self.children: self.add_item(item)

	async def on_error(self,error:Exception,item:Item,interaction:Interaction) -> None:
		embed = Embed(title='an error has occurred!',color=0xff6969)
		embed.add_field(name='error',value=str(error))
		await interaction.followup.send(embed=embed,ephemeral=True)

class CustomModal(Modal):
	def __init__(self,view:View|EmptyView,title:str,children:list[InputText]) -> None:
		self.view = view
		self.interaction = None
		super().__init__(*children,title=title)

	async def callback(self, interaction: Interaction):
		self.interaction = interaction
		self.stop()