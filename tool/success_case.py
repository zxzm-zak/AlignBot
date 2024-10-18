import json
import os

def extract_data_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract data that contains "final correct case" and initialize value, gradient, and use_count
    extracted_data = []
    for item in data:
        if "final correct case" in item:
            extracted_info = {
                "username": item["username"],
                "goal": item["goal"],
                "final correct case": item["final correct case"],
                "value": item.get("value", 0.5),  # Default value is 0.5
                "gradient": item.get("gradient", 0.0),  # Default gradient is 0.0
                "use_count": item.get("use_count", 0)  # Default use_count is 0
            }
            extracted_data.append(extracted_info)
    return extracted_data

def append_data_to_file(save_path, new_data):
    # Check if the save file exists, if yes, read existing data
    if os.path.exists(save_path):
        with open(save_path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    # Append new extracted data to the existing data
    existing_data.extend(new_data)

    # Save the merged data back to the file
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    print(f"Data successfully appended and saved to: {save_path}")

# Function to add value, gradient, and use_count fields
def add_value_to_success_cases(file_path='success_case.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Add value, gradient, and use_count fields if they are missing
    for entry in data:
        if "value" not in entry:
            entry["value"] = 0.5
            entry["gradient"] = 0.0
            entry["use_count"] = 0

    # Save the updated data back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"All success cases have been updated with value, gradient, and use_count fields in {file_path}")

# Example usage
save_path = "success_case.json"  # Path to the save file

# Assuming you have multiple files to extract from
file_paths = ["path to your memory json"]  # Replace with your file paths

for file_path in file_paths:
    new_data = extract_data_from_file(file_path)  # Extract and initialize data
    append_data_to_file(save_path, new_data)  # Save the data to the file

# Call the function to ensure all success cases have the value field
add_value_to_success_cases(save_path)
