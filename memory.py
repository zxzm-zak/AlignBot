import yaml
import json
import ast
from LMP import LMP, image_process


class Memory(image_process, LMP):
    def __init__(self):
        super().__init__()

    def get_keys(self, goal):
        prompt_template = self.prompt_text['keys_prompt']
        prompt = prompt_template.format(goal=goal)
        keys_response = self.LM_noimage(prompt)
        try:
            # 使用 ast.literal_eval 将字符串解析为实际的列表
            keys = ast.literal_eval(keys_response)
        except (ValueError, SyntaxError):
            # 如果解析失败，则打印错误并返回空列表
            print("Failed to parse keys_response.")
            keys = []
        print(f"Keys obtained from goal '{goal}': {keys}")
        return keys

    def find_memory(self, memory_path, keys):
        with open(memory_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        records = []

        for key in keys:
            for item in data:
                if key in item["items"] and item not in records:
                    records.append(item)
                    break

        if records:
            print(f"Found records containing keys: {keys}")
        else:
            print(f"No records containing any of the keys: {keys} were found.")
        
        return records
