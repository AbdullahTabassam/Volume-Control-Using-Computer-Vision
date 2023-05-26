import cv2 as cv
import mediapipe as mp
import time

class handDetector():
    def __init__(self):

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def FindHands(self, img,draw = True):
        imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
                    
        return img


    def fidPosition(self, img, handNo=0, draw=True):
        
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x * w) , int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv.circle(img,(cx,cy),4,(163, 24, 126),cv.FILLED)
        return lmList
    

def main():
    pTime = 0
    cTime = 0 

    cap = cv.VideoCapture(0)
    detector = handDetector()

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


if __name__ == "__main__":
    main()