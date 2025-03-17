import cv2
import time
import numpy as np
import HandTrackingModule as htm 
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam,hCam=640,480
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

Ptime = 0

detector=htm.handdetector(detectionCon=0.7)



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
minVol=volRange[0]
maxVol=volRange[1]

vol=0
volbar=400
volper=0
while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        #print(lmList[4],lmList[8])

        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx,cy=(x1+x2)//2 ,(y1+y2)//2

        cv2.circle(img,(x1, y1),10,(255, 0, 255), cv2.FILLED)
        cv2.circle(img,(x2, y2),10,(255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),2)
        cv2.circle(img,(cx, cy),10,(255,0,255),   cv2.FILLED)

        leng =math.hypot(x2-x1,y2-y1)
        print(leng)

        #hand range = 50 to 100
        #vol range is -60 to 0

        vol=np.interp(leng,[50,300],[minVol,maxVol])
        volbar=np.interp(leng,[50,300],[400,150])
        volper=np.interp(leng,[50,300],[0,100])
        print(int(leng),vol)
        volume.SetMasterVolumeLevel(vol, None)


        if leng<50 :
             cv2.circle(img,(cx, cy),10,(0,255,0),   cv2.FILLED)
             cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        
        if leng>150 :
             cv2.circle(img,(cx, cy),10,(0,0,255),   cv2.FILLED)
             cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
             
             
    
    cv2.rectangle(img,(50,150),(85,400),(0,255,0,),3)
    cv2.rectangle(img,(50,int(volbar)),(85,400),(0,255,0,),cv2.FILLED)
    cv2.putText(img,f'{int(volper)}%',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,250,0),3)
    Ctime = time.time()
    fps = 1 / (Ctime - Ptime)
    Ptime = Ctime
    cv2.putText(img, f'FPS: {str(int(fps))}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cv2.imshow("Img",img)
    cv2.waitKey(1 ) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break