from re import findall
from typing import Dict, Tuple
from typing_extensions import Self
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent

from .model import DataContainer


#将录卡的属性全部统一为第一个值
#而后导出卡片时生成多个属性
same_attr_list: Dict[str, Tuple] = {
    "力量": ("str",),
    "体质": ("con",),
    "体型": ("siz",),
    "敏捷":("dex",),
    "外貌":("app",),
    "智力":("int","灵感"),
    "意志":("pow",),
    "教育":("edu",),
    "幸运":("luc","运气",),
    "理智":("san","理智值",),
    "魔法":("mp",),
    "体力":("hp",),
    "信誉":("信用评级",),
    "计算机使用":("计算机","电脑"),
    "克苏鲁神话":("克苏鲁","cm")
}


class Attribute:
    """属性类"""

    def __init__(self, args: str):
        self.attrs = self.get_attrs(args)
        self.same = self.same_list()

    def get_attrs(self, msg: str) -> Dict[str, int]:
        """通过正则处理玩家的车卡数据，获取属性值"""
        find: list[tuple[str, int]] = findall(r"(\D{2,10})(\d{1,3})", msg)
        attrs: Dict[str, int] = {}
        for i in find:
            a, b = i
            if not self.is_alias(a):
                attrs[str(a)] = int(b)
        return attrs
    
    def is_alias(self, attr: str) -> bool:
        """判定属性是否为别名"""
        for v in same_attr_list.values():
            if attr in v:
                return True
        return False

    def set(self, attr: str, value: int) -> Self:
        """设置属性值"""
        self.attrs[attr] = value
        return self
    
    def add(self, attr: str, value: int) -> Self:
        """增加属性值"""
        if self.get(attr)+value > 100:
            self.set(attr, 100)
        else:
            self.set(attr, self.get(attr)+value)
        return self

    def extend_attrs(self, attrs: str) -> Self:
        """扩展属性"""
        self.attrs.update(self.get_attrs(attrs))
        return self

    def get(self, attr: str) -> int:
        """获取属性值"""
        # if attr in self.same:
        #     for k,v in same_attr_list.items():
        #         if attr in v:
        #             return self.attrs.get(k, 0)
        if self.is_alias(attr):
            for k,v in same_attr_list.items():
                if attr in v:
                    return self.attrs.get(k, 0)
        return self.attrs.get(attr, 0)
    
    def dao(self) -> str:
        """导出属性卡"""
        c = self.__str__()
        for k,v in same_attr_list.items():
            if self.get(k) > 0:
                for i in v:
                    c+=f"{i}{self.get(k)}"
        return c
    
    def same_list(self):
        """将同义词并做一个集合"""
        same = set()
        for k,v in same_attr_list.items():
            same.add(k)
            same.update(v)
        return same
    
    def set_back(self):
        ...

    def to_str(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        """将玩家的车卡数据转换为字符串"""
        attrs = ""
        for k,v in self.attrs.items():
            attrs += f"{k}{v}"
        return attrs


def join_log_msg(data: DataContainer, event: MessageEvent, msg: str):
    """拼接日志消息"""
    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
        if data.is_logging(group_id):
            data.log_add(group_id, msg)


def get_name(event: MessageEvent) -> str:
    """获取玩家昵称"""
    return event.sender.card if event.sender.card else (event.sender.nickname if event.sender.nickname else "PL")


def get_msg(event: MessageEvent, index: int) -> str:
    """获取消息"""
    return event.message.extract_plain_text()[index:].replace(' ', '').lower()
