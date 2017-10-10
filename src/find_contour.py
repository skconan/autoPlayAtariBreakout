import cv2
import os
import numpy as np

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def nothing(x):
    pass


def find_contour():
    img = cv2.imread(DIR_PATH + '\\images\\02.jpg', 1)
    res = img.copy()
    gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(gray.copy(), 140, 255, 0)
    _, cnts, h = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)           
    cv2.drawContours(res,cnts,-1,(0,0,255),2)
    cv2.imshow('image', res)
    key = cv2.waitKey(0) & 0xff
    

if __name__ == '__main__':
    find_contour()
