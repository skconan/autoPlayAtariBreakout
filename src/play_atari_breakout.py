import cv2
import numpy as np
from PIL import ImageGrab
import math
from pynput.keyboard import Key
from pynput.keyboard import Controller as keyboardCtrl

imgColor = None
widthScreen = 1920
heightScreen = 1080


def getPosition(event, x, y, flags, param):
    global imgColor
    if event == cv2.EVENT_LBUTTONDBLCLK and imgColor is not None:
        print(imgColor[x, y])


def getColor():
    global imgColor
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', getPosition)
    while True:
        imgColor = screenshotCapture()
        if imgColor is None:
            continue
        cv2.imshow('image', imgColor)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break


def screenshotCapture():
    img = ImageGrab.grab(
        bbox=(int(widthScreen / 2), 240, widthScreen, heightScreen))
    return np.array(img)


def findBall():
    x, y = 0, 0
    lowerCir = np.array([30, 30, 30], np.uint8)
    upperCir = np.array([40, 40, 40], np.uint8)
    return x, y


def findPlatform():
    x, y = 0, 0
    lowerRect = np.array([30, 30, 30], np.uint8)
    upperRect = np.array([40, 40, 40], np.uint8)
    return x, y


def main():
    xCir, yCir = 0, 0
    xRect, yRect = 0, 0
    while True:
        img = screenshotCapture()
        if img is None:
            continue
        xCir, yCir = findBall(img)
        xRect, yRect = findPlatform(img)


if __name__ == '__main__':
    main()
    getColor()
