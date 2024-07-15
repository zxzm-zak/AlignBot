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

    def LM_noimage(self, prompt):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
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
