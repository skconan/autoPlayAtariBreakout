import cv2
import os
import numpy as np


DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def nothing(x):
    pass


def color_feature():
    img = cv2.imread(DIR_PATH + '\\images\\06.jpg', 1)
    r,g,b = cv2.split(img)
    print('r: ',r.mean())
    print('g: ',g.mean())
    print('b: ',b.mean())
    cv2.imshow('image',img)
    key = cv2.waitKey(0) & 0xff
    

if __name__ == '__main__':
    color_feature()
