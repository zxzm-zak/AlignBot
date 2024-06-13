import os
import base64
import openai
import cv2
import yaml
from openai import AzureOpenAI

class LMP:

    def __init__(self):
        with open('config.yaml', 'r') as file:
            self.cfg = yaml.safe_load(file)
        
        with open('prompt.yaml', 'r') as file:
            self.prompt_text = yaml.safe_load(file)

        self.client = AzureOpenAI(
            azure_endpoint="https://gpt-4o-zngd2.openai.azure.com/",
            api_key="80901122ccbc42fc993a073317f9022f",
            api_version="2024-02-01"
        )

    def LM(self, prompt, base64_image):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]},
        ]

        response = self.client.chat.completions.create(
            model=self.cfg['model'], 
            messages=messages,
            max_tokens=self.cfg['max_tokens'], 
            temperature=self.cfg['temperature'],
            #stop=self.cfg['stop']
        )
        return response.choices[0].message.content

class image_process:

    @staticmethod
    def get_camera_image_path(image_folder):
        image_files = os.listdir(image_folder)
        if image_files:
            latest_image_path = os.path.join(image_folder, image_files[-1])
            return latest_image_path
        else:
            raise FileNotFoundError("No images found in the camera_image folder")

    @staticmethod
    def encode_image(image_path, max_size=(512, 512)):
        image = cv2.imread(image_path)
        compressed_image = cv2.resize(image, max_size, interpolation=cv2.INTER_AREA)
        _, buffer = cv2.imencode('.jpg', compressed_image)
        return base64.b64encode(buffer).decode('utf-8')

class plan(image_process, LMP):
    
    def __init__(self, image_folder):
        super().__init__()
        self.image_folder = image_folder

    def get_action_plan(self, goal, image_path):
        prompt_template = self.prompt_text['prompt_template']
        base64_image = self.encode_image(image_path)
        prompt = prompt_template.format(goal=goal, base64_image=base64_image)
        action_plan = self.LM(prompt, base64_image)
        return action_plan

    def save_plan_to_yaml(self, plan, file_name='plan.yaml'):
        with open(file_name, 'w') as file:
            yaml.dump(plan, file)

    def plan(self, goal):
        try:
            image_path = self.get_camera_image_path(self.image_folder)
            print(f"Using image: {image_path}")
        except FileNotFoundError as e:
            print(e)
            return

        action_plan = self.get_action_plan(goal, image_path)
        print(f"Generated action plan: {action_plan}")

        self.save_plan_to_yaml(action_plan)
        print("Action plan saved to plan.yaml")

if __name__ == "__main__":
    image_folder = 'camera_image'
    planner = plan(image_folder)
    planner.plan("Place the cup on the plate")