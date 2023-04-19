import time

from pages.HomePage import HomePage
from utils.customLogger import LogGen


class TestCase001:
    logger = LogGen.loggen()
    logger.info("Test Case 001: Home Page")

    def test_open_page(self, setup):
        page = HomePage(setup)

        try:
            page.open_home_page()

            is_page_valid_opencv = page.validate_open_page_with_opencv()
            is_page_valid_pyautogui = page.validate_open_page_with_pyautogui()

            if is_page_valid_opencv and is_page_valid_pyautogui:
                time.sleep(5)
                self.logger.info("Page opened successfully!")
                return True
            else:
                self.logger.error("Failed to open page!")
                return False
        except Exception as ex:
            self.logger.error("Exception has been thrown: {}".format(str(ex)))
            return False
