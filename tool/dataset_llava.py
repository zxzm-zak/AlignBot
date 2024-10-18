import json
from collections import defaultdict

def update_data(input_file, output_file):
    # Read the input data
    with open(input_file, 'r', encoding='utf-8') as f:
        try:
            data_list = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON data: {e}")
            return

    # Process the data: group by 'username', 'goal', and 'image path'
    grouped_data = defaultdict(list)
    for entry in data_list:
        username = entry.get('username')
        goal = entry.get('goal')
        image_path = entry.get('image path')
        if username and goal and image_path:
            key = (username, goal, image_path)
            grouped_data[key].append(entry)
        else:
            continue

    # Build the output data structure
    output_data_list = []
    for (username, goal, image_path), entries in grouped_data.items():
        # Merge 'user instructions'
        user_instructions = [entry.get('user instructions', '') for entry in entries]
        merged_instructions = ' '.join(user_instructions).strip()

        # Build messages
        message_content = f"{username} wants robot to {goal}. If you were {username}, what reminders would you give to the robot?"
        messages = [
            {
                "content": message_content,
                "role": "user"
            },
            {
                "content": merged_instructions,
                "role": "assistant"
            }
        ]

        output_entry = {
            "messages": messages,
            "images": [image_path]
        }
        output_data_list.append(output_entry)

    # Write the output data to the output file
    with open(output_file, 'w') as f:
        json.dump(output_data_list, f, indent=4)

# Usage
input_file = 'path to your memory.json'
output_file = 'dataset_llava.json'
update_data(input_file, output_file)
