from pydantic import BaseModel

class Config(BaseModel):
    cache_file: str = 'cache.txt'
    sqlite_file: str = 'orange_dice.db'