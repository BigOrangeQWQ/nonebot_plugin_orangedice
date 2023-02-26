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

- [x] .r  骰点
- [x] .rh 暗骰
- [x] .ra 属性骰点
- [x] .st 录卡
- [x] .li/ti 总结/临时疯狂检定
- [x] .sc sancheck
- [x] .log 日志
- [ ] .nn 昵称修改
- [x] .help 帮助
- [x] .list 疯狂列表
- [x] .coc 车卡
- [x] .en 成长检定
- [x] .dao 导出人物卡

---

### HELP 获取帮助
获取快捷的指令帮助
```
.help

".r#expr(attr) 骰点"
".ra(attr)(value) 属性骰点"
".st(attr value)/clear 人物卡录入/清除"
".log on/off/upload/clear 日志功能开启/关闭/上传/清除"
".sc(success)/(failure) ([san]) 理智检定[不可使用除法]"
".rh 暗骰"
".show 展示人物卡"
".ti/li 临时/永久疯狂检定"
".coc(value) 生成coc人物卡"
".en[attr][expr] 属性成长"
```

### RD 普通骰子
普通的骰点，格式为 [onedice标准](https://github.com/OlivOS-Team/onedice) 内COC的骰子格式

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

### EN 成长
对属性进行成长检定
会自动赋值到人物卡上
```
.en[attritube][expr]

.en力量20
.en理智1d5+2
```

### ST 录人物卡
录入人物属性卡，仅当使用 clear 时重置人物卡
```
.st([attritube][value])/(clear)

.st测试10普通属性100san50..
.st clear
```

### SC 理智检定
进行 **san check** 检定，自动扣除人物卡内的 san。  
支持 **dice expr** 但不支持除法运算符。

```
.sc [success]/[failure] ([san])

.sc 1d8/1d3
```

### TI/LI 疯狂检定
获取一个临时/总结的疯狂发作症状
```
.li #随机获取疯狂发作-总结症状

.ti #随机获取疯狂发作-临时症状
```

### LIST 疯狂表
获取临时/总结疯狂表
```
.list temp/forever
```

### COC 车卡
基于COC7规则的属性随机生成
每次至多生成三个角色
```
.coc[times]

.coc3 #生成三个跑团角色属性卡
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

### DAO 导出角色卡
将角色卡导出来多次使用，与 SHOW 指令的区别为  
SHOW 指令会排除一些重复属性，而 DAO 则会把所有属性全部导出
```
.dao
```

## 相关与参考项目

- [onedice](https://github.com/OlivOS-Team/onedice): Today, we stand as one.
- [nonebot_plugin_cocdicer](https://github.com/abrahum/nonebot_plugin_cocdicer): A COC dice plugin for Nonebot2
- [dice!](https://github.com/Dice-Developer-Team/Dice): QQ Dice Robot For TRPG
- [Blog](https://ruslanspivak.com/lsbasi-part1/)