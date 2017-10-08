import cv2
import numpy as np
from PIL import ImageGrab
import math
from pynput.keyboard import Key
from pynput.keyboard import Controller as keyboardCtrl
from operator import itemgetter
imgColor = None
widthScreen = 1920
heightScreen = 1080
resImg = None

def getPosition(event, x, y, flags, param):
    global imgColor
    if event == cv2.EVENT_MOUSEMOVE and imgColor is not None:
        print(x,y,imgColor[y, x])


def getColor():
    global imgColor
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', getPosition)
    while True:
        imgColor = screenshotCapture()
        # imgColor = cv2.imread('C:/Users/skconan/Desktop/imgCtrlKeyboard/src/images/Screenshot (40).png',1)
        if imgColor is None:
            continue
        cv2.imshow('image', imgColor)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break


def screenshotCapture():
    img = ImageGrab.grab(
        bbox=(int(widthScreen / 2), 240, widthScreen, heightScreen))
    img = np.array(img)

    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def circle_area(radius):
    return math.pi * (radius**2)


def findBall(img):
    global resImg
    x, y = 0, 0
    lowerCir = np.array([30, 30, 30], np.uint8)
    upperCir = np.array([40, 40, 40], np.uint8)

    imgInRange = cv2.inRange(img, lowerCir, upperCir)
    ret, th = cv2.threshold(imgInRange, 127, 255, 0)
    imgCnts, cnts, _ = cv2.findContours(
        th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    res = []
    resImg = img * 0
    cv2.drawContours(resImg, cnts, -1, (0, 255, 0), 3)

    for c in cnts:
        area = cv2.contourArea(c)
        (x, y), r = cv2.minEnclosingCircle(c)
        areaCir = circle_area(r)
        if abs(area - areaCir) <= 40:
            print(abs(area - areaCir))
            cv2.circle(resImg, (int(x), int(y)), int(r), (255, 0, 0), -1)
            res.append([x, y, r])
    if len(res) > 0:
        resSorted = sorted(res, key=itemgetter(-1))
        resSorted = resSorted[-1]
        x = resSorted[0]
        y = resSorted[1]
    # cv2.imshow('resImgCir', resImg)
    # key = cv2.waitKey(1) & 0xff
    # if key == ord('q'):
    #     exit()
    return x, y


def findPlatform(img):
    global resImg
    x, y = 0, 0
    lowerRect = np.array([250,  130,  0], np.uint8)
    upperRect = np.array([255,  140,  5], np.uint8)

    imgInRange = cv2.inRange(img, lowerRect, upperRect)
    ret, th = cv2.threshold(imgInRange, 127, 255, 0)
    imgCnts, cnts, _ = cv2.findContours(
        th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    res = []
    resImg = img * 0
    cv2.drawContours(resImg, cnts, -1, (0, 255, 0), 3)

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
    # cv2.imshow('resImgRect', imgInRange)
    # # cv2.imshow('resImgRect', resImg)
    # key = cv2.waitKey(1) & 0xff
    # if key == ord('q'):
    #     exit()
    return x, y


def main():
    global resImg
    xCir, yCir = 0, 0
    xRect, yRect = 0, 0
    while True:
        img = screenshotCapture()
        if img is None:
            continue
        xCir, yCir = findBall(img)
        xRect, yRect = findPlatform(img)

        cv2.imshow('resImg', resImg)
        # cv2.imshow('resImgRect', resImg)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
    # getColor()
