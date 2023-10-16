from pydantic import BaseModel


class ProjectBot(BaseModel):
	class Config:
		arbitrary_types_allowed=True
	token:str
	base_url:str
	guild_id:int
	admins:list[int]
	immutable_roles:list[int]

class ProjectMongo(BaseModel):
	class Config:
		arbitrary_types_allowed=True
	uri:str

class Project(BaseModel):
	class Config:
		arbitrary_types_allowed=True
	bot:ProjectBot
	mongo:ProjectMongo

def create_project(project:dict) -> Project:
	return Project(
		bot=ProjectBot(**project['bot']),
		mongo=ProjectMongo(**project['mongo'])
	)