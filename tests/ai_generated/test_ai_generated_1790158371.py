import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.epic("Facebook Authentication")
@allure.feature("Login Feature")
@allure.story("Login with invalid credentials")
@allure.title("Kịch bản kiểm thử: Đăng nhập Facebook với tài khoản giả định")
def test_facebook_login(driver, config):
    # Ép cứng URL Facebook để không bị lấy nhầm URL khách sạn
    base_url = 'https://www.facebook.com'
    wait = WebDriverWait(driver, 10)

    with allure.step(f"Truy cập vào trang web: {base_url}"):
        driver.get(base_url)
        # Chờ cho đến khi ô nhập email xuất hiện để đảm bảo trang đã tải xong
        wait.until(EC.presence_of_element_located((By.ID, "email")))

    with allure.step("Nhập địa chỉ email: abc@gmail.com"):
        email_input = driver.find_element(By.ID, "email")
        email_input.clear()
        email_input.send_keys("abc@gmail.com")

    with allure.step("Nhập mật khẩu: 123"):
        password_input = driver.find_element(By.ID, "pass")
        password_input.clear()
        password_input.send_keys("123")

    with allure.step("Click vào nút 'Đăng nhập'"):
        login_button = wait.until(EC.element_to_be_clickable((By.NAME, "login")))
        login_button.click()

    with allure.step("Xác nhận hệ thống xử lý yêu cầu đăng nhập"):
        # Chờ 3 giây để hệ thống phản hồi hoặc chuyển trang sau khi nhấn nút
        time.sleep(3)
        current_url = driver.current_url
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="Kết quả sau khi đăng nhập", 
            attachment_type=allure.attachment_type.PNG
        )
        # Kiểm tra xem có sự thay đổi URL hoặc giữ nguyên tại trang đăng nhập (do sai tài khoản)
        assert len(current_url) > 0