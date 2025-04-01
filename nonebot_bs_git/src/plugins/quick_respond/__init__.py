import asyncio
import random
from nonebot import on_message, on_command
from nonebot.adapters.onebot.v11 import MessageEvent, PrivateMessageEvent, GroupMessageEvent, Bot, Event
from nonebot.rule import to_me
from .save import JsonDictionary  # 假设这个模块中定义了 JsonDictionary 类，用于读取和写入 JSON 数据

def split_by_ampersand(s: str):
    """
    将字符串按第一个'&'分割成两部分
    返回格式：(左半部分, 右半部分)
    """
    left, sep, right = s.partition("&")
    return left, right




# 使用 on_message 拦截所有消息，并在处理时动态加载最新的 JSON 数据
handle_message = on_message(priority=2,block=False)
@handle_message.handle()
async def handle_message_func(bot: Bot, event: Event):
    # 重新加载最新关键词
    keyword_list = JsonDictionary("my_dict.json").data

    text = event.get_plaintext().strip().lower().replace(" ", "")  # 预处理


    await asyncio.sleep(random.uniform(1, 3))

    try:
        user_id = str(event.user_id)
        msg = None
        for key in keyword_list:
            if key == text:  # 处理大小写 & 空格
                msg = random.choice(keyword_list[key])
                print(keyword_list[key])
                print(f"匹配关键词: [{key}] -> 发送: [{msg}]")
                break  # 只匹配一个关键词

        if msg:
            if isinstance(event, GroupMessageEvent):
                await bot.send_group_msg(group_id=event.group_id, message=msg)
                print("已发送群消息")
            elif isinstance(event, PrivateMessageEvent):
                await bot.send_private_msg(user_id=user_id, message=msg)
                print("已发送私聊消息")
        else:
            print("未匹配到任何关键词")
    except Exception as e:
        print("处理消息时发生错误:", e)
    finally:
        await handle_message.finish()



# 学习新的关键词回复，命令为 "lr"
learn_respond = on_command("lr", rule=to_me(), priority=3, block=True)
@learn_respond.handle()
async def learn_handle(bot: Bot, event: Event):
    json_dict = JsonDictionary('my_dict.json')
    text = event.get_plaintext().strip()
    # 去除命令前缀，例如 "lr " 后面的内容
    text = text[3:].strip(" ")
    user_id = str(event.user_id)

    # 示例：解析格式为 "触发词&回复"
    original_str = text
    original_str=text.replace("＆", "&")
    left_part, right_part = split_by_ampersand(original_str)
    json_dict.add_entry(left_part, right_part)
    msg = "收到！您的触发词为 {}，您的回复为 {}".format(left_part, right_part)
    if isinstance(event, GroupMessageEvent):
        await bot.send_group_msg(group_id=event.group_id, message=msg)
    elif isinstance(event, PrivateMessageEvent):
        await bot.send_private_msg(user_id=user_id, message=msg)
    await learn_respond.finish()

# 删除关键词回复，命令为 "dr"
delete_respond = on_command("dr", rule=to_me(), priority=3, block=True)
@delete_respond.handle()
async def delete_handle(bot: Bot, event: Event):
    json_dict = JsonDictionary('my_dict.json')
    text = event.get_plaintext().strip()
    # 去除命令前缀，例如 "dr " 后面的内容
    text = text[3:].strip(" ")
    user_id = str(event.user_id)

    result = json_dict.remove_entry(text)
    if result == True:
        msg = "收到！触发词 {} 已删除".format(text)
    else:
        msg = "没有找到该触发词，再检查一下吧~"
    if isinstance(event, GroupMessageEvent):
        await bot.send_group_msg(group_id=event.group_id, message=msg)
    elif isinstance(event, PrivateMessageEvent):
        await bot.send_private_msg(user_id=user_id, message=msg)
    await delete_respond.finish()
