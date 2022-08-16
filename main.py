import cv2 as cv
from classes.HandDetector import *


if __name__ == "__main__":
    ptime = 0

    cap = cv.VideoCapture(0)
    detector = HandDetector()

    while True:
        ret, frame = cap.read()
        frame = detector.find_hands(frame)
        box = detector.find_position(frame)
        # fingers_num = detector.get_fingers_up()


        # cv.putText(frame, str(fingers_num), (10, 70),
        #            cv. FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv.imshow("Hands Tracer", frame)
        k = cv.waitKey(1)

        if k == 27:
            break

    cap.release()
    cv.destroyAllWindows()
