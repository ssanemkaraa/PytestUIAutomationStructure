import os
import time

import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
reference_image_path = os.path.join(project_root, 'minref.png')
current_image_path = os.path.join(project_root, 'current.png')

loop_time = 1

while (True):
    # screenshot = pyautogui.screenshot()
    grab = ImageGrab.grab()
    array = np.array(grab)
    # screenshot = array[:, :, ::-1].copy()
    screenshot = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)

    cv2.imshow('Test', screenshot)
    # print('FPS {}'.format(1 / (time.time() - loop_time)))
    # loop_time = time

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break

    print('Done')
