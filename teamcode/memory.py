import yaml
import json
import ast
from LMP import LMP, image_process

class Memory:
    def __init__(self, img_mode='use_url', url_link=None):
        self.img_mode = img_mode
        self.url_link = url_link
        self.lmp = LMP(img=img_mode)
        self.image_processor = image_process()

    def get_keys(self, goal):
        prompt_template = self.lmp.prompt_text['keys_prompt']
        prompt = prompt_template.format(goal=goal)
        keys_response = self.lmp.LM_noimage(prompt)
        try:
            keys = ast.literal_eval(keys_response)
        except (ValueError, SyntaxError):
            print("Failed to parse keys_response.")
            keys = []
        print(f"Keys obtained from goal '{goal}': {keys}")
        return keys

    def find_memory(self, memory_path, keys, username):
        try:
            with open(memory_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if not content:
                    print(f"JSON file {memory_path} is empty")
                    return []
                data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file: {e}")
            return []

        records = []
        for item in data:
            if item.get("username", "") == username:
                goal = item.get("goal", "")
                items = item.get("items", [])
                for key in keys:
                    if key in goal or any(key in element for element in items):
                        records.append(item)
                        break

        if records:
            print(f"Found records containing keys: {keys}")
        else:
            print(f"No records containing any of the keys: {keys} were found.")
        return records

    def with_no_memory(self):
        print("Plan with no memory")
        return []

    def llava_memory(self):
        pass
