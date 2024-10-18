from PIL import Image, ImageFilter, ImageEnhance
import os
import cv2
import numpy as np

def enhance_images(input_folder, output_folder):
    # Traverse all subfolders and files in the input folder
    for root, dirs, files in os.walk(input_folder):
        for file_name in files:
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Construct file path
                file_path = os.path.join(root, file_name)

                # Load the image
                img = Image.open(file_path)

                # Apply unsharp mask (optional, currently commented out)
                unsharp_img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
                enhancer = ImageEnhance.Brightness(unsharp_img)
                img_enhanced = enhancer.enhance(1.1)

                # Enhance contrast
                enhancer = ImageEnhance.Contrast(img_enhanced)
                img_enhanced_contrast = enhancer.enhance(1.1)

                # Enhance color saturation
                enhancer = ImageEnhance.Color(img_enhanced_contrast)
                img_enhanced_color = enhancer.enhance(1.1)

                # Convert the image to a NumPy array for resizing with OpenCV
                img_array = np.array(img_enhanced_color)

                # Resize the image to the target width while maintaining the aspect ratio
                target_width = 900
                original_height, original_width = img_array.shape[:2]
                aspect_ratio = original_height / original_width
                target_height = int(target_width * aspect_ratio)
                resized_image = cv2.resize(img_array, (target_width, target_height), interpolation=cv2.INTER_AREA)

                # Convert the resized NumPy array back to a PIL image
                final_img = Image.fromarray(resized_image)

                # Create the corresponding output folder structure
                relative_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_path)
                if not os.path.exists(output_subfolder):
                    os.makedirs(output_subfolder)

                # Ensure the output file has a .png extension for lossless compression
                output_file_name = os.path.splitext(file_name)[0] + '.png'
                output_file_path = os.path.join(output_subfolder, output_file_name)

                # Save the enhanced image to the output folder using PNG format for lossless compression
                final_img.save(output_file_path, format='PNG')

# Parameters
input_folder = 'path to your image folder'  # Source folder path
output_folder = 'path to your output folder'  # Output folder path

# Call the function
enhance_images(input_folder, output_folder)
