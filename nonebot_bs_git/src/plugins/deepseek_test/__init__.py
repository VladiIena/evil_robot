import requests
from nonebot.rule import to_me
from openai import OpenAI
from nonebot.adapters.onebot.v11 import MessageEvent, PrivateMessageEvent, GroupMessageEvent, MessageSegment
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event
from openai import AzureOpenAI
from .weather_temperature import date,daytemp,nighttemp,daypower,dayweather,week
from .user import FileStorageManager,switch_model


# 创建消息处理器（当@机器人时触发）
deepseek_handler = on_message(rule=to_me(),priority=4)

#our time line （现实气象）
otl='''今天的日期为{}星期{}，今天天气为{},今天白天气温为{}度，今天晚上气温为{}度，风力为{}级
            #你可以自行决定是否进行参考，'''.format(date,week,dayweather,daytemp,nighttemp,daypower)




@deepseek_handler.handle()
async def handle_deepseek(bot: Bot, event: Event):
    msg = event.get_plaintext().strip()#接收到的讯息
    user_id = str(event.user_id)#发送对象



    if msg=="":
        await deepseek_handler.finish()

    storage = FileStorageManager()  # 初始化文件管理器
    # 尝试加载用户设置
    user_settings = storage.load_user_settings(user_id)
    # 如果没有设置，设置默认值
    if not user_settings:
        user_settings = {
            "prompt": "none",
            "preference": "回复应当口语化，不得超过30个字",
            "model":"deepseek-r1",
            "voice":"off",
            "voice_model":"七海"
        }
        storage.save_user_settings(user_id, user_settings)
   #没有自定义模版就加载预设
    if user_settings.get('prompt','')=='none':
        system_prompt=otl+user_settings.get("preference", "")
    else:
        system_prompt = otl + user_settings.get("prompt", "")
    #模型预设
    model=user_settings.get("model","deepseek-r1")


    # api

    if model=="gpt-4o":
        client = AzureOpenAI(
            azure_endpoint="https://ai-buddha1122117032ai242554509491.openai.azure.com/",
            api_key="Dv9JLSL6JCRhQE8Drp3bCkdwevZyODGbOtNxle2RqQIR0M3y6EQ2JQQJ99BCACHYHv6XJ3w3AAAAACOG0JOr",

            api_version="2024-05-01-preview"
        )
    else:#deepseek-r1
        client = OpenAI(api_key="sk-GcjLgOylwq0zvMJrvIrY3nsE6eedP6LLwxHvJlfnk51V4UCJ",
                    base_url="https://api.lkeap.cloud.tencent.com/v1")

    #api请求模块
    response = client.chat.completions.create(
        model=model,
        messages=(

                [{"role": "system", "content": system_prompt}]#现实联系与用户prompt
                + storage.print_raw_file(user_id)#聊天记录
                + [{"role": "user", "content": msg}]#信息

    ),
        temperature=0.7,
        stream=False
    )

