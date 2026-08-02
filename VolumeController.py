import cv2
import time
import math
import numpy as np
from HandTrackingModule import handDetector
from pycaw.pycaw import AudioUtilities

cap = cv2.VideoCapture(1)

detector = handDetector()

device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume
minvol =  volume.GetVolumeRange()[0]
maxvol = volume.GetVolumeRange()[1]

ptime = 0

while True:

    ok, frame = cap.read()

    frame = detector.findhands(frame)
    lmlist = detector.findpoints(frame)

    if len(lmlist) != 0:
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2

        # Hand Range 25 - 190
        # Volume Rage -65.25 - 0

        length = math.hypot(x2 - x1, y2 - y1)
        vol = np.interp(length, [25, 190], [minvol, maxvol])
        volBar = int(np.interp(length, [25, 190], [400, 150]))
        volPct = int(np.interp(length, [25, 190], [0, 100]))
        volume.SetMasterVolumeLevel(vol, None)

        colorBar = (255, 255, 0)
        if volPct == 0:
            colorBar = (255, 0, 0) 
        elif volPct == 100:
            colorBar = (0, 0, 255)
        

        cv2.circle(frame, (x1, y1), 15, colorBar, cv2.FILLED)
        cv2.circle(frame, (x2, y2), 15, colorBar, cv2.FILLED)
        cv2.line(frame, (x1, y1), (x2, y2), colorBar, 3)
       

        if length < 25:
            cv2.circle(frame, (cx, cy), 15, (255, 0, 255), cv2.FILLED)


        # Volume bar: border
        cv2.rectangle(frame, (50, 150), (85, 400), colorBar, 2)
        # Volume bar: dynamic fill (blue -> filled from bottom up)
        cv2.rectangle(frame, (50, volBar), (85, 400), colorBar, cv2.FILLED)
        # Volume % label
        cv2.putText(frame, f"{volPct}%", (40, 430), cv2.FONT_HERSHEY_PLAIN, 1.5, colorBar, 2)


    ctime = time.time()
    fps = 1 / (ctime - ptime) if ptime != 0 else 0
    ptime = ctime
            
    cv2.putText(frame, f"FPS: {fps:.2f}", (40, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 1)
    cv2.imshow("Frame", frame)
            
    if cv2.waitKey(1) == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()