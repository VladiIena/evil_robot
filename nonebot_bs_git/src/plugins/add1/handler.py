import asyncio

from nonebot.plugin import on_message
from nonebot.adapters import Event, Message, Bot
from nonebot_plugin_session import extract_session, SessionIdType
import time
import random
from .config import config

plus = on_message(priority=config.plus_one_priority, block=False)
msg_dict = {}


def is_equal(msg1: Message, msg2: Message):
    """判断是否相等"""
    if len(msg1) == len(msg2) == 1 and msg1[0].type == msg2[0].type == "image":
        if msg1[0].data.get("file_size") == msg2[0].data.get("file_size"):
            return True
    return msg1 == msg2


@plus.handle()
async def plush_handler(bot: Bot, event: Event):
    global msg_dict

    session = extract_session(bot, event)
    group_id = session.get_id(SessionIdType.GROUP).split("_")[-1]
    if group_id not in config.plus_one_white_list:
        return

    # 获取或创建群组数据
    group_data = msg_dict.get(group_id)
    if not group_data:
        group_data = {"messages": [], "last_repeated": None}
        msg_dict[group_id] = group_data

    messages = group_data["messages"]
    last_repeated = group_data["last_repeated"]

    # 获取当前消息
    msg = event.get_message()

    # 如果当前消息与最近复读内容相同则跳过
    if last_repeated and is_equal(msg, last_repeated):
        return

    # 检查消息连续性
    try:
        if messages and not is_equal(messages[-1], msg):
            messages.clear()
            group_data["last_repeated"] = None  # 遇到不同消息时重置状态
    except IndexError:
        pass

    messages.append(msg)

    # 触发复读并更新状态
    if len(messages) > 1:
        await asyncio.sleep(random.uniform(1,3))
        await plus.send(msg)
        group_data["last_repeated"] = msg.copy()  # 记录最后复读内容
        messages.clear()