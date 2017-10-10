import cv2
import numpy as np

def nothing(x):
    pass

def color_range():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('image')
    cv2.createTrackbar('Hmin', 'image', 0, 179, nothing)
    cv2.createTrackbar('Smin', 'image', 0, 255, nothing)
    cv2.createTrackbar('Vmin', 'image', 0, 255, nothing)
    cv2.createTrackbar('Hmax', 'image', 0, 179, nothing)
    cv2.createTrackbar('Smax', 'image', 0, 255, nothing)
    cv2.createTrackbar('Vmax', 'image', 0, 255, nothing)
    while True:
        ret, img = cap.read()
        if img is None:
            continue
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        h_min = cv2.getTrackbarPos('Hmin', 'image')
        s_min = cv2.getTrackbarPos('Smin', 'image')
        v_min = cv2.getTrackbarPos('Vmin', 'image')
        h_max = cv2.getTrackbarPos('Hmax', 'image')
        s_max = cv2.getTrackbarPos('Smax', 'image')
        v_max = cv2.getTrackbarPos('Vmax', 'image')
        lowerb = np.array([h_min,s_min,v_min],np.uint8)
        upperb = np.array([h_max,s_max,v_max],np.uint8)
        hsv_inrange = cv2.inRange(hsv,lowerb,upperb)
        res_bgr = cv2.bitwise_and(img,img,mask=hsv_inrange)
        cv2.imshow('image',res_bgr)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()

if __name__ == '__main__':
    color_range()