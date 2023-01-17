# from os.path import exists
# from json import dump, load
# from re import findall
# from nonebot import get_driver

# from nonebot_plugin_orangedice.model import DataContainer, Player

# from .config import Config

# plugin_config = Config.parse_obj(get_driver().config)


# class Card:

#     def __init__(self) -> None:
#         self.data = DataContainer()
#         """
#         {"user_id": {"san": 50 ...}}
#         """

#     def get_card(self, user_id: int) -> dict[str, int]:
#         """获取车卡数据

#         Args:
#             user_id (int): QQ号

#         Returns:
#             dict[str,int]: 属性及数据
#         """
#         return self.data.get_card(user_id).skills

#     def set_card(self, user_id: int, attr: str):
#         """
#         解析并储存玩家数据

#         Args:
#             user_id (int): QQ号
#             attr (str): 未处理的属性字符串  
#         """
#         find: list[tuple[str, int]] = findall(r"(\D{2,4})(\d{1,3})", attr)
#         attrs: dict[str, int] = {}
#         for i in find:
#             a, b = i
#             attrs[str(a)] = int(b)
#         self.data.set_card(user_id, attrs)

#     def clear_card(self, user_id: int):
#         self.data.delete_card(user_id)