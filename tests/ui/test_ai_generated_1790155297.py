import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("Authentication")
@allure.story("Facebook Login")
@allure.title("Test Facebook Login with credentials from configuration")
def test_facebook_login(driver, config):
    base_url = 'https://www.facebook.com'
    email_address = 'abc@gmail.com'
    password_text = '123'

    with allure.step("Truy cập trang chủ Facebook"):
        driver.get(base_url)
        # Đợi cho đến khi trường nhập email xuất hiện trên màn hình
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "email")))

    with allure.step("Nhập email/số điện thoại"):
        email_input = driver.find_element(By.ID, "email")
        email_input.clear()
        email_input.send_keys(email_address)

    with allure.step("Nhập mật khẩu"):
        password_input = driver.find_element(By.ID, "pass")
        password_input.clear()
        password_input.send_keys(password_text)

    with allure.step("Click nút Đăng nhập"):
        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

    with allure.step("Xác minh kết quả đăng nhập"):
        # Đợi một khoảng thời gian ngắn để trang xử lý chuyển hướng hoặc tải lại dữ liệu
        time.sleep(5)
        current_url = driver.current_url
        # Kiểm tra xem URL có thay đổi hoặc tiêu đề trang hợp lệ hay không
        assert "login" not in current_url, "Đăng nhập thất bại hoặc bị giữ lại ở trang login."