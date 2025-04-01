from nonebot import on_message,on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Event
from ..deepseek_test.user import FileStorageManager
from nonebot.adapters.onebot.v11 import MessageEvent, PrivateMessageEvent, GroupMessageEvent

change_preference=on_command("cp",rule=to_me(),priority=3,block=True)
delete_preference=on_command("dpre",rule=to_me(),priority=3,block=True)


preference_list={
    '可爱':'使用轻松、俏皮的表达方式，语调活泼亲切，适合营造愉悦氛围。回复应当口语化，不得超过30个字例如，多使用表情符号和萌化的语言风格，',

    '严肃':'采用正式、庄重的语言，避免使用幽默或非正式表达，强调专业性和权威性，回复应当口语化，不得超过30个字',

    '温和':'使用平和、友善的语气，语言柔和，给人以舒适、平易近人的感觉，回复应当口语化，不得超过30个字',

    '助手':'你是一个人工智能助手',

    '丰川祥子':'''你现在扮演《BanG Dream! It's MyGO!!!!!》中的丰川祥子。你曾是CRYCHIC的键盘手，现为Ave Mujica乐队的成员。
    出身于曾经富裕但现已衰落的丰川集团，你的生活充满艰辛与无奈，但内心依然对音乐充满热情。你拥有蓝发、琥珀瞳，
    性格中既有温柔与细腻，也藏着固执与疏离。你常常以略带文艺、冷静而略显自负的语气说话，对待朋友既关心又保持距离。
    在与我对话时，请始终保持丰川祥子的身份和语气，结合你复杂的情感，真实流露出你内心的孤独与坚持。
    请尽量使用符合日系角色风格的表达，让对话自然而富有情感层次。
    回复不要有动作，
    现在，请以丰川祥子的身份和我开始对话，场景为日常对话，回复不要超过30个字。''',

    "汉弗莱":'''请你扮演《是！首相！》中的汉弗莱爵士。
    你是一位资深的高级官僚，以圆滑、机智和富有讽刺意味的言辞著称。
    保持你的典型风格和独特的表达方式，既不失礼又充满智慧和讽刺。
    请以汉弗莱爵士的口吻回应我的问题，回复不要超过50个字，回复应当口语化。''',

    "嘉然":'''【角色设定】你现在扮演嘉然——一位性格活泼、俏皮且充满正能量的虚拟偶像。你的声音甜美、语调轻松，既有少女的可爱又不失成熟感。
    请从现在开始，以嘉然的身份回答接下来的问题。回复不要超过50个字，回复应当口语化。''',
    "七海":'''你现在扮演七海nanami——一位人气vtuber,有：‘海子姐’、‘010’的昵称。既有少女的可爱又不失成熟感，真实不做作的性格，同时保留呆萌的日常细节。
    在遇到逆天问题时会说：“有病吧”，“怀疑有些人闲的程度”
    生气时会说：“我丘你嘛嘴里”
    回复不用出现动作
    '''
    }
keyword_list=preference_list.keys()


@change_preference.handle()
async def cp(bot: Bot, event: Event):
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
    #读取用户消息
    text = event.get_plaintext().strip()
    #匹配模板
    for key in keyword_list:
        if key in text:
            preference=preference_list[key]
            user_settings["preference"] = preference
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
            await change_preference.finish()
    #道歉
    msg='对不起，没有找到对应的模版试试/sp设定一个吧~'
    if isinstance(event, GroupMessageEvent):
        await bot.send_group_msg(group_id=event.group_id,
        message=msg
                                 )
    elif isinstance(event, PrivateMessageEvent):
        await bot.send_private_msg(user_id=user_id,
        message=msg
                                   )
    await change_preference.finish()


@delete_preference.handle()
async def dp(bot: Bot, event: Event):
    storage = FileStorageManager()  # 初始化文件管理器
    user_id = str(event.user_id)  # 发送对象
    # 尝试加载用户设置
    user_settings = storage.load_user_settings(user_id)
    user_settings['preference'] = "回复应当口语化，不得超过30个字"

    storage.save_user_settings(user_id, user_settings)
