import cv2
import time
import os
import shutil


def clear_and_capture_images(camera_index, output_folder):
    # Clear the existing content of the output folder
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    # Set the permissions of the output folder to 777
    os.chmod(output_folder, 0o777)

    # Open the camera
    cap = cv2.VideoCapture(camera_index)

    # Check if the camera is successfully opened
    if not cap.isOpened():
        print("Failed to open the camera")
        return

    # Set the image size
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    # Initialize the frame rate counter
    frame_count = 0
    start_time = time.time()

    # Continuously capture images until program termination
    while True:
        # Read the current frame
        ret, frame = cap.read()

        # Check if the image is read correctly
        if not ret:
            print("Failed to capture image")
            break

        # Crop the frame to the desired width range
        frame_cropped = frame[:, 0:1280]

        # Save the cropped image to the output folder
        image_path = os.path.join(output_folder, f"image_{frame_count + 1}.jpg")
        cv2.imwrite(image_path, frame_cropped)

        # Set the file permissions to 777
        os.chmod(image_path, 0o777)

        # Update the frame rate counter
        frame_count += 1

        # Break the loop if 15 seconds have passed
        if time.time() - start_time >= 15:
            break

    # Calculate and display the frame rate
    # elapsed_time = time.time() - start_time
    # fps = frame_count / elapsed_time

    # Release the camera
    cap.release()

    # Print the total number of frames captured
    print(f"Total frames captured: {frame_count}")


# Set the camera index and output folder
camera_index = 1  # 0 represents the default camera, can be changed based on the actual situation
output_folder = os.path.expanduser("/mnt/img/image/img2")  # Output folder path

# Call the clear_and_capture_images function
clear_and_capture_images(camera_index, output_folder)
