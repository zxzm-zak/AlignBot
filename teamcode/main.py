# main.py
import json
import argparse
from LMP import LMP, image_process
from memory import Memory
from plan import Plan
from Correction import Correction

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plan execution with optional modes.')
    parser.add_argument('--mode', choices=['with_memory', 'no_memory', 'llava'], default='no_memory', help='Select mode for plan execution.')
    parser.add_argument('--img', choices=['use_url', 'use_base64'], default='use_url', help='Enable image upload to URL or embedding as base64.')
    
    args = parser.parse_args()
    image_processor = image_process()

    image_folder = '../camera_image'
    memory_path = 'path to your memory json'
    goal = "goal"
    URL_link = "url link for your camera image"
    username_b = input("Please input username:")

    # Instantiate Plan object
    planner = Plan(image_folder, memory_path, goal, username_b, mode=args.mode, img_mode=args.img, url_link=URL_link)
    planner.execute_plan()  # First execution
    counter = 0

    while True:
        continue_adjustment = input("Do you want to adjust the plan? (yes/no): ").strip().lower()
        correction = Correction(image_folder=image_folder, plan_file="plan.yaml", goal=goal, img_mode=args.img, url_link=URL_link)

        if continue_adjustment != 'yes':
            print("Plan adjustment completed.")
            correction.creat_final_records(username_b)
            is_success = True  # Plan was successful
            planner.update_instances(is_success)  # Update value scores
            break
        else:
            # Plan adjustment needed
            is_success = False
            planner.update_instances(is_success)  # Update value scores
            # Proceed with adjustment
            record = correction.creat_records(username_b)
            counter += 1
            planner.counter = counter  # Update counter
            planner.execute_replan()  # Call replan method
