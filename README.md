<div align="center">

# NoneBot Plugin Orangedice

一个普通的COC骰子插件  
真的不点个Star吗？  
<a href="https://pypi.python.org/pypi/nonebot-plugin-orangedice">
    <img src="https://img.shields.io/pypi/dm/nonebot-plugin-orangedice?style=for-the-badge" alt="Download">
</a>

</div>


## 如何下载
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
#version>=0.3.0
CACHE_FILE=cache.txt # 缓存文件位置
SQLITE_FILE=DICE.db #数据库位置
```

## 指令集

普通的骰点，格式为[onedice标准](https://github.com/OlivOS-Team/onedice)内COC骰子格式

### RD 普通骰子
```
.r[expr]

.r1d100
.r5d100a10
```

### RA 属性掷点
掷出一个 1D100 的骰子进行属性/技能检定  
不提供 value 则在人物卡中获取属性

```
.ra[attritube]([value])

.raStar50
.ra属性60
```

### RH 暗骰
掷出一个 1D100 的骰子
并发送至指令执行者的窗口 
```
.rh
```

### ST 录人物卡
录入人物属性卡，仅当使用 clear 时重置人物卡
```
.st([attritube][value])/(clear)

.st测试10普通属性100san50..
.st clear
```

### SC 理智检定
进行 SanCheck 检定，自动扣除人物卡内的 san。  
支持 **dice expr** 但不支持除法运算符。

```
.sc [success]/[failure] ([san])

.sc 1d8/1d3
```
### LOG 日志记录
记录跑团/群聊日志，此功能需群管理/群主才可开启
```
.log (on)/(off)/(upload)/(clear)

.log on     #开启日志记录功能
.log off    #暂停当前日志记录
.log upload #将日志记录上传至群文件
.log clear  #清空之前的日志
```



## 参考项目(让我学习许多Owo)

[OneDice](https://github.com/OlivOS-Team/onedice): Today, we stand as one.  
[nonebot_plugin_cocdicer](https://github.com/abrahum/nonebot_plugin_cocdicer): A COC dice plugin for Nonebot2
