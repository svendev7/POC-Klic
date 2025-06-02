import os
import cv2
import numpy as np
from PIL import Image

def compare_images(current_image_path, reference_image_path, threshold=5):
    """
    Compare two images and determine if they are similar.
    
    Args:
        current_image_path (str): Path to the current screenshot image
        reference_image_path (str): Path to the reference image
        threshold (float): Maximum allowed difference percentage (default: 5%)
        
    Returns:
        tuple: (is_similar, difference_percentage)
    """
    if not os.path.exists(reference_image_path):
        return False, 100.0
    
    if not os.path.exists(current_image_path):
        return False, 100.0
        
    try:
        current_img = cv2.imread(current_image_path)
        reference_img = cv2.imread(reference_image_path)
        
        # Convert images to same size if needed
        reference_img = cv2.resize(reference_img, (current_img.shape[1], current_img.shape[0]))
        
        # Calculate difference
        difference = cv2.absdiff(current_img, reference_img)
        difference_percentage = (np.sum(difference) / (current_img.shape[0] * current_img.shape[1] * current_img.shape[2] * 255)) * 100
        
        return difference_percentage < threshold, difference_percentage
    except Exception as e:
        print(f"Error comparing images: {e}")
        return False, 100.0

def create_reference_screenshot(screenshot_path, reference_dir="reference_images"):
    """
    Save a current screenshot as a reference image.
    
    Args:
        screenshot_path (str): Path to the screenshot to save as reference
        reference_dir (str): Directory to store reference images
        
    Returns:
        str: Path to the saved reference image
    """
    if not os.path.exists(reference_dir):
        os.makedirs(reference_dir)
    
    filename = os.path.basename(screenshot_path)
    reference_path = os.path.join(reference_dir, f"ref_{filename}")
    
    if os.path.exists(screenshot_path):
        try:
            img = Image.open(screenshot_path)
            img.save(reference_path)
            return reference_path
        except Exception as e:
            print(f"Error saving reference image: {e}")
            return None
    
    return None 