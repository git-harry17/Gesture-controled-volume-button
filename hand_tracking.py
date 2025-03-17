#hand tracking
import cv2
import mediapipe as mp
import time 
#-----------------------------------------------------------------------------------------------------------------------
mpHands=mp.solutions.hands

hands=mpHands.Hands()

#mp draw for drawing the hand on screen  
mpDraw=mp.solutions.drawing_utils           
Ptime=0
Ctime=0

#-----------------------------------------------------------------------------------------------------------------------
#RUN WEB CAM
cap = cv2.VideoCapture(0)
while True: 
    #capturing hands and processing the cordinates
    success,img=cap.read()
    #converting to rgb image 
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB )

    #process all frames and provides result :
    results=hands.process(imgRGB)

    #print(results.multi_hand_landmarks)

    #if getting multiple hands extract the info of each hand
    if results.multi_hand_landmarks:
        #this loop is for every hand -----> 
        for handsLms in results.multi_hand_landmarks: 
            #for every index number of landmark -----> 0 to 20 
            for id, lm in enumerate(handsLms.landmark):
                #print(id, lm)   #landmark coordinates 

                h, w, c=img.shape  # landmarks in decimal values 
                cx,cy=int(lm.x*w), int(lm.y*h)
                print(id,cx, cy)  #landmark coordinates in pixles 
                #draw circle on landmark 
                if(id==0):
                    cv2.circle(img,(cx, cy),15,(255, 0, 255), cv2.FILLED)

            #this draws hand connections
            mpDraw.draw_landmarks(img, handsLms, mpHands.HAND_CONNECTIONS)

    #calculating frames 
    Ctime=time.time()
    fps=1/(Ctime-Ptime)
    Ptime=Ctime        

#putting fps on screen 
    cv2.putText(img,str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN,3  ,(255, 0, 255), 3)
    cv2.imshow("Image",img) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#-----------------------------------------------------------------------------------------------------------------------