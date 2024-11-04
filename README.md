## VML robot 
This is continuation of digital futures demo.
### Requirements
```
furhat-remote-api
opencv-python
requests
base64
threading
```
### Furhat Remote API
more information on https://docs.furhat.io/remote-api/
possible to write all conversation control in python script 
### Camera Script Installation

To set up the camera class, install the required dependencies for OpenCV (cv2), follow these steps:

1. **Dependencies**: Install cv2 dependencies:
   ```bash
   sudo apt-get update
   sudo apt-get install libgtk2.0-dev pkg-config
    ```

2. **Install OpenCV w/GUI and requests for API calls**: Run the following command in your terminal:
   ```bash
    pip install opencv-python-headless requests pyudev
     ```

3. **Verify the installation**: You can verify that OpenCV is installed correctly by running the following command in a Python shell:
   ```python
   import cv2
   print(cv2.__version__)
   ```


This will display the version of OpenCV installed, confirming that the installation was successful.




### run virtual furhat with furhat_cooks.py
1. Open Furhat SDK
2. Click "Launch Virtual Furhat"
3. Click "Start Remote API" in the Furhat Studio window
4. In the same direcotry as furhat_cooks.py, run a separate python process ```python -m http.server 8000``` This serves TTS wav files.
5. Run ```python furhat_cooks.py```

