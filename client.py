from discord import Bot,Activity,ActivityType,PermissionOverwrite
from utils.db import MongoDatabase
from tomllib import loads
from utils.project import create_project,Project
from time import perf_counter
from utils.db.documents import Channel

guild_id:int = 0

class Client(Bot):
	def __init__(self,*args,**kwargs) -> None:
		global guild_id
		self.st = perf_counter()
		super().__init__(*args,**kwargs)
		self.project = self.get_project()
		guild_id = self.project.bot.guild_id
		self.db = MongoDatabase(self.project.mongo.uri)
		self.load_extension('personal_channels')
	
	def get_project(self) -> Project:
		with open('project.toml','r') as f:
			return create_project(loads(f.read()))
		
	async def on_connect(self) -> None:
		await self.db.ready()
		await self.change_presence(activity=Activity(type=ActivityType.custom,name='a',state=f'being a good puppy'))
		await self.sync_commands()

	async def start(self,reconnect:bool=True) -> None:
		await self.login(self.project.bot.token)
		await self.connect(reconnect=reconnect)
	
	async def on_ready(self) -> None:
		print(f'{self.user} connected to discord in {perf_counter()-self.st:.2f}s')