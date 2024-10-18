# get_success_cases.py
import os
import json
import random
import math
import numpy as np

class Instance:
    def __init__(self, id, content, value=0.5, gradient=0.0, use_count=0):
        self.id = id
        self.content = content
        self.value = value  # Initial value score
        self.gradient = gradient  # Initial gradient
        self.use_count = use_count  # Use count

class FewShotSystem:
    def __init__(self, num_top_k=2, num_random_k=1, delta_p_positive=0.05, delta_p_negative=0.05, alpha=0.1):
        self.num_top_k = num_top_k  # Number of top value cases to select
        self.num_random_k = num_random_k  # Number of randomly selected cases
        self.delta_p_positive = delta_p_positive  # Positive feedback adjustment
        self.delta_p_negative = delta_p_negative  # Negative feedback adjustment
        self.alpha = alpha  # Decay parameter for value score

    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()

    def select_instances(self, instances):
        total_required = self.num_top_k + self.num_random_k
        
        # If the total number of instances is less than required, return all instances with a warning
        if len(instances) <= total_required:
            print(f"Not enough available instances. Requested {total_required} but only {len(instances)} are available.")
            return instances

        # Sort instances by value, select top num_top_k
        sorted_instances = sorted(instances, key=lambda x: x.value, reverse=True)
        top_k = sorted_instances[:self.num_top_k]

        # Randomly select num_random_k from the remaining instances
        remaining_instances = sorted_instances[self.num_top_k:]
        random_instances = random.sample(remaining_instances, min(self.num_random_k, len(remaining_instances))) if remaining_instances else []

        return top_k + random_instances

    def update_value(self, instance, is_success):
        """Update the value of an instance based on success or failure."""
        if is_success:
            # Positive feedback, update gradient with positive delta
            gradient_update = self.delta_p_positive * math.exp(-self.alpha * instance.use_count)
        else:
            # Negative feedback, update gradient with negative delta
            gradient_update = -self.delta_p_negative * math.exp(-self.alpha * instance.use_count)
        
        # Update gradient and value score
        instance.gradient = min(1.0, max(-1.0, instance.gradient + gradient_update))
        instance.value = min(max(0.1, instance.value + instance.gradient), 1.0)  # Ensure value stays between 0.1 and 1.0
        instance.use_count += 1  # Increment use count

    def load_data(self, goal, username, file_path='success_case.json'):
        """Load relevant cases from a file based on goal and username."""
        try:
            # Check if the file exists
            if not os.path.exists(file_path):
                print(f"File '{file_path}' does not exist. Returning an empty list.")
                return []

            # Load the file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Filter cases by goal and username
            filtered_cases = [
                Instance(i, entry["final correct case"], entry.get("value", 0.5), entry.get("gradient", 0.0), entry.get("use_count", 0))
                for i, entry in enumerate(data)
                if entry["goal"] == goal and entry["username"] == username
            ]
            
            # Check if no matching cases were found
            if not filtered_cases:
                print(f"No matching cases found for goal '{goal}' or username '{username}'. Returning an empty list.")
                return []

            return filtered_cases

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from file '{file_path}': {e}")
            return []

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []

    def save_data(self, instances, file_path='success_case.json'):
        """Save updated instances back to the file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for instance in instances:
            data[instance.id]["value"] = instance.value  # Update value score
            data[instance.id]["gradient"] = instance.gradient  # Update gradient
            data[instance.id]["use_count"] = instance.use_count  # Update use count
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_ranked_cases(self, goal, username):
        """Select cases based on value and random selection."""
        try:
            instances = self.load_data(goal, username)
        except ValueError as e:
            print(e)
            return [], []  # Return empty lists if no cases are found
        selected = self.select_instances(instances)
        return [inst.content for inst in selected], selected  # Return both content and instances

