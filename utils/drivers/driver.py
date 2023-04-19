from selenium import webdriver
from utils.configs.config import Config


class Driver:
    def __init__(self):
        self.browser_name = Config.get_driver_name()
        self.implicit_wait_time = Config.get_implicity_wait()
        self.driver_path = Config.get_driver_path()

    def get_driver(self):
        options = self._get_browser_options()

        if self.browser_name.lower() == "chrome":
            driver = webdriver.Chrome(options=options, executable_path=self.driver_path)
        elif self.browser_name.lower() == "firefox":
            driver = webdriver.Firefox(options=options, executable_path=self.driver_path)
        elif self.browser_name.lower() == "edge":
            driver = webdriver.Edge(executable_path=self.driver_path)
        else:
            raise Exception("Invalid browser name provided!")

        driver.implicitly_wait(self.implicit_wait_time)
        return driver

    def _get_browser_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        options.add_argument("--disable-blink-features=AutomationControlled")
        prefs = {"profile.default_content_setting_values.notifications": 1}
        options.add_experimental_option("prefs", prefs)
        return options
