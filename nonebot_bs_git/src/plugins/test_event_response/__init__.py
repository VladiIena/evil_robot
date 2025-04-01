import nonebot
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.typing import T_State
test1 = on_command("测试") # 这个test1就是个变量名字
@test1.handle()
async def test1_handle(bot: Bot, event: Event, state: T_State):
  nonebot.logger.info("插件执行一次。")
  await test1.finish() # 插件都要有这个