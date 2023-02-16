# NoneBot Plugin Orangedice

一个普通的COC骰子插件  
真的不点个Star吗？  


## 使用方法
```
pip install nonebot_plugin_orangedice 
nb plugin install nonebot_plugin_orangedice
```
注：0.2.2的版本的储存方式为文件储存  
请因为SQLModel依赖导致冲突的用户下载此版本  
```
nb plugin install nonebot_plugin_orangedice==0.2.2
```
## 可选配置

``` 
#version==0.2.0
CARD_FILE=card.json #人物卡文件位置
LOG_FILE=log.json #日志文件位置
CACHE_FILE=cache.json #缓存文件位置
```

```
#version>=0.2.1
CACHE_FILE=cache.txt # 缓存文件位置
SQLITE_FILE=DICE.db #数据库位置
```

## 插件指令
- .r [公式]         骰点(仅支持OneDice标准内COC骰子格式)
- .ra[属性][数值]   属性骰点[使用数值进行D100检定]
- .ra[属性]         属性骰点[从录卡数据中获取属性]
- .st[属性][数值]   人物卡录入
- .st clear         清除人物卡
- .log on           开启日志记录功能
- .log off          关闭日志记录功能
- .log upload       上传日志至群文件
- .log clear        清除此群日志

## 参考项目(让我学习许多Owo)

[OneDice](https://github.com/OlivOS-Team/onedice): Today, we stand as one.  
[nonebot_plugin_cocdicer](https://github.com/abrahum/nonebot_plugin_cocdicer): A COC dice plugin for Nonebot2
