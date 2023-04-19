import os

from utils.baseActions import BaseActions
from utils.configs.config import Config


class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def open_home_page(self):
        url = Config.get_base_url()
        self.driver.get(url)

    def validate_open_page_with_opencv(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        screenshot_path = os.path.join(project_root, 'testData', 'current.png')
        reference_path = os.path.join(project_root, 'testData', 'connect_wallet.png')

        try:
            print("In")
            BaseActions.find_reference_image_with_opencv(screenshot_path=screenshot_path,
                                                             reference_path=reference_path, refconfidence=0.8)
            print("Out")
            return True
        except Exception as ex:
            print("Exception has been thrown: {}".format(str(ex)))
            return False
    def validate_open_page_with_pyautogui(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        screenshot_path = os.path.join(project_root, 'testData', 'current.png')
        reference_path = os.path.join(project_root, 'testData', 'connect_wallet.png')

        try:
            print("In")
            BaseActions.find_reference_image_with_pyautogui(screenshot_path=screenshot_path,
                                                             reference_path=reference_path, refconfidence=0.8)
            print("Out")
            return True
        except Exception as ex:
            print("Exception has been thrown: {}".format(str(ex)))
            return False