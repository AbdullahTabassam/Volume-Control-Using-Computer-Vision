# Hand Gesture Volume Control

This repository contains a Python script that utilizes the MediaPipe and OpenCV libraries to detect hand gestures and control the volume of the computer using the PyCaw library. The script is designed to run on Windows operating systems.

![HandGesture](handGesture.gif)

## Prerequisites

Before running the script, make sure you have the following dependencies installed:

1. Python 3.x
2. MediaPipe
3. OpenCV
4. PyCaw

To install these dependencies, you can use the following commands:

    pip install mediapipe
    pip install opencv-python
    pip install pycaw

## How It Works

The script uses the computer's webcam to capture video frames and then applies hand tracking using the MediaPipe library. Once the hand landmarks are detected, the script determines the hand gesture based on the relative positions of the fingers and palm.

The recognized hand gestures are:

1. Thumb and index finger open: Increase volume
2. Thumb and index finger closed: Decrease volume

To control the volume, the script utilizes the PyCaw library, which provides a high-level interface to manipulate the Windows Core Audio API. It retrieves the default audio playback device and adjusts the volume accordingly based on the detected hand gestures.
Usage

### Step 1:
Clone this repository to your local machine:

    git clone https://github.com/AbdullahTabassam/Volume-Control-Using-Computer-Vision.git

### Step 2:
Navigate to the project directory:
    
    cd Volume-Control-Using-Computer-Vision

### Step 3:
Run the script:

    python VolumeControl.py


The script will start capturing video frames from your webcam and display the output in a window. Make sure your hand is clearly visible in the frame. Also play around to set you specific camera.

    cap = cv2.VideoCapture(x) ... x = 1,2,3

### Step 4:
Perform the hand gestures to control the volume:

1. Open thumb and index finger: Increase volume.
2. Close thumb and index finger: Decrease volume.

As you perform the gestures, the script will adjust the volume accordingly.

### Step 5:
Press the 'ESC' key to close the camera window.

## Customization

If you want to customize the script or integrate it into your own project, you can modify the python file. The script is well-commented to help you understand the implementation and make any necessary changes.