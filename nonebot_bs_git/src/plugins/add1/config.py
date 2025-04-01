from pydantic import BaseModel, Field
from nonebot import get_plugin_config


class Config(BaseModel):
    """Plugin Config Here"""

    plus_one_priority: int = 1#优先级
    plus_one_white_list: list = ['123456','456789']#白名单


config = get_plugin_config(Config)
