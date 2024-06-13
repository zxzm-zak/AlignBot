import cv2
import torch
import detectron2
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
from detectron2 import model_zoo
import numpy as np
from collections import defaultdict
import os

def get_color_name(rgb):
    colors = {
        "红色": (255, 0, 0),
        "绿色": (0, 255, 0),
        "蓝色": (0, 0, 255),
        "黄色": (255, 255, 0),
        "青色": (0, 255, 255),
        "品红色": (255, 0, 255),
        "白色": (255, 255, 255),
        "黑色": (0, 0, 0),
        "灰色": (128, 128, 128),
        "橙色": (255, 165, 0),
        "紫色": (128, 0, 128),
        "棕色": (165, 42, 42)
    }

    closest_color = None
    min_distance = float('inf')
    
    for color_name, color_value in colors.items():
        distance = np.linalg.norm(np.array(color_value) - np.array(rgb))
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name

    return closest_color

def get_obj(image_path, result_folder):
    try:
        cfg = get_cfg()
        cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml"))
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.3
        cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x")
         
        predictor = DefaultPredictor(cfg)
        
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image at path {image_path} not found.")
        
        outputs = predictor(image)
        
        classes = outputs["instances"].pred_classes
        class_names = MetadataCatalog.get(cfg.DATASETS.TRAIN[0]).thing_classes
        masks = outputs["instances"].pred_masks
        colors = []

        for mask in masks:
            mask = mask.cpu().numpy()
            color = cv2.mean(image, mask=mask.astype(np.uint8))[::-1]
            colors.append(color)

        detected_objects = defaultdict(list)
        
        for i in range(len(classes)):
            class_name = class_names[classes[i]]
            color = colors[i]
            color_name = get_color_name(color[:3])
            detected_objects[class_name].append(color_name)
        
        result = []
        for obj, color_list in detected_objects.items():
            if len(color_list) > 1:
                for idx, color in enumerate(color_list):
                    result.append(f"{obj}_{idx + 1}_{color}")
            else:
                result.append(f"{obj}_{color_list[0]}")
        
        v = Visualizer(image[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        
        os.makedirs(result_folder, exist_ok=True)
        result_image_path = os.path.join(result_folder, "detected_image.jpg")
        cv2.imwrite(result_image_path, out.get_image()[:, :, ::-1])
        
        return result

    except Exception as e:
        return str(e)

image_path = "/home/yan/Nutstore Files/icra/image/problem8.jpg"
result_folder = "./result"
detected_objects = get_obj(image_path, result_folder)
print(detected_objects)
