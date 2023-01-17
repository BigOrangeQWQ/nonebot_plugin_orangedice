
from os.path import exists
from json import dump, load
from re import findall
from nonebot import get_driver
from typing import Dict

from .config import Config

plugin_config = Config.parse_obj(get_driver().config)


class Card:

    def __init__(self) -> None:
        self._cache_player_: dict[str, Dict[str, int]] = {}
        """
        {"user_id": {"san": 50 ...}}
        """

    def get_card(self, user_id: int) -> Dict[str, int]:
        """获取车卡数据

        Args:
            user_id (int): QQ号

        Returns:
            dict[str,int]: 属性及数据
        """
        return self._cache_player_.get(str(user_id), {})

    def set_card(self, user_id: int, attr: str):
        """
        解析并储存玩家数据

        Args:
            user_id (int): QQ号
            attr (str): 未处理的属性字符串  
        """
        find: list[tuple[str, int]] = findall(r"(\D{2,4})(\d{1,3})", attr)
        attrs: dict[str, int] = {}
        for i in find:
            a, b = i
            attrs[str(a)] = int(b)
        self._cache_player_[str(user_id)] = attrs

    def clear_card(self, user_id: int):
        self._cache_player_[str(user_id)].clear()

    def save_json(self):
        """
        储存玩家数据
        """
        with open(plugin_config.card_file, 'w', encoding='utf-8') as f:
            dump(self._cache_player_, open(
                plugin_config.card_file, 'w', encoding='utf-8'))

    def read_json(self):
        if exists(plugin_config.card_file):
            with open(plugin_config.card_file, 'r', encoding='utf-8') as f:
                self._cache_player_: Dict[str, Dict[str, int]] = load(f)
        else:
            self.save_json()

    # TODO
    def save_sqlite(self):
        ...

    def read_sqlite(self):
        ...
