import cv2
import time
import math
import numpy as np
from HandTrackingModule import handDetector

cap = cv2.VideoCapture(1)

ptime = 0

detector = handDetector()

from pycaw.pycaw import AudioUtilities
device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume
minvol =  volume.GetVolumeRange()[0]
maxvol = volume.GetVolumeRange()[1]
print(minvol)
print(maxvol)

while True:

    ok, frame = cap.read()

    frame = detector.findhands(frame)
    lmlist = detector.findpoints(frame)

    if len(lmlist) != 0:
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2

        cv2.circle(frame, (x1, y1), 15, (255, 255, 0), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 15, (255, 255, 0), cv2.FILLED)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 0), 3)

        length = math.hypot(x2 - x1, y2 - y1)

        # Hand Range 30 - 240
        # Volume Rage -65.25 - 0

        vol = np.interp(length, [25, 190], [minvol, maxvol])
        volume.SetMasterVolumeLevel(vol, None)

        if length < 22:
            cv2.circle(frame, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

    ctime = time.time()
    fps = 1 / (ctime - ptime) if ptime != 0 else 0
    ptime = ctime
            
    cv2.putText(frame, f"FPS: {fps:.2f}", (40, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 1)
    cv2.imshow("Frame", frame)
            
    if cv2.waitKey(1) == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()