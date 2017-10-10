import cv2
import os
import numpy as np

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def nothing(x):
    pass


def brightness():
    img = cv2.imread(DIR_PATH + '\\images\\04.jpg', 1)
    r, c, ch = img.shape
   
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    cv2.namedWindow('image')
    cv2.createTrackbar('sides', 'image', 0, 16, nothing)
    cv2.createTrackbar('% arclen', 'image', 0, 100, nothing)
    
    while True:
        res = img.copy()
        side = cv2.getTrackbarPos('sides', 'image')
        percent_of_arclen = cv2.getTrackbarPos('% arclen', 'image')
        gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
        ret, th = cv2.threshold(gray.copy(), 250, 255, 0)
        _, cnts, h = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)        
        
        for cnt in cnts:
            cnt_area = cv2.contourArea(cnt)
            if cnt_area < 2000 or cnt_area > 34000:
                continue
            cv2.drawContours(res, cnt, -1, (255, 255, 0), 3)
            # perimeter
            peri = cv2.arcLength(cnt, True)
            print((percent_of_arclen/1000.0))
            # epsilon is maximum distance from contour to approximated contour
            epsilon = (percent_of_arclen/1000.0) * peri
            #   approximates a contour by Douglas-Peucker algorithm.
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            sides = len(approx)
            rect = (x, y), (w, h), r = cv2.minAreaRect(cnt)
            if sides == side:
                cv2.drawContours(res, cnt, -1, (0, 0, 255), 3)
                cv2.drawContours(res, approx, -1, (255, 255, 0), 4)
            font = cv2.FONT_HERSHEY_SIMPLEX

            cv2.putText(res, "sides: {0}".format(sides), (int(x-40),int(y)),font, 0.5, (0, 25, 0), 1, cv2.LINE_AA)
        # cv2.imshow('gray', gray)
        # cv2.imshow('th', th)
        cv2.imshow('image', res)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break


if __name__ == '__main__':
    brightness()
