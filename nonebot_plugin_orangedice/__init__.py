from pathlib import Path
from re import search
from nonebot import get_driver
from nonebot.matcher import Matcher
from nonebot.plugin import on_startswith, on_message, PluginMetadata
from nonebot.adapters.onebot.v11 import GroupMessageEvent, GROUP_ADMIN, GROUP_OWNER, Bot

from nonebot_plugin_orangedice.model import DataContainer
from nonebot_plugin_orangedice.utils import get_attrs

from .config import Config
from .roll import RA, RD

__plugin_meta__ = PluginMetadata(
    name="orange_dice",
    description="一个普通的COC用骰子",
    usage=".r[公式] 骰点[onedice标准]"
    ".ra[属性] 属性骰点"
    ".st[属性][数值]/clear 人物卡录入/清除"
    ".log on/off/upload/clear 日志功能开启/关闭/上传/清除")

MANAGER = GROUP_ADMIN | GROUP_OWNER
roll = on_startswith(".r", priority=5)  # roll点
log = on_startswith(".log", permission=MANAGER, priority=5)  # 日志相关指令
log_msg = on_message(priority=6)  # 记录日志
card = on_startswith(".st", priority=5)  # 作成人物卡
roll_card = on_startswith(".ra", priority=4)  # 人物技能roll点

driver = get_driver()
plugin_config = Config.parse_obj(driver.config)
data = DataContainer()


@roll.handle()
async def roll_handle(matcher: Matcher, event: GroupMessageEvent):
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
    matches = search(r"[\u4e00-\u9fa5]{1,100}", msg)
    group_id = event.group_id
    if matches is None:
        result = RD(name, msg)
    else:
        result = RD(name, msg.replace(matches.group(), ''), matches.group())
    # JOIN LOG MSG
    if data.is_logging(group_id):
        data.log_add(group_id, result)
    await matcher.finish(result)


@roll_card.handle()
async def roll_card_handle(matcher: Matcher, event: GroupMessageEvent):
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
    group_id = event.group_id
    card = get_attrs(data.get_card(user_id).skills)
    msg = event.message.extract_plain_text()[3:].replace(' ', '').lower()
    name = event.sender.card if event.sender.card else event.sender.nickname
    # 正则匹配
    match_item = search(r"[\u4e00-\u9fa5]{1,100}", msg)  # 搜索 测试
    match_num = search(r"\d{1,3}", msg)  # 搜索 测试100

    if match_item is None:
        await matcher.finish('没有找到需要检定的属性')
    if match_num is not None:
        result = RA(name, match_item.group(),
                    int(match_num.group()), card)
    else:
        result = RA(name, match_item.group(), None, card)
    # JOIN LOG MSG
    if data.is_logging(group_id):
        data.log_add(group_id, result)
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
    data.set_card(user_id, msg)
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


@log_msg.handle()
async def log_msg_handle(event: GroupMessageEvent):
    group_id = event.group_id
    msg = event.message.extract_plain_text()
    name = event.sender.card if event.sender.card else event.sender.nickname
    if data.is_logging(group_id):
        data.log_add(group_id, f'[{name}] {msg}')
