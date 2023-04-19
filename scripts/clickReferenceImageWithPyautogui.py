import os

import pyautogui

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
screenshot_path = os.path.join(project_root, 'testData', 'current.png')
reference_path = os.path.join(project_root, 'testData', 'connect_wallet2.png')
refconfidence = 0.8

# When there is more than one screen, this function searches the reference
# image on the main screen and finds the correct point by proportioning all screen coordinates.

screens_size = pyautogui.screenshot().size
all_screen_height = screens_size[0]
all_screen_width = screens_size[1]
screen_size = pyautogui.size()
screen_height = screen_size[0]
screen_width = screen_size[1]

try:
    coordinates = []
    for c in pyautogui.locateAllOnScreen(reference_path, confidence=refconfidence, grayscale=True):
        pyautogui.screenshot(screenshot_path)
        coordinates.append(c)
    if len(coordinates) == 0:
        print("Image not found.")
    else:
        print("Image found.")
        x_ratio = coordinates[0][0] / all_screen_height
        y_ratio = coordinates[0][1] / all_screen_width
        x = int(screen_height * x_ratio)
        y = int(screen_width * y_ratio)
        print("Image coordinates: x={}, y={}".format(x, y))
        pyautogui.moveTo(x=x + 90, y=y + 10, duration=0.5, logScreenshot=True)

except Exception as ex:
    print("Exception has been thrown." + str(ex))
