import cv2
import mediapipe as mp
import time

class handdetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        
        if self.results.multi_hand_landmarks:
            for handsLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handsLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self,img,handNo=0,draw=False):

        lmList=[]
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                #print(id, lm)   #landmark coordinates 

                h, w, c=img.shape  # landmarks in decimal values 
                cx,cy=int(lm.x*w), int(lm.y*h)
                #print(id,cx, cy)  #landmark coordinates in pixles 
                #draw circle on landmark 
                lmList.append([id,cx,cy])
                if draw:
                
                    cv2.circle(img,(cx, cy),15,(255, 0, 255), cv2.FILLED)
        return lmList
def main():
    Ptime = 0
    Ctime = 0
    cap = cv2.VideoCapture(0)
    detector = handdetector()
    
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList=detector.findPosition(img)
        if len(lmList)!=0:
            print(lmList[4])
        
        Ctime = time.time()
        fps = 1 / (Ctime - Ptime)
        Ptime = Ctime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()
