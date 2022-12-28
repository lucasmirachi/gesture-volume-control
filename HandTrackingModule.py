import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, static_image_mode = False, max_num_hands = 2, model_complexity = 1, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.model_complexity = model_complexity
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        #Creating an object for the class "Hands"
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.static_image_mode, self.max_num_hands, self.model_complexity, self.min_detection_confidence, self.min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #To check if something was detected or not
        #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPositions(self, img, handNumber = 0, draw = True):
        landmarkList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNumber]

        #* # To get the landmark information from each hand
        # each landmark has an id and its correspondent x and y positions
            for id,lm in enumerate(myHand.landmark):
                #print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                #print(id, cx, cy)
                landmarkList.append([id, cx, cy])

                if draw:
                    cv2.circle(img, (cx,cy), 15, (0,0,255), cv2.FILLED)
                        
                '''To highligh a specific finger, change the "id" number according to the hand landmarks figure (https://mediapipe.dev/images/mobile/hand_landmarks.png)
                if id == 4: # 4 == thumb tip
                    cv2.circle(img, (cx,cy), 15, (255,0,0), cv2.FILLED)
                if id == 8: # 8 == Index finger tip
                    cv2.circle(img, (cx,cy), 15, (255,0,0), cv2.FILLED)'''

        return landmarkList
                
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        landmarksList = detector.findPositions(img)

        if len(landmarksList) != 0:
            print(landmarksList[4])

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,255), 3) 

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

#This means: "you if you're running this script"
if __name__ == "__main__":
    main()