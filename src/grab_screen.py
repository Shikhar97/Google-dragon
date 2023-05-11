import cv2
import numpy as np
import pyautogui


def grab_screen(region):
    im = pyautogui.screenshot(region=region)
    image = np.asarray(im)
    return image