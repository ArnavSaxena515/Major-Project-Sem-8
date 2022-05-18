import cv2
import mediapipe as mp
import time
import math
import numpy as np


class HandFinder:
    def __init__(self, mode=False, number_of_hands=2, detection_confidence=0.5, tracking_confidence=0.5):

        self.mode = mode
        self.number_of_hands = number_of_hands
        self.number_of_hands = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIndices = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        transform_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.hand_info = self.hands.process(transform_image)
        # print(self.results.multi_handedness)

        if self.hand_info.multi_hand_landmarks:
            for hand_landmarks in self.hand_info.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, hand_landmarks, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        self.lmList = []
        if self.hand_info.multi_hand_landmarks:
            detected_hand = self.hand_info.multi_hand_landmarks[handNo]
            for index, lm in enumerate(detected_hand.landmark):
                height, width, c = img.shape
                x_coord, y_coord = int(lm.x * width), int(lm.y * height)
                self.lmList.append([index, x_coord, y_coord])

                if draw:
                    cv2.circle(img, (x_coord, y_coord), 15, (255, 0, 255), cv2.FILLED)
        return self.lmList

    def active_fingers(self):
        fingers = []
        # Thumb
        if self.lmList[self.tipIndices[0]][1] < self.lmList[self.tipIndices[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for index in range(1, 5):
            if self.lmList[self.tipIndices[index]][2] < self.lmList[self.tipIndices[index] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def distance_tracker(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]


