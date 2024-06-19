import yaml
from LMP import LMP, image_process


class ObjectStateDescriptor(image_process, LMP):
    def __init__(self, image_folder):
        super().__init__()
        self.image_folder = image_folder

    def get_objectlist(self, image_path):
        prompt = self.prompt_text['obj_prompt']
        base64_image = self.encode_image(image_path)
        obj_list = self.LM(prompt, base64_image)
        return obj_list

    def get_object_state(self, obj_list, image_path):
        prompt_template = self.prompt_text['current_state_prompt']
        base64_image = self.encode_image(image_path)
        prompt = prompt_template.format(obj_list=obj_list)
        object_state = self.LM(prompt, base64_image)
        return object_state

    def save_state_to_yaml(self, state, file_name='object_state.yaml'):
        with open(file_name, 'w') as file:
            yaml.dump(state, file)

    def describe_objects(self, obj_list):
        try:
            image_path = self.get_camera_image_path(self.image_folder)
            print(f"Using image: {image_path}")
        except FileNotFoundError as e:
            print(e)
            return

        obj_list = self.get_objectlist(image_path)
        print(f"Generated object list: {obj_list}")
        object_state = self.get_object_state(obj_list, image_path)
        print(f"Generated object state: {object_state}")

        self.save_state_to_yaml(object_state)
        print("Object state saved to object_state.yaml")


