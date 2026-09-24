import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.title("Kiểm thử tính năng đăng nhập thành công với tài khoản chuẩn")
@allure.description("Kịch bản kiểm thử đăng nhập vào trang SauceDemo bằng tài khoản standard_user và mật khẩu hợp lệ.")
@allure.severity(allure.severity_level.CRITICAL)
def test_successful_login(driver, config):
    base_url = config.get("base_url", "https://www.saucedemo.com/")
    
    with allure.step(f"Truy cập vào trang web: {base_url}"):
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)

    with allure.step("Điền thông tin tài khoản đăng nhập"):
        username_input = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        password_input = driver.find_element(By.ID, "password")
        
        with allure.step("Nhập username: standard_user"):
            username_input.clear()
            username_input.send_keys("standard_user")
            
        with allure.step("Nhập password: secret_sauce"):
            password_input.clear()
            password_input.send_keys("secret_sauce")

    with allure.step("Bấm nút Đăng nhập"):
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()

    with allure.step("Xác thực đăng nhập thành công"):
        inventory_container = wait.until(EC.presence_of_element_located((By.ID, "inventory_container")))
        assert inventory_container.is_displayed(), "Đăng nhập không thành công, không tìm thấy trang sản phẩm."
        assert "inventory.html" in driver.current_url, "URL hiện tại không chính xác sau khi đăng nhập."