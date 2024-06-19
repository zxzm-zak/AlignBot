import yaml
from LMP import LMP, image_process
from memory import Memory

class Plan(Memory):
    
    def __init__(self, image_folder, memory_path, goal):
        super().__init__()
        self.image_folder = image_folder
        self.memory_path = memory_path
        self.goal = goal

    def get_action_plan(self, goal, image_path):
        prompt_template = self.prompt_text['prompt_template']
        base64_image = self.encode_image(image_path)
        keys = self.get_keys(goal)
        records = self.find_memory(self.memory_path, keys)
        prompt = prompt_template.format(goal = self.goal, base64_image = base64_image, records = records)
        action_plan = self.LM(prompt, base64_image)
        return action_plan

    def save_plan_to_yaml(self, plan, file_name='plan.yaml'):
        with open(file_name, 'w') as file:
            yaml.dump(plan, file)

    def execute_plan(self):
        try:
            image_path = self.get_camera_image_path(self.image_folder)
            print(f"Using image: {image_path}")
        except FileNotFoundError as e:
            print(e)
            return

        action_plan = self.get_action_plan(self.goal, image_path)
        print(f"Generated action plan: {action_plan}")

        self.save_plan_to_yaml(action_plan)
        print("Action plan saved to plan.yaml")