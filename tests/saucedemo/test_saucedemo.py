import pytest
import allure
import time
from selenium.webdriver.common.by import By

@allure.epic("Cross-Project Testing")
@allure.feature("SauceDemo E-commerce")
class TestSauceDemo:
    @allure.title("TC_01: Đăng nhập thành công vào hệ thống giả lập SauceDemo")
    def test_login_saucedemo(self, driver):
        target_url = "https://www.saucedemo.com/"
        
        with allure.step(f"1. Truy cập vào trang web giả lập: {target_url}"):
            driver.get(target_url)
            time.sleep(1) # Chờ load trang
            
        with allure.step("2. Nhập Username và Password hợp lệ"):
            # Web này cung cấp sẵn tk là: standard_user / pass: secret_sauce
            driver.find_element(By.ID, "user-name").send_keys("standard_user")
            driver.find_element(By.ID, "password").send_keys("secret_sauce")
            
        with allure.step("3. Click nút Đăng nhập"):
            driver.find_element(By.ID, "login-button").click()
            time.sleep(2) # Chờ chuyển trang
            
        with allure.step("4. Xác minh đăng nhập thành công và vào trang sản phẩm"):
            # Kiểm tra xem đường dẫn URL đã chuyển sang trang inventory (kho hàng) chưa
            assert "inventory.html" in driver.current_url
            
            # Kiểm tra xem có icon giỏ hàng trên góc phải màn hình không
            cart_icon = driver.find_elements(By.CLASS_NAME, "shopping_cart_link")
            assert len(cart_icon) > 0, "Đăng nhập thất bại, không tìm thấy icon giỏ hàng!"
            
        with allure.step("5. Chụp ảnh màn hình minh chứng"):
            allure.attach(driver.get_screenshot_as_png(), name="SauceDemo_Logged_In", attachment_type=allure.attachment_type.PNG)