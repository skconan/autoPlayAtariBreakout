import cv2
import os
import numpy as np

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
img = None
pos_x, pos_y = 0, 0


def get_position(event, x, y, flags, param):
    global img, pos_x, pos_y
    if event == cv2.EVENT_MOUSEMOVE and img is not None:
        pos_x, pos_y = x, y
        print('row: ', y, ', col: ', x, ', color value: ', img[y, x])


def get_color():
    global img, pos_x, pos_y
    img = cv2.imread(DIR_PATH + '\\images\\00.jpg', 1)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', get_position)

    r, c, ch = img.shape
    r = int(r / 2)
    c = int(c / 2)
    img = cv2.resize(img, (c, r))
    color = np.array(np.zeros((200, 200, 3), dtype=np.uint8))

    while True:
        c1, c2, c3 = cv2.split(color)
        c1 *= 0
        c2 *= 0
        c3 *= 0
        c1 += img[pos_y, pos_x][0]
        c2 += img[pos_y, pos_x][1]
        c3 += img[pos_y, pos_x][2]
        color = cv2.merge((c1, c2, c3))

        cv2.imshow('image', img)
        cv2.imshow('color', color)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break


if __name__ == '__main__':
    get_color()
