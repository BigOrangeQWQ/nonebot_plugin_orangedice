from typing import Literal
from pydantic import BaseModel, Extra

class Config(BaseModel, extra=Extra.ignore):
    card_file: str = 'card.json'
    log_file: str = 'log.json'
    cache_file: str = 'cache.json'
    save_type: Literal['file','sqlite','SQLITE','FILE'] = 'file'