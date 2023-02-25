from ast import MatchSequence
from pathlib import Path
from re import search
from random import choice
from nonebot import get_driver
from nonebot.params import Depends
from nonebot.matcher import Matcher
from nonebot.plugin import on_startswith, on_message, PluginMetadata
from nonebot.adapters.onebot.v11 import GroupMessageEvent, GROUP_ADMIN, GROUP_OWNER, MessageEvent, Bot

from .model import DataContainer
from .utils import Attribute, get_msg, join_log_msg, get_name
from .message import fear_list, crazy_forever, crazy_list, crazy_temp
from .config import Config
from .roll import COC, RA, RD, SC, random

__plugin_meta__ = PluginMetadata(
    name="orange_dice",
    description="一个普通的COC用骰子",
    usage=".r[expr]([attr]) 骰点"
    ".ra[attr]([value]) 属性骰点"
    ".st[attr][value]/clear 人物卡录入/清除"
    ".log (on/off/upload/clear) 日志功能开启/关闭/上传/清除"
    ".sc[success]/[failure] ([san]) 理智检定[不可使用除法]"
    ".rh 暗骰"
    ".show 展示人物卡"
    ".ti/li 临时/永久疯狂检定"
    ".coc([value]) 生成coc人物卡"
    ".en[attr][expr] 属性成长"
)

MANAGER = GROUP_ADMIN | GROUP_OWNER


# -> 阻断响应器
log = on_startswith(".log", permission=MANAGER, priority=5)  # 日志相关指令
help = on_startswith(".help", priority=5)  # 帮助
#骰点相关
roll = on_startswith(".r", priority=5)  # roll点
roll_card = on_startswith(".ra", priority=4)  # 人物技能roll点
sancheck = on_startswith(".sc", priority=5)  # 理智检定
roll_p = on_startswith(".rh", priority=4)  # 暗骰
#人物卡相关
card = on_startswith(".st", priority=5)  # 人物卡录入
show = on_startswith(".show", priority=5)  # 展示人物卡
dao = on_startswith(".dao" ,priority=5) #人物卡导出
coc_create = on_startswith(".coc", priority=5)  # 生成coc人物卡
en = on_startswith(".en", priority=5)  # 属性成长
#疯狂检定相关
insane_list = on_startswith(".list", priority=5)  # 获取所有疯狂表
temp_insane = on_startswith(".ti", priority=5)  # 临时疯狂表
forever_insane = on_startswith(".li", priority=5)  # 永久疯狂表

# -> 非阻断响应器
log_msg = on_message(priority=1, block=False)  # 记录日志

# -> 数据相关
driver = get_driver()
plugin_config = Config.parse_obj(driver.config)
data = DataContainer()


@roll.handle()
async def roll_handle(matcher: Matcher, event: MessageEvent, name: str = Depends(get_name)):
    """
    处理骰点检定

    Example:
        [in].rd测试
        RD('测试','PlayerName','1D100')
        [out]进行了[测试]检定1D100=result

        [in].r
        RD('PlayerName',None, '')
        [out]进行了检定1D100=result

        [in].rd测试50
        [error out]进行了检定1D100=0
    """
    msg: str = get_msg(event, 2)
    matches = search(
        r"(\d|[d|a|k|q|p|+|\-|\*|\/|\(|\)|x]){1,1000}", msg)  # 匹配骰子公式
    if matches is None:

        result = RD(name, msg)
    else:
        result = RD(name, matches.group(), msg.replace(matches.group(), ""))

    join_log_msg(data, event, result)  # JOIN LOG MSG

    await matcher.finish(result)


@roll_card.handle()
async def roll_card_handle(matcher: Matcher, event: MessageEvent, name: str = Depends(get_name)):
    """处理玩家属性骰点

    Example:
        [in].ra测试
        RA('name', 110, '测试')
        [out]name[attr]进行了[测试]检定1D100=result [msg]

        [in].ra测试100
        RA('name', 110, '测试', 100)
        [out]name[100]进行了[测试]检定1D100=result [msg]
    """

    user_id = event.user_id
    card = Attribute(data.get_card(user_id).skills).attrs
    msg = get_msg(event, 3)
    # 正则匹配
    match_item = search(r"\D{1,100}", msg)  # 搜索 测试

    if match_item is None:
        await matcher.finish('没有找到需要检定的属性')
    else:
        match_num = search(r"\d{1,3}", msg.replace(
            match_item.group(), ""))  # 搜索 测试100
        if match_num is not None:
            result = RA(name, match_item.group(),
                        int(match_num.group()), card)
        else:
            result = RA(name, match_item.group(), None, card)

    join_log_msg(data, event, result)  # JOIN LOG MSG

    await matcher.finish(result)


@card.handle()
async def make_card_handle(matcher: Matcher, event: GroupMessageEvent):
    """处理玩家车卡数据

    Example:
        [in].stsan60测试20
        fun(110, 'san60测试20')
    """
    msg = get_msg(event, 3)
    user_id = event.user_id
    if msg == 'clear':
        data.delete_card(user_id)
        await matcher.finish("已清除您的数据！")
    attrs = Attribute(data.get_card(user_id).skills).extend_attrs(msg).to_str()
    data.set_card(user_id, attrs)
    await matcher.finish("已录入您的车卡数据！")


