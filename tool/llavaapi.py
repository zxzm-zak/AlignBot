import os
from openai import OpenAI
from transformers.utils.versions import require_version
import base64
import cv2
import yaml
require_version("openai>=1.5.0", "To fix: pip install openai>=1.5.0")

if __name__ == '__main__':
    # change to your custom port
    with open('../config/prompt.yaml', 'r') as file:
            prompt_text = yaml.safe_load(file)
    port = 8000
    client = OpenAI(
        api_key="0",
        base_url="http://localhost:{}/v1".format(os.environ.get("API_PORT", 8000)),
    )
    image_folder = '../camera_image'
    image_files = os.listdir(image_folder)
    if image_files:
        latest_image_path = os.path.join(image_folder, image_files[-1])
        image_path = latest_image_path
    else:
        raise FileNotFoundError("No images found in the camera_image folder")

    LLava_prompt = prompt_text['LLava_prompt']
    LLava_prompt_1 = prompt_text['LLava_prompt_1']
    LLava_prompt_2 = prompt_text['LLava_prompt_2']

    goal = "goal"
    URL_link = "url link for your camera image"

    username = input("Please input username:")
    LLava_prompt = LLava_prompt.format(goal=goal, username=username)
    LLava_prompt_1 = LLava_prompt_1.format(goal=goal, username=username)
    LLava_prompt_2 = LLava_prompt_2.format(goal=goal, username=username)

    messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": [
                        {
                            "type": "text",
                            "text": LLava_prompt_2
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": URL_link, 
                            }
                        }
                    ]},
        ]

    result = client.chat.completions.create(
        messages=messages, 
        model="test", 
        temperature=0.5
    )
    print(result.choices[0].message.content)