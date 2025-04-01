from nonebot import require,get_bot
from nonebot.adapters.onebot.v11 import MessageEvent, PrivateMessageEvent, GroupMessageEvent
from nonebot.adapters.onebot.v11 import Bot, Event
from .weather_temperature import date,daytemp,nighttemp,daypower,dayweather,week,forecast_weather



require("nonebot_plugin_apscheduler")
group_ids=[643198071,759576098]#白名单
user_ids=[2906119953,745494088]
from nonebot_plugin_apscheduler import scheduler
msg="早上好！！！\n今天日间温度{}，天气{}".format(daytemp,dayweather)
def tem_tip():
    if abs(int(daytemp)-int(nighttemp))>=12:
        tip1='昼夜温差较大，要注意保暖~'
    else:
        tip1=''
    return tip1
def power_tip():
    index = daypower.find('-')
    if index != -1:
        result = daypower[index + 1:]  # 从 '-' 的下一个位置开始截取
        if int(result)>=6:
            tip2='风大，路上小心~'
        else:
            tip2=''
    return tip2
def temp_tip():
    if int(daytemp)>30:
        tip3='很热，穿薄点~'
    elif int(daytemp)<10:
        tip3 = '很冷，穿厚点~'
    else:
        tip3=''
    return tip3
def weather():
    if '雨' in dayweather:
        tip4='今天有雨出门记得带伞~'
    else:
        tip4=''
    return tip4
msg=msg+"\n"+tem_tip()+' '+power_tip()+' '+temp_tip()+' '+weather()
@scheduler.scheduled_job("cron", hour="8",minute='35')
async def run_every_2_hour():
    bot=get_bot()
    for i in group_ids:
        try:
            await bot.send_group_msg(group_id=i, message=msg)
        except Exception as e:
            print(f"发送消息到群 {i} 时出错：{e}")
    for d in user_ids:
        try:
            await bot.send_private_msg(user_id=d, message=msg)
        except Exception as e:
            print(f"发送消息到 {d} 时出错：{e}")
