import json
import os

class JsonDictionary:
    def __init__(self, filename):
        current_dir = os.path.dirname(__file__)
        self.filename = os.path.join(current_dir, filename)
        self.data = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            # 转换旧数据：将所有值转换为列表形式
            #for key in self.data:
                #if not isinstance(self.data[key], list):
                    #self.data[key] = [self.data[key]]
            print("加载的JSON数据:", self.data)
        else:
            print("文件不存在:", self.filename)

    def add_entry(self, key, value):
        # 确保存储的值为列表形式
        if not isinstance(value, list):
            value = [value]
        # 合并已有条目（如果存在）
        if key in self.data:
            self.data[key].extend(value)  # 追加新值到现有列表
            # 去重
            # self.data[key] = list(dict.fromkeys(self.data[key]))
        else:
            self.data[key] = value
        self._save()

    def remove_entry(self, key):
        if key in self.data:
            del self.data[key]
            self._save()
            return True
        return False

    def _save(self):
        temp_file = self.filename + '.tmp'
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        os.replace(temp_file, self.filename)