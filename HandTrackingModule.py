import cv2
import time
import mediapipe as mp

mpDraw = mp.solutions.drawing_utils
mphands = mp.solutions.hands
hand = mphands.Hands()

cap = cv2.VideoCapture(1)

ptime = 0
while True:

    ok, frame = cap.read()

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hand.process(img)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame, handLms, mphands.HAND_CONNECTIONS)

    ctime = time.time()
    fps = 1 / (ctime - ptime) if ptime != 0 else 0
    ptime = ctime

    cv2.putText(frame, f"FPS: {fps:.2f}", (40, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 1)
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()