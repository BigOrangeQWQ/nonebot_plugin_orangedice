# NoneBot Plugin Orangedice

一个普通的COC骰子插件


## 使用方法
```
pip install nonebot_plugin_orangedice 
nb plugin install nonebot_plugin_orangedice
```

请Python3.8下载0.2.0版本  
其他版本停止3.8版本的维护工作  
```
nb plugin install nonebot_plugin_orangedice==0.2.0
```
## 可选配置
[人物卡/日志/缓存]储存位置[0.2.0]
``` 
CARD_FILE=card.json
LOG_FILE=log.json
CACHE_FILE=cache.json
```

缓存储存/数据库位置
```
CACHE_FILE=cache.txt
SQLITE_FILE=DICE.db
```

## 插件指令
- .r [公式]         骰点(仅支持OneDice标准内COC骰子格式)
- .ra[属性]         属性骰点  
- .st[属性][数值]   人物卡录入
- .st clear         清除人物卡
- .log on           开启日志记录功能
- .log off          关闭日志记录功能
- .log upload       上传日志至群文件
- .log clear        清除此群日志

## 参考项目(让我学习许多Owo)

[OneDice](https://github.com/OlivOS-Team/onedice): Today, we stand as one.  
[nonebot_plugin_cocdicer](https://github.com/abrahum/nonebot_plugin_cocdicer): A COC dice plugin for Nonebot2
