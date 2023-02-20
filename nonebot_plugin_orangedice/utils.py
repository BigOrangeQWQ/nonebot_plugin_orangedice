from re import findall
from typing import Dict, Self
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent

from .model import DataContainer

class Attribute:
    """属性类"""
    
    def __init__(self, args: str):
        self.attrs = self.get_attrs(args)

    def get_attrs(self, msg: str) -> Dict[str, int]:
        """通过正则处理玩家的车卡数据，获取属性值"""
        find: list[tuple[str, int]] = findall(r"(\D{2,10})(\d{1,3})", msg)
        attrs: Dict[str, int] = {}
        for i in find:
            a, b = i
            attrs[str(a)] = int(b)
        return attrs
    
    def set_attr(self, attr: str, value: int) -> Self:
        """设置属性值"""
        self.attrs[attr] = value
        return self
        
    def extend_attrs(self, attrs: str) -> Self:
        """扩展属性"""
        self.attrs.update(self.get_attrs(attrs))
        return self
        
    def to_str(self) -> str:
        return str(self)

    def get(self, attr: str) -> int:
        """获取属性值"""
        return self.attrs.get(attr, 0)

    def __str__(self, msg: Dict[str, int]) -> str:
        """将玩家的车卡数据转换为字符串"""
        attrs = ""
        for i in msg:
            attrs += f"{i}{msg[i]}\n"
        return attrs

def join_log_msg(data: DataContainer, event: MessageEvent, msg: str):
    """拼接日志消息"""
    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
        if data.is_logging(group_id):
            data.log_add(group_id, msg)
            
def get_name(event: MessageEvent) -> str:
    """获取玩家昵称"""
    a = event.sender.card if event.sender.card else event.sender.nickname
    return a if a else "PL"

def get_msg(event: MessageEvent, index: int) -> str:
    return event.message.extract_plain_text()[index:].replace(' ', '').lower()
    