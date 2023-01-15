from os.path import exists
from json import load, dump
from pathlib import Path
from typing import TypedDict
from nonebot import get_driver

from .config import Config

LogType = TypedDict('Log', {'msg': list[str], 'log': bool})
plugin_config = Config.parse_obj(get_driver().config)

class Log:

    def __init__(self) -> None:
        self._cache_log_: dict[str, LogType] = {}
        """
        {"group_id": {'msgs': ['msg'], 'log': bool}}

        (nickname: msg)
        nickname: msg
        """

    def save_json(self):
        """
        使用json文件储存数据
        """
        with open(plugin_config.log_file, 'w', encoding='utf-8') as f:
            dump(self._cache_log_, f)

    def read_json(self):
        """
        读取json文件数据
        若文件不存在则创建
        """
        if exists(plugin_config.log_file):
            with open(plugin_config.log_file, 'r', encoding='utf-8') as f:
                self._cache_log_ = load(f)
        else:
            self.save_json()

    def is_loging(self, group_id: int) -> bool:
        """
        检测某群是否正在记录日志

        Args:
            group_id (int): 群号

        Returns:
            bool: 记录中返回True
        """
        return self._cache_log_.get(str(group_id),{}).get('log', False)

    def log_on(self, group_id: int):
        """
        开启某群的日志记录功能

        Args:
            group_id (int): 群号
        """
        try:
            self._cache_log_[str(group_id)]['log'] = True
        except KeyError:
            self._cache_log_[str(group_id)] = {'msg': ['初始化'], 'log': True}

    def log_off(self, group_id: int):
        """
        关闭某群的日志记录功能

        Args:
            group_id (int): 群号
        """
        try:
            self._cache_log_[str(group_id)]['log'] = False
        except KeyError:
            self._cache_log_[str(group_id)] = {'msg': ['初始化'], 'log': False}

    def log_add_message(self, group_id: int, message: str):
        """
        为日志增加消息

        Args:
            message (str): 需增加的消息
        """
        self._cache_log_[str(group_id)]['msg'].append(message)
    
    def log_clear(self, group_id: int):
        """
        清除某群的所有日志

        Args:
            group_id (int): 群号
        """
        self._cache_log_[str(group_id)]['msg'].clear()

    def log_upload(self, group_id: int) -> str:
        """
        创建文件放置指定群日志，

        Args:
            group_id (int): QQ号

        Return:
            str: 文件路径
        """
        with open(plugin_config.cache_file, 'w', encoding='utf-8') as f:
            for i in self._cache_log_[str(group_id)]['msg']:
                f.write(f"{i}\n")
        return Path(plugin_config.cache_file).absolute().as_posix()
        
