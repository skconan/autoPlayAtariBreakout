import cv2
import os
import numpy as np

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def nothing(x):
    pass


def brightness():
    img = cv2.imread(DIR_PATH + '\\images\\01.jpg', 1)
    r, c, ch = img.shape
   
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    cv2.namedWindow('image')
    cv2.createTrackbar('value', 'image', 0, 255, nothing)

    while True:
        brightness_value = cv2.getTrackbarPos('value', 'image')
        brightness_add = np.array(np.zeros((r, c), dtype=np.uint8))
        brightness_add.fill(brightness_value)

        h, s, v = cv2.split(hsv)
        v = cv2.add(v, brightness_add)
        result_hsv = cv2.merge((h, s, v))
        result_bgr = cv2.cvtColor(result_hsv, cv2.COLOR_HSV2RGB)

        cv2.imshow('image', result_bgr)
        cv2.imshow('hsv', result_hsv)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break


if __name__ == '__main__':
    brightness()
