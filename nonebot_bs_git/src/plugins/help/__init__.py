from nonebot import on_message,on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import MessageEvent, PrivateMessageEvent, GroupMessageEvent



help=on_command("help",rule=to_me(),priority=3,block=True)


@help.handle()
async def help1(bot: Bot, event: Event):
    user_id = str(event.user_id)  # 发送对象
    msg = '''
    默认基准模版为：回复应当口语化，不得超过30个字
    
    /cp 可以使用预设风格（prompt），可选有：可爱/温和/严肃/助手/丰川祥子/汉弗莱，在自定义风格（prompt）存在时预设模版不会触发！重启预设模板需要/dp
    示例：/cp 温和 or /cp 变温和 
    
    /sp 可以设置自定义回复风格（prompt）
    示例：/sp 风趣诙谐、机智俏皮，适时融入幽默元素和轻松的措辞。
    
    /dp可以删除自定义的回复风格（prompt），重新使用预设模板
    示例：/dp
    
    /dc 删除对话记录
    示例：/dc
    
    /cm 更改对话模型，可选参数：deepseek-r1，gpt-4o
    示例：/cm gpt-4o
    
    /vc 更改回复模式（语音/文字），可选参数：on，off
    示例：/vc on
    
    /jm （神秘小功能）
    
    ！目前只支持文本消息，每个人的bot都是独立的，bot有上下文联系的能力但是一句话尽量不要分开发
    '''
    if isinstance(event, GroupMessageEvent):
        await bot.send_group_msg(group_id=event.group_id,
                                 message=msg
                                 )
    elif isinstance(event, PrivateMessageEvent):
        await bot.send_private_msg(user_id=user_id,
                                   message=msg
                                   )

    await help.finish()# 插件都要有这个
