### Identify Cameras by Index with Descriptions
import cv2
import pyudev

# Create a context for pyudev
context = pyudev.Context()

# Check camera indices and print their availability and descriptions
for i in range(10):  # Check the first 10 indices
    try:
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera index {i} is available.")
            
            # Get device information using a different method
            device_info = cv2.getBuildInformation()
            if 'Video I/O' in device_info:
                print("Camera index {} description: {}".format(i, device_info.split('Video I/O')[1].split('\n')[0].strip()))
            else:
                print(f"Camera index {i} description: Unknown model")
    except Exception as e:
        print(f"Error opening camera index {i}: {e}")
        continue
        
    cap.release()