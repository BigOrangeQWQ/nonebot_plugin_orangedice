<div align="center">

# NoneBot Plugin Orangedice

一个普通的COC骰子插件

</div>

# 使用方法
```
nb plugin install nonebot_plugin_orangedice
```

# 可选配置
[人物卡/日志/缓存]储存位置
``` 
CARD_FILE=card.json
LOG_FILE=log.json
CACHE_FILE=cache.json
SAVE_TYPE=FILE
```

# 插件指令
- .r [公式]         骰点
- 请参考onedice内COC部分
- .ra[属性]         属性骰点  
- .st[属性][数值]   人物卡录入
- .st clear         清除人物卡
- .log on           开启日志记录功能
- .log off          关闭日志记录功能
- .log upload       上传日志至群文件
- .log clear        清除此群日志


### 相关项目

[OneDice](https://github.com/OlivOS-Team/onedice): Today, we stand as one.  
[nonebot_plugin_cocdicer](https://github.com/abrahum/nonebot_plugin_cocdicer): A COC dice plugin for Nonebot2