from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageEvent, PrivateMessageEvent, GroupMessageEvent, MessageSegment
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from ..deepseek_test.user import FileStorageManager

voice_switch= on_command("vc", rule=to_me(), priority=1, block=True)
change_voice_model=on_command('cvm',rule=to_me(),priority=3,block=True)

@voice_switch.handle()
async def vc(bot: Bot, event: MessageEvent):
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

    keyword_list = {"on": "on", "off": "off"}

    for key in keyword_list:
        if key in text:
            switch = keyword_list[key]
            user_settings["voice"] = switch
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
            await voice_switch.finish()
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
    await voice_switch.finish()



@change_voice_model.handle()
async def vcm(bot: Bot, event: Event):
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

    keyword_list = {"七海": "七海",
                    "东雪莲": "东雪莲",
                    "丰川祥子":"丰川祥子",
                    "睦子米":"睦子米",
                    "张维为":"张维为",
                    "张维维": "张维为",
                    "soyo":"soyo"
                    }

    for key in keyword_list:
        if key in text:
            model=keyword_list[key]
            user_settings["voice_model"] = model
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
            await change_voice_model.finish()
        # 道歉.jpg
    msg = '对不起，没有找到对应的模版试试设定一个吧~'
    if isinstance(event, GroupMessageEvent):
        await bot.send_group_msg(group_id=event.group_id,
                                 message=msg
                                 )
    elif isinstance(event, PrivateMessageEvent):
        await bot.send_private_msg(user_id=user_id,
                                   message=msg
                                   )
    await change_voice_model.finish()