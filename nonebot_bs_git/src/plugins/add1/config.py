from pydantic import BaseModel, Field
from nonebot import get_plugin_config


class Config(BaseModel):
    """Plugin Config Here"""

    plus_one_priority: int = (Field(5, doc="plus_one 响应优先级"))
    plus_one_white_list: list = (Field(['your user_id here'], doc="plus_one 白名单"))


config = get_plugin_config(Config)
