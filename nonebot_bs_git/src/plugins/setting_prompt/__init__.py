from nonebot import on_message,on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Event
from ..deepseek_test.user import FileStorageManager
from nonebot.adapters.onebot.v11 import MessageEvent, PrivateMessageEvent, GroupMessageEvent

setting_prompt=on_command("sp",rule=to_me(),priority=3,block=True)
delete_prompt=on_command("dp",rule=to_me(),priority=3,block=True)
delete_conversation=on_command('dc',rule=to_me(),priority=3,block=True)
change_model=on_command('cm',rule=to_me(),priority=3,block=True)

@setting_prompt.handle()
async def sp(bot: Bot, event: Event):
    storage = FileStorageManager()  # 初始化文件管理器
    user_id = str(event.user_id)  # 发送对象
    # 尝试加载用户设置
    user_settings = storage.load_user_settings(user_id)
    # 如果没有设置，设置默认值
    if not user_settings:
        user_settings = {
            "prompt": "none",
            "preference": "回复应当口语化，不得超过30个字",
            "model": "deepseek-r1",
            "voice": "off",
            "voice_model": "七海"
        }
        storage.save_user_settings(user_id, user_settings)
    # 读取用户消息
    text = event.get_plaintext().strip()
    text=text[3:]
    #更改prompt字段
    user_settings["prompt"] = text
    #保存
    storage.save_user_settings(user_id, user_settings)

    msg = 'ok~'

    if isinstance(event, GroupMessageEvent):
        await bot.send_group_msg(group_id=event.group_id,
                                 message=msg
                                 )
    elif isinstance(event, PrivateMessageEvent):
        await bot.send_private_msg(user_id=user_id,
                                   message=msg
                                   )
    await setting_prompt.finish()

@delete_prompt.handle()
async def dp(bot: Bot, event: Event):
    storage = FileStorageManager()  # 初始化文件管理器
    user_id = str(event.user_id)  # 发送对象
    # 尝试加载用户设置
    user_settings = storage.load_user_settings(user_id)
    #覆盖prompt
    user_settings['prompt'] = "none"
    storage.save_user_settings(user_id, user_settings)

    msg = 'ok~'

    if isinstance(event, GroupMessageEvent):
        await bot.send_group_msg(group_id=event.group_id,
                                 message=msg
                                 )
    elif isinstance(event, PrivateMessageEvent):
        await bot.send_private_msg(user_id=user_id,
                                   message=msg
                                   )
    await delete_prompt.finish()

@delete_conversation.handle()
async def dc(bot: Bot, event: Event):
    storage = FileStorageManager()  # 初始化文件管理器
    user_id = str(event.user_id)  # 发送对象
    # 尝试加载用户设置
    user_settings = storage.load_user_settings(user_id)

    # 清空对话记录
    storage.delete_conversation(user_id)


    msg = 'ok~'

    if isinstance(event, GroupMessageEvent):
        await bot.send_group_msg(group_id=event.group_id,
                                 message=msg
                                 )
    elif isinstance(event, PrivateMessageEvent):
        await bot.send_private_msg(user_id=user_id,
                                   message=msg
                                   )
    await delete_conversation.finish()

@change_model.handle()
async def cm(bot: Bot, event: Event):
    storage = FileStorageManager()  # 初始化文件管理器
    user_id = str(event.user_id)  # 发送对象
    # 尝试加载用户设置
    user_settings = storage.load_user_settings(user_id)
    # 如果没有设置，设置默认值
    if not user_settings:
        user_settings = {
            "prompt": "none",
            "preference": "回复应当口语化，不得超过30个字",
            "model": "deepseek-r1",
            "voice":"off",
            "voice_model": "七海"
        }
        storage.save_user_settings(user_id, user_settings)
    # 读取用户消息
    text = event.get_plaintext().strip()

    keyword_list={"deepseek-r1":"deepseek-r1","gpt-4o":"gpt-4o"}

    for key in keyword_list:
        if key in text:
            model=keyword_list[key]
            user_settings["model"] = model
            storage.save_user_settings(user_id, user_settings)
            msg='ok~'
            if isinstance(event, GroupMessageEvent):
                await bot.send_group_msg(group_id=event.group_id,
                                         message=msg
                                         )
            elif isinstance(event, PrivateMessageEvent):
                await bot.send_private_msg(user_id=user_id,
                                           message=msg
                                           )
            await change_model.finish()
        # 道歉.jpg
    msg = '对不起，没有找到对应的模版试试/sp设定一个吧~'
    if isinstance(event, GroupMessageEvent):
        await bot.send_group_msg(group_id=event.group_id,
                                 message=msg
                                 )
    elif isinstance(event, PrivateMessageEvent):
        await bot.send_private_msg(user_id=user_id,
                                   message=msg
                                   )
    await change_model.finish()