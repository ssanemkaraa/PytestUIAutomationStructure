import os

import pytest
from selenium import webdriver
from utils.configs.config import Config


@pytest.fixture(autouse=True)
def run_around_tests():
    print("\nTest başladı\n")
    yield
    print("\nTest Tamamlandı\n")


@pytest.fixture()
def setup():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    driver_path = os.path.join(project_root, 'utils', 'drivers', 'chromedriver')

    browser_name = Config.get_driver_name()
    implicit_wait_time = Config.get_implicity_wait()
    options = get_browser_options()

    if browser_name.lower() == "chrome":
        driver = webdriver.Chrome(options=options, executable_path=driver_path)
    elif browser_name.lower() == "firefox":
        driver = webdriver.Firefox(options=options, executable_path=driver_path)
    elif browser_name.lower() == "edge":
        driver = webdriver.Edge(executable_path=driver_path)
    else:
        raise Exception("Invalid browser name provided!")

    driver.implicitly_wait(implicit_wait_time)
    return driver


def get_browser_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")
    prefs = {"profile.default_content_setting_values.notifications": 1}
    options.add_experimental_option("prefs", prefs)
    return options