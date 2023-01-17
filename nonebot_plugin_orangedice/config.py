from pydantic import BaseModel, Extra

class Config(BaseModel, extra=Extra.ignore):
    cache_file: str = 'cache.json'
    sqlite_file: str = 'orange_dice.db'