import os

import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
reference_path = os.path.join(project_root, '../testData/connect_wallet.png')
screenshot_path = os.path.join(project_root, '../testData/current.png')
refconfidence = 0.8
while True:
    try:
        screens_size = pyautogui.screenshot().size
        all_screen_height = screens_size[0]
        all_screen_width = screens_size[1]
        screen_size = pyautogui.size()
        screen_height = screen_size[0]
        screen_width = screen_size[1]
        screen = np.array(ImageGrab.grab(bbox=None))

        screenshot = pyautogui.screenshot(screenshot_path)
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
        coordinates = []

        for minimage in pyautogui.locateAllOnScreen(reference_path, confidence=refconfidence):
            cv2.rectangle(
                screenshot,
                (minimage.left, minimage.top,
                 minimage.width,
                 minimage.height),
                (0, 0, 255),
                2
            )
            coordinate = (minimage.left,
                          minimage.top,
                          minimage.width,
                          minimage.height)

            coordinates.append(coordinate)

        x_ratio = coordinates[0][0] / all_screen_height
        y_ratio = coordinates[0][1] / all_screen_width
        x = int(screen_height * x_ratio)
        y = int(screen_width * y_ratio)

        pyautogui.moveTo(x=x + 20, y=y + 10, duration=0.5, logScreenshot=True)
        cv2.imwrite(screenshot_path, screen)

    except Exception as ex:
        print("Error: " + str(ex))
