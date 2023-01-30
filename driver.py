from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def create_driver(timeout):
    caps = DesiredCapabilities.CHROME
    caps["goog:loggingPrefs"] = {"performance": "ALL"}  # Caps for network log's
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument('--headless')  # Create options
    driver = webdriver.Chrome(options=driver_options, desired_capabilities=caps)
    driver.set_page_load_timeout(timeout)  # Set timeout

    return driver
