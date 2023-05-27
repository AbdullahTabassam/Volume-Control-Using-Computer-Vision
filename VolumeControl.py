import cv2
import time
import mediapipe as mp
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import HandTrackModule as htm
import numpy as np
import math


pTime = 0
cTime = 0 

wCam, hCam = 1280 , 720
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

min_vol=volume.GetVolumeRange()[0]
max_vol=volume.GetVolumeRange()[1]
print(min_vol,max_vol)


while cap.isOpened():
    success, img = cap.read() 
    img = cv2.flip(img,1)
    img = detector.FindHands(img)

    lmList = detector.fidPosition(img) 
    if len(lmList) != 0:
        x1 ,y1 = lmList[4][1], lmList[4][2]
        x2 ,y2 = lmList[8][1], lmList[8][2]
        cx ,cy = (x1+x2)//2,(y1+y2)//2
        length = math.hypot(x2-x1, y2-y1)
        cv2.circle(img,(x1,y1),15,(163, 24, 126),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(163, 24, 126),cv2.FILLED)
        cv2.circle(img,(cx,cy),15,(163, 24, 126),cv2.FILLED)

        cv2.line(img,(x1,y1),(x2,y2),(163, 24, 126),3)
        if length <150:
            cv2.circle(img,(cx,cy),15,(0, 200, 0),cv2.FILLED)
        if length >200:
            cv2.circle(img,(cx,cy),15,(0, 0, 200),cv2.FILLED)
        vol = np.interp(length,[50,250],[min_vol,max_vol])
        
        volume.SetMasterVolumeLevel(vol, None)
        cv2.rectangle(img,(80,620),(1200,660),(255,255,255),3)
        vol_bar = np.interp(vol,[min_vol,max_vol],[80,1200])

        if length <150:
            cv2.putText(img,f'Volume: {int(fps)}',(80,575),cv2.FONT_HERSHEY_PLAIN,3,(0, 200, 0),3)
        if length >150:
            cv2.putText(img,f'Volume: {int(fps)}',(80,575),cv2.FONT_HERSHEY_PLAIN,3,(0, 0, 200),3)
        
        cv2.rectangle(img,(80,620),(int(vol_bar),660),(255,255,255),cv2.FILLED)

    cTime = time.time()
    fps = 1/(cTime-pTime) 
    pTime = cTime

    cv2.putText(img,f'FPS: {int(fps)}',(10,70),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),3)
    cv2.imshow("image",img)

    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()