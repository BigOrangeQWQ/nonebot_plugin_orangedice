from pydantic import BaseModel, Extra

class Config(BaseModel, extra=Extra.ignore):
    cache_file: str = 'cache.txt'
    sqlite_file: str = 'orange_dice.db'