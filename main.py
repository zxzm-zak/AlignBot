from getstate import ObjectStateDescriptor
from plan import Plan
from Correction import Correction

if __name__ == "__main__":
    image_folder = 'camera_image'
    memory_path = 'memory.json'
    goal = "bring me the banana"
    #obj_list = "block_red, block_orange, block_purple, block_pink, block_yellow, block_green"
    #obj_list = "Oven, Microwave, Water Boiler, Paper Towel Roll"
    #obj_list = "refrigerator, banana"
    #descriptor = ObjectStateDescriptor(image_folder)
    #obj_list = descriptor.get_objectlist
    #descriptor.describe_objects(obj_list)
    
    planner = Plan(image_folder, memory_path, goal)
    planner.execute_plan()
    #correction = Correction(image_folder="camera_image", plan_file="plan.yaml")
    #record = correction.get_records()
    #print(record)