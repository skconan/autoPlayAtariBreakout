import cv2
import numpy as np
from PIL import ImageGrab
import math
from pynput.keyboard import Key
from pynput.keyboard import Controller as keyboardCtrl

def main():
    global img
    xCir, yCir = 0, 0
    xRect, yRect = 0, 0
    lowerCir = np.array([30, 30, 30], np.uint8)
    upperCir = np.array([40, 40, 40], np.uint8)
    lowerRect = np.array([30, 30, 30], np.uint8)
    upperRect = np.array([40, 40, 40], np.uint8)    