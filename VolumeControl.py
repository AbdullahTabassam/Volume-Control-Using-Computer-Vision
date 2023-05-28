## Import Important Libraries
import cv2
import time
import mediapipe as mp
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import HandTrackModule as htm
import numpy as np
import math

## Time for FPS
pTime = 0       # Previous time
cTime = 0       # Current time

## Webcam Settings
wCam, hCam = 1280 , 720         # Window width and height
cap = cv2.VideoCapture(1)       # Set video capture object
cap.set(3, wCam)                # Set widhth
cap.set(4, hCam)                # Set height

## Use the module created
detector = htm.handDetector()

## Using 'pycaw' module for volume controls
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
min_vol=volume.GetVolumeRange()[0]
max_vol=volume.GetVolumeRange()[1]
print(min_vol,max_vol)

## While cthe camera object is open, run the loop
while cap.isOpened():
    success, img = cap.read() 
    img = cv2.flip(img,1)
    img = detector.FindHands(img)

    lmList = detector.fidPosition(img) 
    if len(lmList) != 0:
        x1 ,y1 = lmList[4][1], lmList[4][2]                         # Index finger tip coordinates
        x2 ,y2 = lmList[8][1], lmList[8][2]                         # Thumb tip coordinates
        cx ,cy = (x1+x2)//2,(y1+y2)//2                              # Midpoint
        length = math.hypot(x2-x1, y2-y1)                           # Distance between thumbtip and index finger tip
        cv2.circle(img,(x1,y1),15,(163, 24, 126),cv2.FILLED)        # Circle on the index finger tip
        cv2.circle(img,(x2,y2),15,(163, 24, 126),cv2.FILLED)        # Circle on the thumb tip
        cv2.circle(img,(cx,cy),15,(163, 24, 126),cv2.FILLED)        # Circle in the centre

        cv2.line(img,(x1,y1),(x2,y2),(163, 24, 126),3)              # Join the circles with line

        ## Change the color with volume increasing

        if length <150:
            cv2.circle(img,(cx,cy),15,(0, 200, 0),cv2.FILLED)
        if length >200:
            cv2.circle(img,(cx,cy),15,(0, 0, 200),cv2.FILLED)
        vol = np.interp(length,[50,250],[min_vol,max_vol])          # Change Scale for volume range in pycaw
        
        volume.SetMasterVolumeLevel(vol, None)                      # Set the colume depending on the distance between thumbtip and index finger tip
        cv2.rectangle(img,(80,620),(1200,660),(255,255,255),3)
        vol_bar = np.interp(vol,[min_vol,max_vol],[80,1200])        # Change Scale for volume bar

        vol_dig = np.interp(vol,[min_vol,max_vol],[0,100])          # Change Scale for volume digits

        if length <150:
            cv2.putText(img,f'Volume: {int(vol_dig)}',(80,575),cv2.FONT_HERSHEY_PLAIN,3,(0, 200, 0),3)  # Show digits in green
        if length >150:
            cv2.putText(img,f'Volume: {int(vol_dig)}',(80,575),cv2.FONT_HERSHEY_PLAIN,3,(0, 0, 200),3)  # Show digits in red
        
        cv2.rectangle(img,(80,620),(int(vol_bar),660),(255,255,255),cv2.FILLED)                         # Rectangle to contain volume bar

    ## Claculate Frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime) 
    pTime = cTime

    cv2.putText(img,f'FPS: {int(fps)}',(10,70),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),3) ## Show frame rate on screen corner
    cv2.imshow("image",img)                 ## Show the frames (video) in 'image' window

    if cv2.waitKey(1) == 27:                ## Press escape key to come out of the loop (close the camera window)
        break

cap.release()                               ## Close the capture
cv2.destroyAllWindows()                     ## Close all windows