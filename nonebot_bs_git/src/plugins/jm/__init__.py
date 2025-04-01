import random
import os
import jmcomic, os, time, yaml
from PIL import Image
from jmcomic import JmAlbumDetail
from nonebot import on_message,on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from ..deepseek_test.user import FileStorageManager
from nonebot.adapters.onebot.v11 import MessageEvent, PrivateMessageEvent, GroupMessageEvent
from .img2pdf import jpg_to_pdf
import zipfile


jmcomic1=on_command('jm',rule=to_me(),priority=3,block=True)


@jmcomic1.handle()
async def jm(bot: Bot, event: Event):
    storage = FileStorageManager()  # 初始化文件管理器
    user_id = str(event.user_id)  # 发送对象
    text = event.get_plaintext().strip('/jm ')
    option = jmcomic.create_option_by_file("D:/abababa/nonebot-chatgpt/nonebot_bs/src/plugins/jm/option.yml")
    result = jmcomic.download_album(text,option)


    album = result[0]
    folder_name = JmAlbumDetail.get_dirname(album, 'title')








    input_path=r"D:/abababa/nonebot-chatgpt/nonebot_bs/book/{}".format(folder_name)


    output_path = "D:/abababa/nonebot-chatgpt/nonebot_bs/user_sessions/{}".format(user_id)
    pdfname=folder_name
    jpg_to_pdf(input_path, output_path, pdfname)






    pdf= "D:/abababa/nonebot-chatgpt/nonebot_bs/user_sessions/{}/{}.pdf".format(user_id,pdfname)
    import subprocess

    password = "114514"
    file_path = pdf
    zip_path = "{}.7z".format(text)

    command = [r"D:\7-Zip\7z.exe", "a", zip_path, file_path, f"-p{password}", "-mhe=on"]  # -mhe=on 隐藏文件名
    subprocess.run(command)

    print("✅ 文件已加密压缩")
    os.remove(pdf)
    zip=r"D:\abababa\nonebot-chatgpt\nonebot_bs\{}".format(zip_path)
    try:
        await  bot.call_api("upload_group_file",group_id=event.group_id, file=zip, name=zip_path)
        os.remove(zip)
        await jmcomic1.finish("文件上传成功！")
    except :
        await jmcomic1.finish()


