from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.logger import get_logger
import os
import time

logger = get_logger("base_page")


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # mở url
    def open(self, url):
        logger.info(f"Open URL: {url}")
        self.driver.get(url)

    # find element
    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    # click
    def click(self, locator):
        logger.info(f"Click: {locator}")
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    # input text
    def input_text(self, locator, text):
        logger.info(f"Input: {locator} = {text}")
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    # get text
    def get_text(self, locator):
        element = self.find(locator)
        return element.text

    # wait element visible
    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    # screenshot khi lỗi
    def take_screenshot(self, name="error"):
        folder = "screenshots"
        os.makedirs(folder, exist_ok=True)

        timestamp = int(time.time())
        path = f"{folder}/{name}_{timestamp}.png"

        self.driver.save_screenshot(path)
        logger.error(f"Screenshot saved: {path}")

        return path