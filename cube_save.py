import cv2
import time
import os
import shutil
import subprocess


def clear_folder(folder_path):
    # Clear the existing content of the folder
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)
    os.chmod(folder_path, 0o777)


def capture_and_run_scripts(camera_indices, output_folders, open_script_path, close_script_path):
    for output_folder in output_folders:
        # Clear the existing content of the output folder
        clear_folder(output_folder)

    # Open the cameras
    caps = [cv2.VideoCapture(index) for index in camera_indices]

    # Check if the cameras are successfully opened
    for cap in caps:
        if not cap.isOpened():
            print(f"Failed to open camera with index {cap}")
            return

    # Set the image size for all cameras
    for cap in caps:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Capture a single frame from each camera with a delay of 100ms
    frames = [cap.read()[1] for cap in caps]

    # Check if the images are read correctly
    for i, frame in enumerate(frames):
        if frame is None:
            print(f"Failed to capture image from camera with index {camera_indices[i]}")
            return

    # Save the images to the output folder with customized filenames
    for i, frame in enumerate(frames):
        image_path = os.path.join(output_folders[i], f"cam_{i}_C.jpg")
        cv2.imwrite(image_path, frame)
        os.chmod(image_path, 0o777)

    # Release the cameras
    for cap in caps:
        cap.release()

    # Display a message
    print(f"Initial images captured successfully for cameras {camera_indices} in folders {output_folders}.")

    # Run open.py script
    subprocess.run(["python3", open_script_path])

    # Wait for a moment (you can adjust the sleep duration as needed)
    time.sleep(0.1)

    # Open the cameras again
    caps = [cv2.VideoCapture(index) for index in camera_indices]

    # Set the image size for all cameras to 1280x1080
    for cap in caps:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Capture another frame from each camera after running open.py
    frames_after_open = [cap.read()[1] for cap in caps]

    # Check if the images are read correctly
    for i, frame_after_open in enumerate(frames_after_open):
        if frame_after_open is None:
            print(f"Failed to capture image from camera with index {camera_indices[i]} after running open.py")
            return

    # Save the images after open.py to the output folder with customized filenames
    for i, frame_after_open in enumerate(frames_after_open):
        after_open_image_path = os.path.join(output_folders[i], f"cam_{i}_O.jpg")
        cv2.imwrite(after_open_image_path, frame_after_open)
        os.chmod(after_open_image_path, 0o777)

    # Release the cameras after running open.py
    for cap in caps:
        cap.release()

    # Run close.py script
    subprocess.run(["python3", close_script_path])

    # Display a message
    print(f"Scripts executed successfully for cameras {camera_indices} in folders {output_folders}.")


# Set the camera indices and output folders
camera_indices = [0, 1]  # You can modify this list based on your actual camera indices
output_folder_cam0 = os.path.expanduser("/mnt/img/cube_img/f_cam0")  # Output folder path for camera 0
output_folder_cam1 = os.path.expanduser("/mnt/img/cube_img/f_cam1")  # Output folder path for camera 1
output_folders = [output_folder_cam0, output_folder_cam1]
open_script_path = "/home/nano/client/open.py"
close_script_path = "/home/nano/client/close.py"

# Call the capture_and_run_scripts function
capture_and_run_scripts(camera_indices, output_folders, open_script_path, close_script_path)
