# 导入必要的库
import json
import os
from uuid import uuid4  # 用于生成唯一用户ID
import requests

class FileStorageManager:
    def __init__(self, storage_dir="user_sessions"):
        # 初始化存储目录
        self.storage_dir = storage_dir
        # 创建存储目录（如果不存在）
        os.makedirs(storage_dir, exist_ok=True)

    def _get_filepath(self, user_id):
        # 为每个用户创建单独的目录
        user_dir = os.path.join(self.storage_dir, user_id)
        os.makedirs(user_dir, exist_ok=True)
        # 在用户目录下存储 conversation.json 文件
        return os.path.join(user_dir, "conversation.json")

    def save_session(self, user_id, new_messages):
        #将所有消息存储为一个 JSON 数组
        path = self._get_filepath(user_id)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        data.extend(new_messages)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


    def print_raw_file(self, user_id):
        #输出用户聊天记录
        path = self._get_filepath(user_id)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            print("文件不存在或数据格式错误")
            return []

            #保存用户设置

    def save_user_settings(self, user_id, settings):

            #将用户的 prompt、偏好等信息存储到 user_settings.json 文件中，
            #settings 为字典格式，如：{"prompt": "...", "preference": "..."}

            path = self._get_settings_filepath(user_id)
            with open(path, 'w', encoding='utf-8') as f:
                    json.dump(settings, f, ensure_ascii=False, indent=2)

        # 加载用户设置

    def load_user_settings(self, user_id):
        path = self._get_settings_filepath(user_id)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            return settings
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _get_settings_filepath(self, user_id):
        # 为每个用户存储 prompt偏好的文件路径
        user_dir = os.path.join(self.storage_dir, user_id)
        os.makedirs(user_dir, exist_ok=True)
        return os.path.join(user_dir, "user_settings.json")

    def delete_conversation(self, user_id):
        #清空指定用户的对话记录
        path = self._get_filepath(user_id)
        try:
            # 用空数组覆盖原有内容
            with open(path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
        except FileNotFoundError:
            # 如果文件不存在则无需处理
            pass

def switch_model(model_type, weights_path):
        base_url = "http://127.0.0.1:9880"

        endpoint = {
            "gpt": "/set_gpt_weights",
            "sovits": "/set_sovits_weights"
        }.get(model_type.lower())

        if not endpoint:
            raise ValueError("Invalid model type. Use 'gpt' or 'sovits'")

        try:
            response = requests.get(
                f"{base_url}{endpoint}",
                params={"weights_path": weights_path}
            )

            if response.status_code == 200:
                print(f"{model_type}模型切换成功！")
            else:
                print(f"切换失败: {response.json()}")

        except Exception as e:
            print(f"请求异常: {str(e)}")