#语音模块
    if(user_settings.get('voice','off'))=='off':
    #不用发语音
    #判断消息是群还是私聊后发送
        if isinstance(event, GroupMessageEvent):
            await bot.send_group_msg(group_id=event.group_id,

            message=response.choices[0].message.content.replace('\n', '').replace('\r', '')

                                     )
        elif isinstance(event, PrivateMessageEvent):
            await bot.send_private_msg(user_id=user_id,

            message=response.choices[0].message.content.replace('\n', '').replace('\r', '')

                                       )
        storage.save_session(user_id, [
        {"role": "user", "content": msg},
        {"role": "assistant", "content":

            response.choices[0].message.content.replace('\n', '').replace('\r', '')}
    ])
        await deepseek_handler.finish()
    #发语音
    elif(user_settings.get('voice','off'))=='on':




        voice_model=user_settings.get("voice_model","七海")
        if(voice_model=="七海"):
            switch_model("gpt", r"D:\abababa\nonebot-chatgpt\GPT-SoVITS-v3lora-20250228\GPT_weights_v2\七海GPT.ckpt")
            switch_model("sovits", r"D:\abababa\nonebot-chatgpt\GPT-SoVITS-v3lora-20250228\SoVITS_weights_v2\七海SoVITS.pth")
            refer_wav_path="D:/abababa/nonebot-chatgpt/数据集/七海/Nana7mi/Nana7mi_1104.wav"
            prompt_text = "不是鲨鱼卫衣那套其实就已经就是卫衣本身就是很宽松的那一套已经有曲线了好吗总有人觉得我是。"
            language="zh"
        elif (voice_model=="东雪莲"):
            switch_model("gpt", r"D:\abababa\nonebot-chatgpt\GPT-SoVITS-v3lora-20250228\GPT_weights_v2\东雪莲GPT.ckpt")
            switch_model("sovits", r"D:\abababa\nonebot-chatgpt\GPT-SoVITS-v3lora-20250228\SoVITS_weights_v2\东雪莲SoVITS.pth")
            refer_wav_path = "D:/abababa/nonebot-chatgpt/数据集/东雪莲/Azuma/Azuma_238.wav"
            prompt_text= "高考差六分没考上他想考得上的学校但是他去了另外一所，不错的大学，等他上完大学之后给再发些什么他就是敷衍的啊啊嗯嗯的回答。"
            language = "zh"
        elif (voice_model=="张维为"):
            switch_model("gpt", r"D:\abababa\nonebot-chatgpt\GPT-SoVITS-v3lora-20250228\GPT_weights_v2\zww-e5.ckpt")
            switch_model("sovits", r"D:\abababa\nonebot-chatgpt\GPT-SoVITS-v3lora-20250228\SoVITS_weights_v2\zww_e8_s112.pth")
            refer_wav_path = r"D:\abababa\nonebot-chatgpt\数据集\zww\1.要给他迎头痛击 张维为老师金句锦集06(Av518956763,P1).mp3_0004628160_0004750400.wav"
            prompt_text= "他如果真的是发现问题的时候，他会及时。"
            language = "zh"
        elif (voice_model=="丰川祥子"):
            switch_model("gpt", r"D:\abababa\nonebot-chatgpt\GPT-SoVITS-v3lora-20250228\GPT_weights_v2\丰川祥子V2-e30.ckpt")
            switch_model("sovits", r"D:\abababa\nonebot-chatgpt\GPT-SoVITS-v3lora-20250228\SoVITS_weights_v2\丰川祥子V2_e150_s1500.pth")
            refer_wav_path = r"D:\abababa\nonebot-chatgpt\数据集\Ave Mujica模型\祥子\sakiko\sakikoV2 (2).wav"
            prompt_text = "私がいなくてもできたでしょ練習したいならすればいいでしょ全員揃わないとできないルールなんてありませんわ"
            language = "ja"
        elif (voice_model=="soyo"):
            switch_model("gpt", r"D:\abababa\nonebot-chatgpt\GPT-SoVITS-v3lora-20250228\GPT_weights_v2\长崎素世V2.1-e30.ckpt")
            switch_model("sovits", r"D:\abababa\nonebot-chatgpt\GPT-SoVITS-v3lora-20250228\SoVITS_weights_v2\长崎素世V2.1_e20_s360.pth")
            refer_wav_path = r"D:\abababa\nonebot-chatgpt\数据集\mygo\素世\soyoV2\soyo (1).wav"
            prompt_text = "さきちゃん、よかった。来てくれて。びしょ濡れじゃない？大丈夫？"
            language = "ja"
        elif (voice_model=="睦子米"):
            switch_model("gpt", r"D:\abababa\nonebot-chatgpt\GPT-SoVITS-v3lora-20250228\GPT_weights_v2\Mutsumi-beta-0103.ckpt")
            switch_model("sovits", r"D:\abababa\nonebot-chatgpt\GPT-SoVITS-v3lora-20250228\SoVITS_weights_v2\Mutsumi-beta-0103.pth")
            refer_wav_path = r"D:\abababa\nonebot-chatgpt\ttsmodel\GPT-SoVITS\model_Mutsumi_beta_0103\model_Mutsumi_beta_0103\サキ、ムシカが壊れたらサキも.wav"
            prompt_text = "サキ、ムシカが壊れたらサキも"
            language = "ja"
        elif (voice_model=="墨提斯"):
            switch_model("gpt", r"D:\abababa\nonebot-chatgpt\GPT-SoVITS-v3lora-20250228\GPT_weights_v2\Mortis_0104_fix_dpo.ckpt")
            switch_model("sovits", r"D:\abababa\nonebot-chatgpt\GPT-SoVITS-v3lora-20250228\SoVITS_weights_v2\Mortis_0104_fix_dpo.pth")
            refer_wav_path = r"D:\abababa\nonebot-chatgpt\ttsmodel\GPT-SoVITS\model_Mortis_0104_fix_dpo\model_Mortis_0104_fix_dpo\むつみちゃんとむつみちゃんの大好きなバンドは守るから.wav"
            prompt_text = "サキ、ムシカが壊れたらサキも"
            language = "ja"
        else :
            switch_model("gpt", r"D:\abababa\nonebot-chatgpt\GPT-SoVITS-v3lora-20250228\GPT_weights_v2\七海GPT.ckpt")
            switch_model("sovits",
                         r"D:\abababa\nonebot-chatgpt\GPT-SoVITS-v3lora-20250228\SoVITS_weights_v2\七海SoVITS.pth")
            refer_wav_path = "D:/abababa/nonebot-chatgpt/数据集/七海/Nana7mi/Nana7mi_1104.wav"
            prompt_text = "不是鲨鱼卫衣那套其实就已经就是卫衣本身就是很宽松的那一套已经有曲线了好吗总有人觉得我是。"
            language = "zh"


        voice_text=response.choices[0].message.content.replace('\n', '').replace('\r', '')
        # 请求参数
        data = {
            "text": voice_text,  # 要转为语音的文本
            "text_lang":language,  # 转语音的文本语言
            "ref_audio_path": refer_wav_path,  # 参考音频文件路径
            "prompt_text": prompt_text,
            # 提供的提示文本
            "prompt_lang": language,  # 提示文本的语言


            "top_k": 15,  # GPT生成的top_k选项
            "top_p": 0.8,  # GPT生成的top_p选项
            "temperature": 0.85,  # GPT生成的温度选项
            "speed": 0.93,  # 语速
            "text_split_method": "cut0"

        }
        # 发起POST请求将文本转换为语音
        url="http://127.0.0.1:9880/tts"
        response_voice = requests.post(url, json=data)

        # 检查请求是否成功
        if response_voice.status_code == 200:
            # 将音频流保存到文件
            with open("user_sessions/{}/output_audio.wav".format(user_id), "wb") as f:
                f.write(response_voice.content)
            print("音频已保存为 output_audio.wav")
        else:
            print("请求失败，错误信息：", response_voice.text)

        voice = MessageSegment.record(file="file://D:/abababa/nonebot-chatgpt/nonebot_bs/user_sessions/{}/output_audio.wav".format(user_id))

        # 根据消息类型发送
        if isinstance(event, GroupMessageEvent):
            await bot.send(event=event, group_id=event.group_id, message=voice)  # 群消息
        elif isinstance(event, PrivateMessageEvent):
            await bot.send(event=event, user_id=event.user_id, message=voice)  # 私聊消息

            # 保存对话记录
        storage.save_session(user_id, [
            {"role": "user", "content": msg},
            {"role": "assistant", "content":

                response.choices[0].message.content.replace('\n', '').replace('\r', '')}
        ])

    await deepseek_handler.finish()