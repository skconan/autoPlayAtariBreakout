import cv2
import numpy as np
import math
import pyautogui
from operator import itemgetter
import time

imgColor = None
resImg = None
widthScreen = 1920
heightScreen = 1080






def get_position(event, x, y, flags, param):
    global imgColor
    if event == cv2.EVENT_MOUSEMOVE and imgColor is not None:
        print(x, y, imgColor[y, x])

def get_color():
    global imgColor
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', get_position)
    while True:
        imgColor = screenshotCapture()
        if imgColor is None:
            continue
        cv2.imshow('image', imgColor)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break

def screenshot_capture():
    img = pyautogui.screenshot(
        region=(int(widthScreen / 2), 240, int(widthScreen / 2), heightScreen - 240))
    img = np.array(img)

    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def circle_area(radius):
    return math.pi * (radius**2)


def find_ball(img):
    global resImg
    x, y = 0, 0
    lowerCir = np.array([30, 30, 30], np.uint8)
    upperCir = np.array([40, 40, 40], np.uint8)

    imgInRange = cv2.inRange(img, lowerCir, upperCir)
    ret, th = cv2.threshold(imgInRange, 127, 255, 0)
    imgCnts, cnts, _ = cv2.findContours(
        th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    res = []

    for c in cnts:
        area = cv2.contourArea(c)
        (x, y), r = cv2.minEnclosingCircle(c)
        areaCir = circle_area(r)
        if abs(area - areaCir) <= 40:
            cv2.circle(resImg, (int(x), int(y)), int(r), (255, 0, 0), -1)
            res.append([x, y, r])
    if len(res) > 0:
        resSorted = sorted(res, key=itemgetter(-1))
        resSorted = resSorted[-1]
        x = resSorted[0]
        y = resSorted[1]

    return x, y


def find_platform(img):
    global resImg
    x, y = 0, 0
    lowerRect = np.array([250,  130,  0], np.uint8)
    upperRect = np.array([255,  140,  5], np.uint8)

    imgInRange = cv2.inRange(img, lowerRect, upperRect)
    ret, th = cv2.threshold(imgInRange, 127, 255, 0)
    imgCnts, cnts, _ = cv2.findContours(
        th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    res = []

    for c in cnts:
        areaCnt = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)
        areaRect = w * h
        if areaCnt / areaRect >= 0.8 and w / (h * 1.0) >= 10:
            cv2.rectangle(resImg, (x, y), (x + w, y + h), (255, 255, 0), -1)
            res.append((areaCnt, x, y, w, h))

    if len(res) > 0:
        resSorted = sorted(res, key=itemgetter(0))
        resSorted = resSorted[0]
        x = resSorted[1]
        y = resSorted[2]
        w = resSorted[3]
        h = resSorted[4]
        cv2.circle(resImg, (int(x + w / 2), int(y + h / 2)),
                   int(h), (255, 0, 255), -1)

        return int(x + w / 2), int(y + h / 2), x + int(w / 2.5), x + w - int(w / 2.5)
    return 0, 0, 0, 0


def keyboard(xBall, xR, xL):
    if xBall > xR:
        print('press right')
        pyautogui.keyDown('right')

    elif xBall < xL:
        print('press left')
        pyautogui.keyDown('left')

    else:
        pyautogui.keyUp('left')
        pyautogui.keyUp('right')


def main():
    global resImg
    xCir, yCir = 0, 0
    xRect, yRect = 0, 0
    print('wait 5 second')
    for i in range(0, 5):
        print(i)
        time.sleep(1)

    while True:
        img = screenshot_capture()
        if img is None:
            continue
        resImg = img * 0
        xCir, yCir = find_ball(img)
        xRect, yRect, xL, xR = find_platform(img)
        print(xCir, xRect, xCir - xRect)
        keyboard(xCir, xR, xL)
        r, c, ch = resImg.shape
        resImg = cv2.resize(resImg, (int(c / 3), int(r / 3)))
        cv2.imshow('resImg', resImg)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
