from getstate import ObjectStateDescriptor

if __name__ == "__main__":
    image_folder = 'camera_image'
    #obj_list = "block_red, block_orange, block_purple, block_pink, block_yellow, block_green"
    obj_list = "Oven, Microwave, Water Boiler, Paper Towel Roll"
    descriptor = ObjectStateDescriptor(image_folder)
    descriptor.describe_objects(obj_list)
    