@log.handle()
async def log_handle(matcher: Matcher, event: GroupMessageEvent, bot: Bot):
    """
    日志相关指令
    """
    msg = get_msg(event, 4)
    group_id = event.group_id
    if msg == 'on':
        data.open_log(group_id)
        await matcher.finish("已开启记录日志")
    if msg == 'off':
        data.close_log(group_id)
        await matcher.finish("已关闭记录日志")
    if msg == 'upload':
        with open(plugin_config.cache_file, 'w', encoding='utf-8') as f:
            for i in data.get_log(group_id).msg:
                f.write(f"{i}\n")
        file = Path(plugin_config.cache_file).absolute().as_posix()
        try:
            await bot.upload_group_file(group_id=group_id, file=file, name=f'logs-{event.message_id}.txt')
        except:
            await matcher.finish("上传群文件失败，请检查橘子的权限。")
        await matcher.finish("已上传至群文件")
    if msg == 'clear':
        data.delete_log(group_id)
        await matcher.finish("已清除此群之前的所有日志信息")
    else:
        await matcher.finish("不清楚你想干什么~")


@sancheck.handle()
async def sancheck_handle(matcher: Matcher, event: MessageEvent):
    """
    处理理智检定
    """
    msg = get_msg(event, 3)
    attr = Attribute(data.get_card(event.user_id).skills)
    user_id = event.user_id
    match = search(r"(\S{1,100})\/(\S{1,100})", msg)
    sdice, fdice = "1", "1d3"
    if match is not None:
        sdice, fdice = match.group(1), match.group(2)
    if attr.get("san") == 0:
        await sancheck.finish("你没有理智属性")
    result, drop_san = SC(get_name(event), attr.get("san"), fdice, sdice)
    data.set_card(user_id, attr.set(
        "san", attr.get("san") - drop_san).to_str())

    join_log_msg(data, event, result)  # JOIN LOG MSG

    await matcher.finish(result)


@log_msg.handle()
async def log_msg_handle(event: GroupMessageEvent):
    """
    记录群聊信息
    """
    group_id = event.group_id
    msg = event.message.extract_plain_text()
    name = get_name(event)
    if data.is_logging(group_id):
        data.log_add(group_id, f'[{name}] {msg}')


@roll_p.handle()
async def private_roll_handle(matcher: Matcher, event: GroupMessageEvent, bot: Bot):
    """
    1D100暗骰指令
    """
    msg = get_msg(event, 3)
    name = get_name(event)
    result = RD(name, msg)

    await bot.send_private_msg(user_id=event.user_id, message=result)
    join_log_msg(data, event, result)

    await matcher.finish(f"{name} 进行了一次暗骰~")


@show.handle()
async def show_card_handle(event: MessageEvent):
    """
    展示人物卡数据
    """
    user_id = event.user_id
    card = Attribute(data.get_card(user_id).skills).to_str()
    msg = f"你的车卡数据如下：\n{card}"
    await show.finish(msg)


@insane_list.handle()
async def show_insane_list_handle(event: MessageEvent, matcher: Matcher):
    """
    提供疯狂表
    """
    need = get_msg(event, 5)
    if need == 'temp':
        await matcher.finish("\n".join(crazy_temp))
    if need == 'forever':
        await matcher.finish("\n".join(crazy_forever))


@temp_insane.handle()
async def get_temp_insane(event: MessageEvent, matcher: Matcher):
    """
    临时疯狂检定
    """
    result = random("1d10")
    if result == 9: 
        msg = f"9) 恐惧:{choice(fear_list)},持续{random('1d10')}轮"
    elif result == 10:
        msg = f"10) 躁狂:{choice(crazy_list)},持续{random('1d10')}轮"
    else:
        msg = crazy_temp[result-1]
    await matcher.finish(msg.replace("1D10", str(random("1d10"))))


@forever_insane.handle()
async def get_forever_insane(event: MessageEvent, matcher: Matcher):
    """
    总结疯狂检定
    """
    result = random("1d10")
    if result == 9:
        msg = f"9) 恐惧:{choice(fear_list)}"
    elif result == 10:
        msg = f"10) 躁狂:{choice(crazy_list)}"
    else:
        msg = crazy_forever[result-1]
    await matcher.finish(msg.replace("1D10", str(random("1d10"))))


@coc_create.handle()
async def create_coc_role(event: MessageEvent, matcher: Matcher):
    """
    创建人物卡
    """
    value = int(get_msg(event, 4))
    if value > 3:
        value = 3
    await matcher.finish("\n".join([COC() for i in range(value)]))


@help.handle()
async def help_send(event: MessageEvent, matcher: Matcher):
    """
    帮助信息
    """
    await matcher.finish(__plugin_meta__.usage)

@dao.handle()
async def dao_send(event: MessageEvent, matcher: Matcher):
    """
    导出角色卡
    """
    await matcher.finish(Attribute(data.get_card(event.user_id).skills).dao())
    
@en.handle()
async def improve_self(event: MessageEvent, matcher: Matcher,name: str = Depends(get_name)):
    """
    自我提升
    """
    msg = get_msg(event, 3)
    matches = search(
        r"(\d|[d|a|k|q|p|+|\-|\*|\/|\(|\)|x]){1,1000}", msg)
    if matches:
        item = msg.replace(matches.group(), "")
        result = random(matches.group()) 
        user_id = event.user_id
        data.set_card(user_id, Attribute(data.get_card(user_id).skills).add(item, result).to_str())
        await matcher.finish(f"{name} 对 {item} 理解提升了 {result} !")