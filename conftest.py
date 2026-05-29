import pytest
import os
from datetime import datetime
import allure

from core.config_loader import load_config
from core.logger import get_logger
from core.api_client import APIClient
from core.driver_factory import create_driver

logger = get_logger("tests")


# load config
@pytest.fixture(scope="session")
def config():
    return load_config()


# API client
@pytest.fixture(scope="session")
def api_client(config):
    return APIClient(
        base_url=config["api_url"],
        timeout=config.get("timeout", 10)
    )


# UI driver
@pytest.fixture(scope="function")
def driver():
    driver = create_driver()
    yield driver
    driver.quit()


# log test start/end
def pytest_runtest_logstart(nodeid, location):
    logger.info(f"[TEST START] {nodeid}")


def pytest_runtest_logfinish(nodeid, location):
    logger.info(f"[TEST END] {nodeid}")


# 🔥 ADD PHẦN NÀY (QUAN TRỌNG NHẤT)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # chỉ xử lý khi test FAIL
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)

        if driver:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)

            file_name = f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            file_path = os.path.join(screenshot_dir, file_name)

            # chụp ảnh
            driver.save_screenshot(file_path)

            logger.error(f"[SCREENSHOT] Saved: {file_path}")

            # attach vào Allure
            allure.attach.file(
                file_path,
                name=file_name,
                attachment_type=allure.attachment_type.PNG
            )