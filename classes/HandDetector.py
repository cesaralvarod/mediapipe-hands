import mediapipe as mp
import cv2 as cv


class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionConf=0.5, tracingConf=0.5):
        self.mode = mode
        self.max_hands = maxHands
        self.min_detection_confidence = detectionConf
        self.min_tracing_confidence = tracingConf

        self.mediapipe_hands = mp.solutions.hands
        self.hands = self.mediapipe_hands.Hands(model_complexity=0, min_detection_confidence=self.min_detection_confidence,min_tracking_confidence=self.min_tracing_confidence)
        self.draw = mp.solutions.drawing_utils
        self.landmarks = [4, 8, 12, 16, 20]

    def find_hands(self, frame, drawHand=True):
        img_color = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        self.results = self.hands.process(img_color)
        

        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                if drawHand:
                    self.draw.draw_landmarks(
                        frame, hand, self.mediapipe_hands.HAND_CONNECTIONS)

        return frame
      

    def find_position(self, frame,drawHand=True):
        box = []

        if self.results.multi_hand_landmarks:
            hands_number = len(self.results.multi_hand_landmarks)
            sum=0
            mult=1
            
            for i in range(hands_number):
              hand = self.results.multi_hand_landmarks[i]
              
              x_list = []
              y_list = []
              hand_list = []

              for id, lm in enumerate(hand.landmark):
                  height, width, c = frame.shape
                  cx, cy = int(lm.x*width), int(lm.y*height)
                  x_list.append(cx)
                  y_list.append(cy)
                  hand_list.append([id, cx, cy])
                  if drawHand:
                      cv.circle(frame, (cx, cy), 5, (0, 0, 0),
                              cv.FILLED)  # Draw a circle

              xmin, xmax, ymin, ymax = min(x_list), max(
                x_list), min(y_list), max(y_list)

              fingers_up = self.get_fingers_up(hand_list,xmin-30, ymin-30 )
              sum = sum + fingers_up
              mult = mult*fingers_up

              box = xmin, ymin, xmax, ymax

              if drawHand:
                  cv.rectangle(frame, (xmin-20, ymin-20),
                             (xmax+20, ymax+20), (0, 255, 0), 2)
                  cv.putText(frame,str(fingers_up), (xmin-30, ymin-30),cv. FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
                  
            cv.putText(frame,"Suma: "+ str(sum), (40, 50),cv. FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv.putText(frame,"Multiplicacion: "+ str(mult), (40, 100),cv. FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)   

        return  box
      
    def get_fingers_up(self, hand,x,y):
      fingers=[]
      is_hand_right = True
      
      if hand[17][1]>hand[1][1]:
          is_hand_right = False
      elif hand[17][1]<hand[1][1]:
          is_hand_right = True
      
      for lm in self.landmarks:
        if lm <21:
          if hand[lm]:
            if lm==4:
              if is_hand_right:
                if hand[lm][1]>hand[lm-1][1] and hand[lm][2]< hand[lm-1][2]:
                    fingers.append(hand[lm])
              else: 
                if hand[lm][1]<hand[lm-1][1] and hand[lm][2]< hand[lm-1][2]:
                    fingers.append(hand[lm])
            else:
              if hand[lm][2]< hand[lm-1][2]:
                fingers.append(hand[lm])
              
      return len(fingers)

    def distance(self, p1, p2, frame, drawHand=True, r=15, t=3):
        x1, y1 = self.list[p1][1:]
        x2, y2 = self.list[p2][1:]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        if drawHand:
            cv.line(frame, (x1, y1), (x2, y2), (0, 0, 255), t)
            cv.circle(frame, (x1, y1), r, (0, 0, 255), cv.FILLED)
            cv.circle(frame, (x2, y2), r, (0, 0, 255), cv.FILLED)
            cv.circle(frame, (cx, cy), r, (0, 0, 255), cv.FILLED)

        length = math.hypot(x2-x1, y2-y1)

        return length, [x1, y1, x2, y2, cx, cy]
