import yaml
import json
import os
import cv2
import base64
import sys
from LMP import LMP, image_process

class Correction(image_process, LMP):
    
    def __init__(self, image_folder, plan_file):
        super().__init__()
        self.image_folder = image_folder
        self.plan_file = plan_file

    def load_planstep(self):
        with open(self.plan_file, 'r') as file:
            return yaml.safe_load(file)
    
    def save_records(self, record, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as jsonfile:
                existing_data = json.load(jsonfile)
        else:
            existing_data = []

        if not isinstance(existing_data, list):
            existing_data = [existing_data]

        existing_data.append(record)

        with open(file_path, 'w') as jsonfile:
            json.dump(existing_data, jsonfile, indent=4)

    def get_records(self):
        prompt_template = self.prompt_text['correction_prompt']
        image_path = self.get_camera_image_path(self.image_folder)

        base64_image = self.encode_image(image_path)
        
        planstep = self.load_planstep()
        instructions = input("If you have any instructions please enter here:")
        if instructions.strip() == "":
            sys.exit("No instructions provided. Terminating the program.")

        prompt = prompt_template.format(instructions=instructions, planstep=planstep)
        record = self.LM(prompt, base64_image)
            
        if isinstance(record, str):
            json_start = record.find('{')
            if json_start != -1:
                json_content = record[json_start:]
                json_end = json_content.rfind('}')
                if json_end != -1:
                    json_content = json_content[:json_end + 1]
                record = json.loads(json_content)

        self.save_records(record, 'memory.json')
            
        return record
