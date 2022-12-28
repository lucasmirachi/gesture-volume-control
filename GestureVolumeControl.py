import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import math
import numpy as np
from subprocess import call

cap = cv2.VideoCapture(0)

detector = htm.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    landmarksList = detector.findPositions(img, draw=False)
    if len(landmarksList) != 0:
        #for this project, according to the finger's id numbers provided by the mediapipe documentation, we'll only need the values from id4(thumb_tip) and id8(index_finger_tip)
        #print(landmarksList)
        thumb_x, thumb_y = landmarksList[4][1], landmarksList[4][2]
        index_x, index_y = landmarksList[8][1], landmarksList[8][2]
        center_x, center_y = (thumb_x+index_x)//2, (thumb_y+index_y)//2

        #to highlight the fingers with a circle
        cv2.circle(img, (thumb_x, thumb_y), 15, (0,0,255), cv2.FILLED)
        cv2.circle(img, (index_x, index_y), 15, (0,0,255), cv2.FILLED)

        #to create a line between the two fingers
        cv2.line(img, (thumb_x, thumb_y), (index_x, index_y), (255,255,0), 3)

        #to know the actual lenght of this line between the two fingers
        lenght = math.hypot((thumb_x-index_x), (thumb_y-index_y))
        #print(lenght)

        # printing the length, it was noticed that, for my case, the max length was around 300 and the minimal around 50
        # so now it is needed to convert the range 50 - 300 to 0 - 100
        volume = np.interp(lenght,[50,300],[0,100]) 
        #print(volume)

        #to change the volume in linux Ubuntu 22.04
        call(["amixer", "-D", "pulse", "sset", "Master", str(volume) + "%"])

        #to draw the volume bar 
        cv2.rectangle(img, (center_x-200, center_y-100), (center_x+200, center_y-50), (255,255,0), 3)
        volume_bar = np.interp(volume,[0,100],[center_x-200,center_x+200])
        cv2.rectangle(img, (center_x-200, center_y-100), (int(volume_bar), center_y-50), (255,255,0), cv2.FILLED)
        cv2.putText(img, f'Volume: {int(volume)}%' , (center_x-150,center_y-125), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0), 3)


    pTime = 0
    cTime = 0
    #To calculate the FPS
    cTime = time.time()
    fps = 1/(cTime - pTime) #cTime = 'Current Time' and pTime = 'Previous Time'
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}' , (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,255), 3) 

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break