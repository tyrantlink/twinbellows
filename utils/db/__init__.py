from beanie import init_beanie
from .documents import Channel
from motor.motor_asyncio import AsyncIOMotorClient

class MongoDatabase:
	def __init__(self,mongo_uri:str) -> None:
		self._client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=5000)['twinbellows']

	async def ready(self) -> None:
		await init_beanie(self._client, document_models=[Channel]) # type: ignore

	async def channel(self,_id:int|str,use_cache:bool=True) -> Channel|None:
		"""user documents"""
		return await Channel.find_one({'_id': _id},ignore_cache=not use_cache)