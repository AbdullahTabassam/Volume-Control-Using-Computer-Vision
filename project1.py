import cv2 as cv
import mediapipe as mp
import time
import HandTrackModule as htm

pTime = 0
cTime = 0 

cap = cv.VideoCapture(0)
detector = htm.handDetector()

while cap.isOpened():
    success, img = cap.read() 
    img = detector.FindHands(img)
    lmList = detector.fidPosition(img)
    if len(lmList) != 0:
        print(lmList[8])
    cTime = time.time()
    fps = 1/(cTime-pTime) 
    pTime = cTime
    cv.putText(img,str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3, (255,255,255),3)

    cv.imshow("image",img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()