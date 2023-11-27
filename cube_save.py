import cv2
import time
import os
import shutil
import subprocess

def capture_and_run_scripts(camera_indices, output_folder, open_script_path, close_script_path):
    # Clear the existing content of the output folder
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    # Set the permissions of the output folder to 777
    os.chmod(output_folder, 0o777)

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

    # Capture a single frame from each camera
    frames = [cap.read()[1] for cap in caps]

    # Check if the images are read correctly
    for i, frame in enumerate(frames):
        if frame is None:
            print(f"Failed to capture image from camera with index {camera_indices[i]}")
            return

    # Save the images to the output folder
    for i, frame in enumerate(frames):
        image_path = os.path.join(output_folder, f"captured_image_camera{camera_indices[i]}.jpg")
        cv2.imwrite(image_path, frame)
        os.chmod(image_path, 0o777)

    # Release the cameras
    for cap in caps:
        cap.release()

    # Display a message
    print("Images captured successfully.")

    # Run the open.py script
    subprocess.run(["/home/nano/client/open.py"])

    # Wait for a moment (you can adjust the sleep duration as needed)
    time.sleep(0.1)

    # Capture another frame from each camera after running open.py
    frames_after_open = [cap.read()[1] for cap in caps]

    # Check if the images are read correctly
    for i, frame_after_open in enumerate(frames_after_open):
        if frame_after_open is None:
            print(f"Failed to capture image from camera with index {camera_indices[i]} after running open.py")
            return

    # Save the images after open.py to the output folder
    for i, frame_after_open in enumerate(frames_after_open):
        image_path = os.path.join(output_folder, f"captured_image_after_open_camera{camera_indices[i]}.jpg")
        cv2.imwrite(image_path, frame_after_open)
        os.chmod(image_path, 0o777)

    # Run the close.py script
    subprocess.run(["/home/nano/client/close.py"])

    # Display a message
    print("Scripts executed successfully.")

# Set the camera indices and output folders
camera_indices = [0, 1]  # You can modify this list based on your actual camera indices
output_folder_cam0 = os.path.expanduser("/mnt/img/cube_img/f_cam0")  # Output folder path for camera 0
output_folder_cam1 = os.path.expanduser("/mnt/img/cube_img/f_cam1")  # Output folder path for camera 1
open_script_path = "/home/nano/client/open.py"
close_script_path = "/home/nano/client/close.py"

# Call the capture_and_run_scripts function for camera 0
capture_and_run_scripts([camera_indices[0]], output_folder_cam0, open_script_path, close_script_path)

# Call the capture_and_run_scripts function for camera 1
capture_and_run_scripts([camera_indices[1]], output_folder_cam1, open_script_path, close_script_path)
