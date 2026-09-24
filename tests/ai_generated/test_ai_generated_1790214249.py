import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.title("Kiểm thử tính năng đăng nhập thành công với tài khoản chuẩn")
def test_successful_login(driver):
    with allure.step("Mở trang web SauceDemo"):
        driver.get("https://www.saucedemo.com/")
        driver.maximize_window()

    with allure.step("Nhập tên đăng nhập (standard_user)"):
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        username_input.send_keys("standard_user")

    with allure.step("Nhập mật khẩu (secret_sauce)"):
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("secret_sauce")

    with allure.step("Nhấp vào nút Đăng nhập"):
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()

    with allure.step("Kiểm tra đăng nhập thành công và chụp ảnh màn hình"):
        # Xác thực đăng nhập thành công bằng cách kiểm tra URL hoặc sự xuất hiện của trang sản phẩm
        WebDriverWait(driver, 10).until(
            EC.url_contains("inventory.html")
        )
        
        # Đính kèm ảnh chụp màn hình vào Allure Report
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Login_Success_Screenshot",
            attachment_type=allure.attachment_type.PNG
        )
        
        # Kiểm tra tiêu đề trang hoặc một phần tử đặc trưng trên trang inventory
        inventory_container = driver.find_element(By.ID, "inventory_container")
        assert inventory_container.is_displayed(), "Đăng nhập thất bại, không tìm thấy trang sản phẩm."