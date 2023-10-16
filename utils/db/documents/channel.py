from beanie import Document
from datetime import timedelta 
from pydantic import Field

class Channel(Document):
	class Settings:
		name = "channels"
		use_cache = True
		validate_on_save = True
		use_state_management = True
		cache_expiration_time = timedelta(seconds=5)
	
	id:int = Field(description='discord channel id')
	owner:int = Field(description='discord user id')
	permissions:dict[int,dict[str,bool|None]] = Field(description='discord user/role id: permission level')