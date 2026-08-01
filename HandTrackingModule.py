import cv2
import time
import mediapipe as mp


class handDetector():
    def __init__(self, mode=False, num_hands = 2, detection_conf = 0.5, tracking_conf = 0.5):

        self.mode = mode
        self.num_hands = num_hands
        self.detection_conf = detection_conf
        self.tracking_conf = tracking_conf

        self.mpDraw = mp.solutions.drawing_utils
        self.mphands = mp.solutions.hands
        self.hand = self.mphands.Hands(static_image_mode=self.mode,
                                      max_num_hands=self.num_hands,
                                      min_detection_confidence=self.detection_conf,
                                      min_tracking_confidence=self.tracking_conf)

    def findhands(self, frame, draw = True):
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.result = self.hand.process(frameRGB)
        
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mphands.HAND_CONNECTIONS)

        return frame

    def findpoints(self, frame):
        lmlist = []
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                for id, lms in enumerate(handLms.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lms.x * w), int(lms.y * h)

                    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
                    lmlist.append([id, cx, cy])

        return lmlist




def main():
    cap = cv2.VideoCapture(1)

    ptime = 0
    ctime = 0

    detector = handDetector()
    while True:

        ok, frame = cap.read()

        frame = detector.findhands(frame)
        lmlist = detector.findpoints(frame)

        ctime = time.time()
        fps = 1 / (ctime - ptime) if ptime != 0 else 0
        ptime = ctime
        
        cv2.putText(frame, f"FPS: {fps:.2f}", (40, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 1)
        cv2.imshow("Frame", frame)
        
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

