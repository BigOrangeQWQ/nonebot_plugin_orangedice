from pathlib import Path
from re import search
from nonebot import get_driver
from nonebot.matcher import Matcher
from nonebot.plugin import on_startswith, on_message, PluginMetadata
from nonebot.adapters.onebot.v11 import GroupMessageEvent,GROUP_ADMIN, GROUP_OWNER, Bot, MessageEvent

from .model import DataContainer
from .utils import Attribute, join_log_msg, get_name
from .config import Config
from .roll import RA, RD, SC

__plugin_meta__ = PluginMetadata(
    name="orange_dice",
    description="一个普通的COC用骰子",
    usage=".r[公式] 骰点[onedice标准]"
    ".ra[属性] 属性骰点"
    ".st[属性][数值]/clear 人物卡录入/清除"
    ".log on/off/upload/clear 日志功能开启/关闭/上传/清除"
    ".sc[失败损失]/[成功损失] ([理智值]) 理智检定[支持公式，不支持除法运算符]"
    "")

MANAGER = GROUP_ADMIN | GROUP_OWNER
roll = on_startswith(".r", priority=5)  # roll点 阻断
log = on_startswith(".log", permission=MANAGER, priority=5)  # 日志相关指令 阻断
card = on_startswith(".st", priority=5)  # 作成人物卡 阻断
roll_card = on_startswith(".ra", priority=4)  # 人物技能roll点 阻断
sancheck = on_startswith(".sc", priority=5)  #理智检定 阻断

log_msg = on_message(priority=1, block=False)  # 记录日志 不阻断

driver = get_driver()
plugin_config = Config.parse_obj(driver.config)
data = DataContainer()


@roll.handle()
async def roll_handle(matcher: Matcher, event: MessageEvent):
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
    msg = event.message.extract_plain_text()[2:].replace(' ', '').lower()
    name = event.sender.card if event.sender.card else event.sender.nickname
    matches = search(r"\D{1,100}", msg)
    if matches is None:
        result = RD(name, msg)
    else:
        result = RD(name, msg.replace(matches.group(), ''), matches.group())
    
    join_log_msg(data, event, result) # JOIN LOG MSG
    
    await matcher.finish(result)


@roll_card.handle()
async def roll_card_handle(matcher: Matcher, event: MessageEvent):
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
    msg = event.message.extract_plain_text()[3:].replace(' ', '').lower()
    name = event.sender.card if event.sender.card else event.sender.nickname
    # 正则匹配
    match_item = search(r"\D{1,100}", msg)  # 搜索 测试

    if match_item is None:
        await matcher.finish('没有找到需要检定的属性')
    else: 
        match_num = search(r"\d{1,3}", msg.replace(match_item.group(),""))  # 搜索 测试100
        if match_num is not None:
            result = RA(name, match_item.group(),
                        int(match_num.group()), card)
        else:
            result = RA(name, match_item.group(), None, card)
            
    join_log_msg(data, event, result) # JOIN LOG MSG
    
    await matcher.finish(result)


@card.handle()
async def make_card_handle(matcher: Matcher, event: GroupMessageEvent):
    """处理玩家车卡数据

    Example:
        [in].stsan60测试20
        fun(110, 'san60测试20')
    """
    msg = event.message.extract_plain_text()[3:].replace(' ', '').lower()
    user_id = event.user_id
    if msg == 'clear':
        data.delete_card(user_id)
        await matcher.finish("已清除您的数据！")
    attrs = Attribute(data.get_card(user_id).skills).extend_attrs(msg).to_str()
    data.set_card(user_id, attrs)
    await matcher.finish("已录入您的车卡数据！")


@log.handle()
async def log_handle(matcher: Matcher, event: GroupMessageEvent, bot: Bot):
    msg = event.message.extract_plain_text()[4:].strip().lower()
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
    msg = event.message.extract_plain_text()[3:].strip().lower()
    attr = Attribute(data.get_card(event.user_id).skills)
    user_id = event.user_id
    match = search(r"(\S{1,100})\/(\S{1,100})", msg)
    sdice, fdice = "1" , "1d3"
    if match is not None:
        sdice, fdice = match.group(1), match.group(2)
    if attr.get("san") == 0:
        await sancheck.finish("你没有理智属性")
    result, drop_san = SC(get_name(event), attr.get("san"), fdice, sdice)
    data.set_card(user_id, attr.set_attr("san", attr.get("san") - drop_san).to_str())
    
    join_log_msg(data, event, result) # JOIN LOG MSG
    
    await matcher.finish(result)
    


@log_msg.handle()
async def log_msg_handle(event: GroupMessageEvent):
    group_id = event.group_id
    msg = event.message.extract_plain_text()
    name = event.sender.card if event.sender.card else event.sender.nickname
    if data.is_logging(group_id):
        data.log_add(group_id, f'[{name}] {msg}')
