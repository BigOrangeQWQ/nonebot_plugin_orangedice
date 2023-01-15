"""
骰点相关，使用onedice协议
"""
from typing import Optional

from .dice import Lexer, Parser

def random(statement: str = '1d100') -> int:
    """
    使用onedice进行骰点

    Args:
        statement (str, optional): [onedice]公式. 默认为 '1d100'.

    Returns:
        int: 骰点后结果
    """
    return int(Parser(Lexer(statement)).parse())



def RD(player_name: Optional[str], statement: str = '1d100', item: str = '', ) -> str:
    """
    进行骰点并返回骰点消息

    Args:
        player_name: Optional[str] 玩家名字
        item: Optional[str] 检定技能
        statement: str = '1d100' [onedice]骰子检定公式

    Return:
        str 检定后信息
    """
    statement = '1d100' if statement == 'd' or statement == '' else statement
    result = random(statement)
    item = f'[{item}]' if item != '' else ''
    return f"{player_name}进行了{item}检定{statement.upper()}={result}"


def RA(player_name: Optional[str], item: str, attr: Optional[int], card: dict[str, int]) -> str:
    """进行检定并返回骰点信息

    Args:
        player_name (str): 玩家名字
        user_id (int): QQ号
        item (str): 检定技能
        attr (int): 技能值

    Returns:
        str: 检定后信息
    """
    attrs: int = card.get(item, 0)
    attrs = attr if attr is not None else attrs
    result: int = random()
    msg = '失败~'
    if (result > 95):
        msg = "大失败~"
    if (result < attrs):
        msg = '成功！'
    if (result < attrs*0.5):
        msg = '困难成功！'
    if (result < attrs*0.2):
        msg = "极限成功！"
    if (result < 5):
        msg = "大成功！！"
    if (result == 0):
        return f'{player_name}没有这个属性'
    return f"{player_name}[{attrs}]进行了[{item}]检定1D100={result} {msg}"
