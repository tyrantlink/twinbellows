from discord.ui import select,Select
from pydantic import BaseModel
from utils.classes import EmptyView
from client import Client
from discord import Interaction,Embed,SelectOption


class Config(BaseModel):
	archive_time:int = 90
	archive_category:int = 0
	logging_channel:int = 0
	deletion_time:int = 180
	archive_before_deletion:bool = True

class ConfigView(EmptyView):
	def __init__(self,client:Client,cog) -> None:
		super().__init__()
		self.client = client
		self.cog = cog
		self.config:Config = cog.load_config()
		self.embed:Embed
		self.initalize_embed()
		self.add_items(self.select_option) # type: ignore
		self.get_item('select_option').options = [SelectOption(label=f.name,description=f.value) for f in self.embed.fields] # type: ignore
		self.do_kill()


	def do_kill(self) -> None:
		item = self.get_item('select_option')
		item.disabled = True # type: ignore
		item.placeholder = 'this is read-only for now' # type: ignore

	
	def initalize_embed(self,load_config:bool=False) -> None:
		if load_config: self.config = self.cog.load_config()
		self.embed = Embed(title='personal channel manager config',color=0x6969ff)
		for k,v in self.config.model_dump().items():
			match k:
				case 'archive_time': k = 'archive time (days)'
				case 'deletion_time': k = 'deletion time (days)'
				case 'archive_category':
					k = 'archive category'
					v = f'<#{v}>' if v else 'none'
				case 'logging_channel':
					k = 'logging channel'
					v = f'<#{v}>' if v else 'none'
				case _: k = k.replace('_',' ')
			self.embed.add_field(name=k,value=str(v))

	@select(
			custom_id='select_option',
			placeholder='select an option',
			options=[SelectOption(label='naaa')])
	async def select_option(self,select:Select,interaction:Interaction) -> None:
		...