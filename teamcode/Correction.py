import yaml
import json
import os
from urllib.parse import urlparse, unquote
import cv2
import base64
import sys
from datetime import datetime
from LMP import LMP, image_process

class Correction:
    
    def __init__(self, image_folder, plan_file, goal, img_mode='use_url', url_link=None):
        self.image_folder = image_folder
        self.plan_file = plan_file
        self.goal = goal
        self.img_mode = img_mode
        self.url_link = url_link
        self.lmp = LMP(img=img_mode)  # Instantiate the LMP class
        self.image_processor = image_process()  # Instantiate image_process class

    def load_planstep(self):
        with open(self.plan_file, 'r') as file:
            return yaml.safe_load(file)
    
    def save_records(self, record, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as jsonfile:
                content = jsonfile.read()
                if content.strip():  # Check if the file is empty
                    existing_data = json.loads(content)
                else:
                    existing_data = []
        else:
            existing_data = []

        if not isinstance(existing_data, list):
            existing_data = [existing_data]

        existing_data.append(record)

        with open(file_path, 'w') as jsonfile:
            json.dump(existing_data, jsonfile, indent=4)

    def creat_records(self, username):
        
        timestep = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        planstep = self.load_planstep() 
        instructions = input("If you have any instructions, please enter here:")
        if instructions.strip() == "":
            sys.exit("No instructions provided. Terminating the program.")
        
        if self.img_mode == 'use_url':
            prompt_template = self.lmp.prompt_text['correction_prompt_url']  # get prompt from LMP
            prompt = prompt_template.format(url_link1=self.url_link, timestep1=timestep, goal1=self.goal, instructions1=instructions, planstep1=planstep, username1=username)
            record = self.lmp.LM(prompt, url_link=self.url_link)
        elif self.img_mode == 'use_base64':
            prompt_template = self.lmp.prompt_text['correction_prompt']  # get prompt from LMP
            image_path = self.image_processor.get_camera_image_path(self.image_folder)
            base64_image = self.image_processor.encode_image(image_path)
            prompt = prompt_template.format(image_path1=image_path, timestep1=timestep, goal1=self.goal, instructions1=instructions, planstep1=planstep, username1=username)
            record = self.lmp.LM(prompt, base64_image=base64_image)
        else:
            record = self.lmp.LM_noimage(prompt)

        record = self.process_record(record)

        self.save_records(record, 'memory.json')
        return record

    def creat_final_records(self, username):
        
        timestep = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        planstep = self.load_planstep() 

        if self.img_mode == 'use_url':
            prompt_template = self.lmp.prompt_text['finalcase_prompt_url']
            prompt = prompt_template.format(url_link1=self.url_link, timestep1=timestep, goal1=self.goal, planstep1=planstep, username1=username)
            record = self.lmp.LM(prompt, url_link=self.url_link)
        elif self.img_mode == 'use_base64':
            prompt_template = self.lmp.prompt_text['finalcase_prompt']
            image_path = self.image_processor.get_camera_image_path(self.image_folder)
            base64_image = self.image_processor.encode_image(image_path)
            prompt = prompt_template.format(image_path1=image_path, timestep1=timestep, goal1=self.goal, planstep1=planstep, username1=username)
            record = self.lmp.LM(prompt, base64_image=base64_image)
        else:
            record = self.lmp.LM_noimage(prompt)

        record = self.process_record(record)

        self.save_records(record, 'memory.json')
        return record

    def process_record(self, record):
        if isinstance(record, str):
            json_start = record.find('{')
            if json_start != -1:
                json_content = record[json_start:]
                json_end = json_content.rfind('}')
                if json_end != -1:
                    json_content = json_content[:json_end + 1]
                record = json.loads(json_content)
        return record

    def get_filename_from_url(url):
    # Parse URL, get filename from url
        parsed_url = urlparse(url)
        path = parsed_url.path
        path = unquote(path)
        filename = os.path.basename(path)
        if not filename:
            query_params = parsed_url.query
            for param in query_params.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    if key in ['file', 'filename', 'name']:
                        return value
        return filename