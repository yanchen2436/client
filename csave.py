import cv2
import time
import os

def capture_images(camera_index, output_folder):
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

        # Update the frame rate counter
        frame_count += 1

    # Calculate and display the frame rate
    elapsed_time = time.time() - start_time
    #fps = frame_count / elapsed_time

    # Release the camera
    cap.release()

# Set the camera index and output folder
camera_index = 1  # 0 represents the default camera, can be changed based on the actual situation
output_folder = os.path.expanduser("~/share/image/img")  # Output folder path

# Call the capture_images function
capture_images(camera_index, output_folder)
