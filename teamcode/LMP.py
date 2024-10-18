# This code is configured to use Azure OpenAI for accessing GPT models.
# If you'd prefer to use the OpenAI API directly instead of Azure OpenAI, you can modify the code as follows:
# 
# 1. Replace the AzureOpenAI client instantiation with OpenAI's API client:
#
#    # import openai  # Make sure you have installed the openai package: pip install openai
#    # openai.api_key = "your_openai_api_key_here"
#    # response = openai.ChatCompletion.create(
#    #     model="gpt-4",
#    #     messages=[
#    #         {"role": "system", "content": "You are a helpful assistant."},
#    #         {"role": "user", "content": "Hello!"}
#    #     ]
#    # )
#    # print(response.choices[0].message['content'])
#
# 2. Make sure to replace your Azure API key with your OpenAI API key, and adjust the usage according to OpenAI's documentation:
#    https://platform.openai.com/docs/guides/chat
#
# 3. Remove or comment out any Azure-specific code if it's no longer needed.

import os
import base64
from openai import OpenAI
import cv2
import yaml
from openai import AzureOpenAI
import os
import cv2
import requests
from msal import ConfidentialClientApplication

class LMP:
    def __init__(self, img = "use_url"):
        with open('../config/config.yaml', 'r') as file:
            self.cfg = yaml.safe_load(file)
        
        with open('../config/prompt.yaml', 'r') as file:
            self.prompt_text = yaml.safe_load(file)

        self.client = AzureOpenAI(
            azure_endpoint="AZURE_ENDPOINT",
            api_key="AZURE_API_KEY",
            api_version="AZURE_API_VERSION"
        ) # 
        self.img = img

    def LM(self, prompt, base64_image=None, url_link=None):
        if self.img == 'use_url':
            if not url_link:
                raise ValueError("URL link is required when img mode is 'use_url'.")
            messages = [
                {"role": "system", "content": "You are a helpful assistant. You are controlling a one-armed robot."},
                {"role": "user", "content": [
                    {
                        "type": "text", 
                        "text": prompt
                    },
                    {
                        "type": "image_url", 
                        "image_url": {
                            "url": url_link, 
                            "detail": "high"
                        }
                    }
                ]},
            ]
        elif self.img == 'use_base64':
            if not base64_image:
                raise ValueError("Base64 image is required when img mode is 'use_base64'.")
            messages = [
                {"role": "system", "content": "You are a helpful assistant. You are controlling a one-armed robot."},
                {"role": "user", "content": [
                    {
                        "type": "text", 
                        "text": prompt
                    },
                    {
                        "type": "image_url", 
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}", 
                            "detail": "high"
                        }
                    }
                ]},
            ]
        else:
            raise ValueError("Invalid image mode. Please use 'use_url' or 'use_base64'.")

        response = self.client.chat.completions.create(
            model=self.cfg['model'], 
            messages=messages,
            max_tokens=self.cfg['max_tokens'], 
            temperature=self.cfg['temperature'],
        )
        return response.choices[0].message.content


class llava:
    def __init__(self, img = "use_url"):
        with open('../config/config.yaml', 'r') as file:
            self.cfg = yaml.safe_load(file)
        
        with open('../config/prompt.yaml', 'r') as file:
            self.prompt_text = yaml.safe_load(file)

        self.port = 8000

        self.client = OpenAI(
            api_key="0",
            base_url="http://localhost:{}/v1".format(os.environ.get("API_PORT", 8000)),
        )
        self.img = img

    def lv(self, prompt, base64_image=None, url_link=None):
        if self.img == 'use_url':
            if not url_link:
                raise ValueError("URL link is required when img mode is 'use_url'.")
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
                            "url": url_link, 
                        }
                    }
                ]},
            ]
        elif self.img == 'use_base64':
            if not base64_image:
                raise ValueError("Base64 image is required when img mode is 'use_base64'.")
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
                            "url": f"data:image/jpeg;base64,{base64_image}", 
                            "detail": "high"
                        }
                    }
                ]},
            ]
        else:
            raise ValueError("Invalid image mode. Please use 'use_url' or 'use_base64'.")
            

        result = self.client.chat.completions.create(messages=messages, model="test", temperature = 0.6)

        return result.choices[0].message.content
    

    def lam(self, prompt, base64_image=None, url_link=None):
        if self.img == 'use_url':
            if not url_link:
                raise ValueError("URL link is required when img mode is 'use_url'.")
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": [
                    {
                        "type": "text", 
                        "text": prompt
                    }
                ]},
            ]
        elif self.img == 'use_base64':
            if not base64_image:
                raise ValueError("Base64 image is required when img mode is 'use_base64'.")
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": [
                    {
                        "type": "text", 
                        "text": prompt
                    }
                ]},
            ]
        else:
            raise ValueError("Invalid image mode. Please use 'use_url' or 'use_base64'.")
            
        result = self.client.chat.completions.create(messages=messages, model="Llama-2-7b-hf", temperature=0.9)

        return result.choices[0].message.content

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
    def encode_image(image_path, target_width=800):
        image = cv2.imread(image_path)
        original_height, original_width = image.shape[:2]
        aspect_ratio = original_height / original_width
        target_height = int(target_width * aspect_ratio)
        resized_image = cv2.resize(image, (target_width, target_height), interpolation=cv2.INTER_AREA)
        _, buffer = cv2.imencode('.jpg', resized_image, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        encoded_image = base64.b64encode(buffer).decode('utf-8')
        return encoded_image