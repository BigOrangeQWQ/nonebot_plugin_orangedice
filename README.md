<div align="center">

# NoneBot Plugin Orangedice

一个普通的COC骰子插件

</div>

# 使用方法
```
nb plugin install nonebot_plugin_orangedice
```

# 可选配置
``` 
[人物卡/日志/缓存]储存位置
CARD_FILE=card.json
LOG_FILE=log.json
CACHE_FILE=cache.json
[FILE/SQLITE]储存选择
SAVE_TYPE=FILE
注: SQLITE 储存方式尚未制作
```

# 插件指令
.r[公式] 骰点  
.ra[属性] 属性骰点  
.st[属性][数值]/clear 人物卡录入/清除  
.log on/off/upload/clear 日志功能开启/关闭/上传/清除  

公式  
AdB(kq)C(pb)DaE  
b: 奖励骰  
p: 惩罚骰  
k: 取大骰  
q: 取小骰  
a: 取骰池  

### 相关项目

[OneDice](https://github.com/OlivOS-Team/onedice): Today, we stand as one. 
[nonebot_plugin_cocdicer](https://github.com/abrahum/nonebot_plugin_cocdicer): A COC dice plugin for Nonebot2