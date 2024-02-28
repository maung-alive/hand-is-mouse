import cv2
import time
import HandTrackingModule as htm
import math
import mouse

width, height = 1920, 1080  # Your screen
startMouseX, startMouseY = mouse.get_position()
curCursorX, curCursorY = mouse.get_position()
sensitivity = 1.2    # Default Sensitivity

detector = htm.handDetector(trackCon=0.9, detectionCon=0.5)

dragging = False # Mouse drag don't change this
dragX, dragY = 0, 0 # To drag
doneDragging = False # Dragging true or false
startedDragging = False # to set first position to drag
startDragX, startDragY = 0, 0


capture = cv2.VideoCapture(0)

pTime = 0

def getNearest(integer):        # to make more stable the mouse cursor
    list = [i for i in str(integer)]

    list[-1] = 0
    nList = [str(i) for i in list]

    return int(''.join(nList))

while True:
    success, frame = capture.read()
    frame = cv2.flip(frame, 1)
    frame_width, frame_height = frame.shape[0], frame.shape[1]

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    frame = detector.findHands(frame, draw=True)
    lm = detector.findPosition(frame, draw=False)

    if len(lm[0]) != 0:
        thumbX, thumbY = lm[0][4][1], lm[0][4][2]
        fingerX, fingerY = lm[0][8][1], lm[0][8][2]
        midgerX, midgerY = lm[0][12][1], lm[0][12][2]
        thgerX, thgerY = lm[0][16][1], lm[0][16][2]

        cursorX, cursorY = lm[0][5][1], lm[0][5][2]
        midMidX, midMidY = lm[0][10][1], lm[0][10][2]

        cv2.circle(frame, (thumbX, thumbY), 10, (0,255,255), 2)
        cv2.circle(frame, (fingerX, fingerY), 10, (0,255,255), 2)
        cv2.circle(frame, (midgerX, midgerY), 10, (0,255,255), 2)
        cv2.circle(frame, (thgerX, thgerY), 10, (0,255,255), 2)

        thTofin_distance = math.hypot(fingerX-thumbX, fingerY-thumbY)
        thTomid_distance = math.hypot(midgerX-thumbX, midgerY-thumbY)
        thToth_distance = math.hypot(thgerX-thumbX, thgerY-thumbY)
        scrollDown = math.hypot(midgerX - fingerX, midgerY - fingerY)
        scrollUp = math.hypot(fingerX-cursorX, fingerY-cursorY)
        drag = math.hypot(midMidX-thumbX, midMidY-thumbY)

        # Mouse Move
        mouseX, mouseY = lm[0][6][1], lm[0][6][2]
        deltaX, deltaY = mouseX - startMouseX, mouseY - startMouseY
        curCursorX = int(width/frame_width * deltaX)*sensitivity
        curCursorY = int(width/frame_width * deltaY)*sensitivity
        startMouseX, startMouseY = mouseX,mouseY
        mouse.move(curCursorX, curCursorY, absolute=False, duration=0.1)

        # Mouse Drag
        if dragging:
            dragX, dragY = mouse.get_position()
            print(dragX, dragY)
            doneDragging = False
        else:
            if not doneDragging:
                mouse.drag(startDragX, startDragY, dragX, dragY, absolute=False, duration=0.1)
                doneDragging = True
                startedDragging = False

        if drag < 40:
            if not startedDragging:
                startDragX, startDragY = curCursorX, curCursorY
                startedDragging = True
            dragging = True
        elif drag > 40:
            dragging = False

        if scrollDown < 20:
            mouse.wheel(-1)
        elif scrollUp < 15:
            mouse.wheel(1)
        elif thTofin_distance < 25:
            mouse.click('left')
        elif thTomid_distance < 20:
            mouse.click('right')
        else:
            pass


    cv2.putText(frame, f"FPS: {int(fps)}", (10, 10), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 1)
    cv2.imshow("Camera", frame)
    cv2.waitKey(1)