import yaml
import json
from LMP import LMP, image_process, llava
from memory import Memory
import random
from get_success_cases import FewShotSystem  # Import the FewShotSystem class

class Plan:
    def __init__(self, image_folder, memory_path, goal, username, mode='with_memory', img_mode='use_url', url_link=None):
        self.image_folder = image_folder
        self.memory_path = memory_path
        self.goal = goal
        self.counter = 0
        self.username = username
        self.mode = mode
        self.img_mode = img_mode
        self.url_link = url_link
        self.lmp = LMP(img=self.img_mode)
        self.llava = llava(img=self.img_mode)
        self.image_processor = image_process()
        self.memory = Memory(img_mode=self.img_mode, url_link=self.url_link)
        self.few_shot_system = FewShotSystem(num_top_k=2, num_random_k=1)  # Initialize FewShotSystem
        self.selected_instances = []  # To store selected instances for later updates

    def get_random_final_cases(self, f_goal, f_username):
        # Use FewShotSystem to get ranked cases
        cases, instances = self.few_shot_system.get_ranked_cases(f_goal, f_username)
        self.selected_instances = instances  # Store for later updating
        return cases

    def update_instances(self, is_success):
            """Update value scores of selected instances based on feedback."""
            for instance in self.selected_instances:
                self.few_shot_system.update_value(instance, is_success)
            self.few_shot_system.save_data(self.selected_instances)
        
    def get_random_records(self, sel_goal, n):
        memory_file = 'memory.json'
        try:
        # 打开 memory.json 文件并加载数据
            with open(memory_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"File {memory_file} not found.")
            return []
        except json.JSONDecodeError:
            print(f"Error parsing JSON from {memory_file}.")
            return []

        # 筛选出具有相同 goal 的记录
        goal_matches = [entry for entry in data if entry.get('goal') == sel_goal]

        if len(goal_matches) == 0:
            print(f"No matching records found for goal: {sel_goal}")
            return []

        # 随机抽取 n 条记录
        selected_records = random.sample(goal_matches, min(n, len(goal_matches)))

        return selected_records

    def get_action_plan(self, goal, image_path):
        prompt_template = self.lmp.prompt_text['prompt_template']
        prompt_template_norecords = self.lmp.prompt_text['prompt_template_norecords']
        AlignBot_Prompt = self.lmp.prompt_text['AlignBot_Prompt']
        LLava_prompt_0 = self.lmp.prompt_text['LLava_prompt']
        LLava_prompt_1 = self.lmp.prompt_text['LLava_prompt_1']
        LLava_prompt_2 = self.lmp.prompt_text['LLava_prompt_2']


        if self.mode == 'with_memory':
            records = self.get_random_records(goal, 2) 
            print(records)
            prompt = prompt_template.format(goal=self.goal, records=records)

        elif self.mode == 'no_memory':
            prompt = prompt_template_norecords.format(goal=self.goal)
        
        elif self.mode == 'llava':
            LLava_prompt = LLava_prompt_2.format(goal=self.goal, username=self.username)
            if self.img_mode == 'use_url':
                Reminders = self.llava.lv(LLava_prompt, url_link=self.url_link)
            elif self.img_mode == 'use_base64':
                base64_image = self.image_processor.encode_image(image_path)
                Reminders = self.llava.lv(LLava_prompt, base64_image=base64_image)
            else:
                raise ValueError("Please use 'use_url' or 'use_base64' to upload image.")
            print(Reminders)
            final_cases = self.get_random_final_cases(f_goal=self.goal, f_username=self.username)
            print(final_cases)
            prompt = AlignBot_Prompt.format(goal=self.goal, username=self.username, Successes = final_cases, Reminders = Reminders)
        else:
            raise ValueError("Invalid mode. Please use 'with_memory', 'no_memory' or 'llava'.")

        if self.img_mode == 'use_url':
            action_plan = self.lmp.LM(prompt, url_link=self.url_link)
        elif self.img_mode == 'use_base64':
            base64_image = self.image_processor.encode_image(image_path)
            action_plan = self.lmp.LM(prompt, base64_image=base64_image)
        else:
            raise ValueError("Please use 'use_url' or 'use_base64' to upload image.")
        
        return action_plan
    
    def get_action_replan(self, goal, image_path):
        AlignBot_Prompt_re = self.lmp.prompt_text['AlignBot_Prompt_re']
        prompt_template = self.lmp.prompt_text['prompt_template']
        
        try:
            with open(self.memory_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if not content:
                    print(f"JSON file {self.memory_path} is empty")
                    return []
                data = json.loads(content)

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file: {e}")
            return []

        filtered_records = []
        for entry in data[-self.counter:]:
            filtered_entry = {k: entry[k] for k in entry if k not in ['items','url link', 'color', 'state of items', 'failure case']}
            filtered_records.append(filtered_entry)

        print(self.counter)
        print(filtered_records)
        
        prompt = AlignBot_Prompt_re.format(goal=goal, records=filtered_records)

        if self.img_mode == 'use_url':
            print(self.url_link)
            action_plan = self.lmp.LM(prompt, url_link=self.url_link)
        elif self.img_mode == 'use_base64':
            base64_image = self.image_processor.encode_image(image_path)
            action_plan = self.lmp.LM(prompt, base64_image=base64_image)
        else:
            raise ValueError("Please use 'use_url' or 'use_base64' to upload image.")

        return action_plan

    def save_plan_to_yaml(self, plan, file_name='plan.yaml'):
        with open(file_name, 'w') as file:
            yaml.dump(plan, file)

    def execute_plan(self):
        try:
            if self.img_mode == 'use_url':
                # using URL pattern, local image path is not required
                image_path = None
                print(f"Using url image")
            else:
                # Get local image path
                image_path = self.image_processor.get_camera_image_path(self.image_folder)
                print(f"Using image: {image_path}")
        except FileNotFoundError as e:
            print(e)
            return

        action_plan = self.get_action_plan(self.goal, image_path)
        print(f"Generated action plan: {action_plan}")

        self.save_plan_to_yaml(action_plan)
        print("Action plan saved to plan.yaml")

    def execute_replan(self):
        try:
            if self.img_mode == 'use_url':
                # using URL pattern, local image path is not required
                image_path = None
                print(f"Using url image")
            else:
                # Get local image path
                image_path = self.image_processor.get_camera_image_path(self.image_folder)
                print(f"Using image: {image_path}")

        except FileNotFoundError as e:
            print(e)
            return

        action_plan = self.get_action_replan(self.goal, image_path)
        print(f"Generated action plan: {action_plan}")

        self.save_plan_to_yaml(action_plan)
        print("Action plan saved to plan.yaml")
