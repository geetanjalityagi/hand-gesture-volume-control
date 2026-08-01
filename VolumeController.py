import cv2
import time
from HandTrackingModule import handDetector

cap = cv2.VideoCapture(1)

ptime = 0

detector = handDetector()
while True:

    ok, frame = cap.read()

    frame = detector.findhands(frame)
    lmlist = detector.findpoints(frame)

    if len(lmlist) != 0:
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]

        cv2.circle(frame, (x1, y1), 15, (255, 255, 0), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 15, (255, 255, 0), cv2.FILLED)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 0), 3)

    ctime = time.time()
    fps = 1 / (ctime - ptime) if ptime != 0 else 0
    ptime = ctime
            
    cv2.putText(frame, f"FPS: {fps:.2f}", (40, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 1)
    cv2.imshow("Frame", frame)
            
    if cv2.waitKey(1) == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()