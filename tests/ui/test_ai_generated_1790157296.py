import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.title("Kiểm thử chức năng đăng nhập Facebook")
def test_facebook_login(driver, config):
    base_url = config.get('base_url', 'https://www.facebook.com')
    
    with allure.step("Truy cập trang chủ Facebook"):
        driver.get(base_url)
        
    with allure.step("Nhập email là abc@gmail.com"):
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.clear()
        email_input.send_keys("abc@gmail.com")
        
    with allure.step("Nhập mật khẩu là 123"):
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pass"))
        )
        password_input.clear()
        password_input.send_keys("123")
        
    with allure.step("Bấm nút Đăng nhập"):
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "login"))
        )
        login_button.click()
        
    with allure.step("Chờ hệ thống xử lý đăng nhập"):
        time.sleep(3)