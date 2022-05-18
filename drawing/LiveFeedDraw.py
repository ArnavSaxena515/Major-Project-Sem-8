import cv2
import numpy as np
# from cvzone.HandTrackingModule import HandDetector as htm
import cvzone.HandTrackingModule as htm


def run_drawer():
    headerImage = cv2.imread("Canvas.png")

    # Capture the video camera
    video_feed = cv2.VideoCapture(0)
    # Set dimensions for webcam window
    video_feed.set(3, 1280)
    video_feed.set(4, 720)

    brush_thickness = 15
    eraser_thickness = 50
    draw_color = (255, 0, 255)
    red_color = (255, 0, 0)
    blue_color = (0, 0, 255)
    pink_color = (255, 0, 255)

    hand_detect = htm.HandFinder(detection_confidence=0.85, number_of_hands=1)
    x_prev, y_prev = 0, 0
    imgCanvas = np.zeros((720, 1280, 3), np.uint8)
    while True:
        # 1. Import image
        success, live_image = video_feed.read()

        live_image = cv2.flip(live_image, 1)  # Flip the image to solve the mirror issue
        live_image[0:128, 0:1280] = headerImage

        # 2 Find Hand Landmarks
        live_image = hand_detect.findHands(live_image)
        hand_landmarks = hand_detect.findPosition(live_image, draw=False)

        if len(hand_landmarks) != 0:
            # print(landmarks)
            # Tip of index and middle fingers
            x1, y1 = hand_landmarks[8][1:]  # index finger tip
            x2, y2 = hand_landmarks[12][1:]  # middle finger tip

            # 3 Check which fingers are up
            fingers_active = hand_detect.active_fingers()
            # print(fingers_up)

            # 4 If selection mode - Two fingers are up
            if fingers_active[1] and fingers_active[2]:
                cv2.rectangle(live_image, (x1, y1 - 15), (x2, y2 + 15), draw_color, cv2.FILLED)
                if y1 < 128:  # value of header
                    if 15 < x1 < 215:
                        draw_color = (0, 0, 255)
                        print("RED")
                        print(draw_color)
                    elif 300 < x1 < 500:
                        draw_color = (255, 0, 0)
                        print("BLUE")
                        print(draw_color)
                    elif 630 < x1 < 830:
                        draw_color = pink_color
                        print("PINK")
                        print(draw_color)
                    elif 1115 < x1 < 1260:
                        draw_color = (0, 0, 0)
                        print("ERASER")
                x_prev, y_prev = x1, y1


            # 5 If drawing mode - Index finger is up
            elif fingers_active[1] and fingers_active[2] == False:
                cv2.circle(live_image, (x1, y1), 15, draw_color, cv2.FILLED)
                if x_prev == 0 and y_prev == 0:  # first frame
                    x_prev, y_prev = x1, y1
                if draw_color == (0, 0, 0):
                    cv2.line(live_image, (x_prev, y_prev), (x1, y1), draw_color, thickness=eraser_thickness)
                    cv2.line(imgCanvas, (x_prev, y_prev), (x1, y1), draw_color, thickness=eraser_thickness)

                # cv2.line(img, (xp, yp), (x1, y1), drawColor, thickness=brushThickness)
                cv2.line(imgCanvas, (x_prev, y_prev), (x1, y1), draw_color, thickness=brush_thickness)
                x_prev, y_prev = x1, y1
            else:
                x_prev, y_prev = x1, y1

        gray_image = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, image_inverse = cv2.threshold(gray_image, 50, 255, cv2.THRESH_BINARY_INV)
        image_inverse = cv2.cvtColor(image_inverse, cv2.COLOR_GRAY2BGR)
        live_image = cv2.bitwise_and(live_image, image_inverse)
        live_image = cv2.bitwise_or(live_image, imgCanvas)
        cv2.imshow("Image", live_image)
        # key = cv2.waitKey(0)
        # if key == ord('q') or key == ord('Q'):
        #     break
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    return
    #
