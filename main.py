import cv2
import time
import HandTrackingModule as htm
import math
import mouse

width, height = 1920, 1080
detector = htm.handDetector()

capture = cv2.VideoCapture(0)
capture.set(3, 480)
capture.set(4, 640)

pTime = 0

while True:
    success, frame = capture.read()
    frame = cv2.flip(frame, 1)
    frame_width, frame_height = frame.shape[0], frame.shape[1]

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    frame = detector.findHands(frame)
    lm = detector.findPosition(frame, draw=False)

    if len(lm[0]) != 0:
        thumbX, thumbY = lm[0][4][1], lm[0][4][2]
        fingerX, fingerY = lm[0][8][1], lm[0][8][2]
        midgerX, midgerY = lm[0][12][1], lm[0][12][2]

        posX, posY = lm[0][5][1], lm[0][5][2]
        curX, curY = mouse.get_position()
        mouseX = int(width/frame_width * posX)
        mouseY = int(height/frame_height * posY)
        mouse.move(mouseX, mouseY, absolute=True)

        cv2.circle(frame, (thumbX, thumbY), 10, (0,255,255), 2)
        cv2.circle(frame, (fingerX, fingerY), 10, (0,255,255), 2)
        cv2.circle(frame, (midgerX, midgerY), 10, (0,255,255), 2)

        thTofin_distance = math.hypot(fingerX-thumbX, fingerY-thumbY)
        thTomid_distance = math.hypot(midgerX-thumbX, midgerY-thumbY)

        if thTofin_distance < 50:
            mouse.click('left')
        elif thTomid_distance < 50:
            mouse.click('right')

    cv2.putText(frame, f"FPS: {int(fps)}", (50, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 1)
    cv2.imshow("Camera", frame)
    cv2.waitKey(1)

capture.release()