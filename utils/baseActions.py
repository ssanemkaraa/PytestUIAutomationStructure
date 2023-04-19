import os
import re
import time

import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab, Image, ImageOps
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BaseActions:

    def __init__(self, driver):
        self.driver = driver

        # self.driver = WebDriver

    def switch_to_new_window(self):
        try:
            time.sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.switch_to.window(self.driver.current_window_handle)
            time.sleep(0.5)
            return True

        except Exception as ex:
            print("Exception has been thrown." + str(ex))
            self.driver.close()
            return False

    def switch_to_previous_window(self):
        try:
            time.sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.switch_to.window(self.driver.current_window_handle)
            return True

        except Exception as ex:
            print("Exception has been thrown." + str(ex))
            self.driver.close()
            return False

    def refresh_to_window(self):

        try:
            self.driver.refresh()
            self.driver.switch_to.window(self.driver.current_window_handle)
            time.sleep(2)
            return True

        except Exception as ex:
            print("Exception has been thrown." + str(ex))
            self.driver.close()
            return False

    def scroll_to_window(self, scrollsize):

        try:
            time.sleep(1)
            pyautogui.scroll(scrollsize)
            return True

        except Exception as ex:
            print("Exception has been thrown." + str(ex))
            self.driver.close()
            return False

    def maximize_to_active_window(self):

        try:
            self.driver.maximize_window()
            self.driver.switch_to.window(self.driver.current_window_handle)
            return True

        except Exception as ex:
            print("Exception has been thrown." + str(ex))
            self.driver.close()
            return False

    def switch_to_modal(self, locator, byType):
        elm = self.get_element_selected_type(locator, byType)
        try:
            WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it(elm))
            return True
        except Exception as ex:
            print("Exception has been thrown." + str(ex))
            self.driver.close()
            return False

    def get_element_selected_type(self, locator, byType):
        global elm
        wait = WebDriverWait(self.driver, 10)
        match byType:
            case "xpath":
                elm = wait.until(EC.presence_of_element_located((By.XPATH, locator)))
            case "id":
                elm = wait.until(EC.presence_of_element_located((By.ID, locator)))
            case "name":
                elm = wait.until(EC.presence_of_element_located((By.NAME, locator)))
            case "class":
                elm = wait.until(EC.presence_of_element_located((By.CLASS_NAME, locator)))
            case "tag":
                elm = wait.until(EC.presence_of_element_located((By.TAG_NAME, locator)))
        return elm

    def click_locator(self, locator, byType):
        elm = self.get_element_selected_type(locator, byType)
        try:
            if elm.is_displayed:
                elm.click()
                return True
            else:
                self.driver.close()
                return False
        except Exception as ex:
            print("Exception has been thrown." + str(ex))
            self.driver.close()
            return False

    def clean_input_locator(self, locator, byType):
        try:
            self.click_locator(locator, byType)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press("backspace")
            return True

        except Exception as ex:
            print("Exception has been thrown." + str(ex))
            self.driver.close()
            return False

    def get_text_in_locator(self, locator, byType):
        elm = self.get_element_selected_type(locator, byType)
        try:
            htmlandtext = elm.get_attribute('innerHTML')
            text = re.sub(r'<.*?>', '', str(htmlandtext))
            return text
        except Exception as ex:
            print("Exception has been thrown." + str(ex))
            self.driver.close()
            return False

    def is_text_in_locator(self, locator, byType, reftext):
        elm = self.get_element_selected_type(locator, byType)
        try:
            htmlandtext = elm.get_attribute('innerHTML')
            text = re.sub(r'<.*?>', '', str(htmlandtext))
            i = text.find(str(reftext))
            if i > 0:
                return True
        except Exception as ex:
            print("Exception has been thrown." + str(ex))
            self.driver.close()
            return False

    def wait_dissapear_locator(self, locator, byType):
        elm = self.get_element_selected_type(locator, byType)
        try:
            WebDriverWait(self.driver, 5).until_not(elm)
        except Exception as ex:
            print("Exception has been thrown." + str(ex))
            self.driver.close()
            return False

    def see_locator(self, locator, byType):
        elm = self.get_element_selected_type(locator, byType)
        try:
            if elm.is_displayed:
                return True
        except Exception as ex:
            print("Exception has been thrown." + str(ex))
            self.driver.close()
            return False

    def send_input_data_locator(self, locator, byType, data):
        elm = self.get_element_selected_type(locator, byType)
        try:
            if elm.is_displayed:
                elm.click()
                time.sleep(1)
                elm.send_keys(data)
                return True
            else:
                self.driver.close()
                return False
        except Exception as ex:
            print("Exception has been thrown." + str(ex))
            self.driver.close()
            return False


    @staticmethod
    def find_reference_image_with_opencv(screenshot_path, reference_path, refconfidence):
        # search reference image on the main screen and finds the correct point by proportioning all screen coordinates.
        try:
            screens_size = pyautogui.screenshot().size
            all_screen_height = screens_size[0]
            all_screen_width = screens_size[1]
            screen_size = pyautogui.size()
            screen_height = screen_size[0]
            screen_width = screen_size[1]

            time.sleep(1)
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

            if pyautogui.moveTo(x=x + 20, y=y + 10, duration=0.5, logScreenshot=True):
                return True

        except Exception as ex:
            print("Exception has been thrown." + str(ex))
            return False

    @staticmethod
    def find_reference_image_with_pyautogui(screenshot_path, reference_path, refconfidence):
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
                if pyautogui.moveTo(x=x + 90, y=y + 10, duration=0.5, logScreenshot=True):
                    return True

        except Exception as ex:
            print("Exception has been thrown." + str(ex))
