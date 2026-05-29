import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from core.config_loader import get_config
from core.logger import get_logger

logger = get_logger("driver_factory")

def create_driver():
    config = get_config()

    browser = config.get("browser", "chrome").lower()
    headless = config.get("headless", False)

    logger.info(f"Start browser: {browser} | headless={headless}")

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")

        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        
        # Bắt buộc phải có 2 dòng này khi chạy Jenkins trên Docker/Linux
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Chỉ định đường dẫn trình duyệt nếu đang chạy trên Linux (Docker)
        if os.path.exists("/usr/bin/chromium"):
            options.binary_location = "/usr/bin/chromium"

        # Khởi tạo siêu gọn gàng, Selenium 4 sẽ tự lo phần Driver
        driver = webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
            
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Firefox(options=options)

    else:
        raise Exception(f"Browser not supported: {browser}")

    driver.maximize_window()
    return driver