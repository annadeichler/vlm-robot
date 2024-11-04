import cv2
import requests

class CameraHandler:
    def __init__(self, camera_index=1, quality='720p'):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index)
        
        # Define pre-set quality settings
        quality_settings = {
            '480p': (640, 480),
            '720p': (1280, 720),
            '1080p': (1920, 1080),
            '1440p': (2560, 1440),
            '4k': (3840, 2160)
        }
        
        # Set the width and height based on the selected quality
        if quality in quality_settings:
            width, height = quality_settings[quality]
        else:
            width, height = quality_settings['720p']  # Default to 720p if invalid quality
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def stream_video(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            cv2.imshow('Video Stream', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def take_screenshot(self, file_format='png', screenshot_path=None):
        ret, frame = self.cap.read()
        if ret:
            valid_formats = ['jpg', 'jpeg', 'png']
            if file_format not in valid_formats:
                print(f"Invalid format '{file_format}'. Defaulting to 'png'.")
                file_format = 'png'
            if screenshot_path is None:
                screenshot_path = f'screenshot.{file_format}'
            cv2.imwrite(screenshot_path, frame)
            return screenshot_path
        return None

    def preprocess_frame_for_vlm(self):
        ret, frame = self.cap.read()  # Capture the current frame from the camera
        if not ret:
            print("Failed to capture image from camera.")
            return None
        
        # Resize the image to a fixed size (e.g., 224x224) for VLM input
        resized_frame = cv2.resize(frame, (224, 224))
        
        # Normalize the image data to the range [0, 1]
        normalized_frame = resized_frame / 255.0

        # Convert the image to a format suitable for VLM (e.g., adding a batch dimension)
        image_tensor = normalized_frame.astype('float32')
        image_tensor = image_tensor.reshape((1, 224, 224, 3))  # Add batch dimension
        
        return image_tensor

    def display_image_tensor(self, image_tensor):
        if image_tensor is not None:
            # Convert back to a displayable format (removing batch dimension)
            display_frame = image_tensor[0] * 255.0  # Scale back to [0, 255]
            display_frame = display_frame.astype('uint8')  # Convert to uint8
            cv2.imshow('Image Tensor', display_frame)
            cv2.waitKey(0)  # Wait for a key press to close the window
        else:
            print("No frame to display.")

    def send_to_llama(image_tensor):
        # Convert the tensor to a format suitable for the API (e.g., JSON)
        payload = {
            'image': image_tensor.tolist()  # Convert numpy array to list
        }
        # Make the API call (replace 'API_URL' with the actual endpoint)
        response = requests.post('API_URL', json=payload)
        return response.json()

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    camera_handler = CameraHandler(quality='720p')  # Example for 1080p quality
    print("Starting video stream. Press 'q' to quit.")
    camera_handler.stream_video()
    screenshot_path = camera_handler.take_screenshot(file_format='jpg')  # Example for jpg format
    if screenshot_path:
        print(f"Screenshot saved at: {screenshot_path}")
    else:
        print("Failed to take screenshot.")
    image_tensor = camera_handler.preprocess_frame_for_vlm()
    camera_handler.display_image_tensor(image_tensor)
    print(f"Output of the image tensor for LLaMA: {image_tensor}")
    camera_handler.release()