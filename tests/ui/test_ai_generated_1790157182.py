import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.epic("Facebook Web Application")
@allure.feature("Authentication")
class TestFacebookLogin:

    @allure.title("Test Facebook Login UI and Invalid Credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_facebook_invalid_login(self, driver, config):
        base_url = config.get('base_url', 'https://www.facebook.com')
        
        with allure.step("Navigate to Facebook home page"):
            driver.get(base_url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            allure.attach(
                driver.get_screenshot_as_png(), 
                name="Facebook Home Page", 
                attachment_type=allure.attachment_type.PNG
            )

        with allure.step("Input invalid email address"):
            email_field = driver.find_element(By.ID, "email")
            email_field.clear()
            email_field.send_keys("example_qa_test_user@gmail.com")

        with allure.step("Input invalid password"):
            password_field = driver.find_element(By.ID, "pass")
            password_field.clear()
            password_field.send_keys("DemoPassword123!")

        with allure.step("Click on the Login button"):
            login_button = driver.find_element(By.NAME, "login")
            login_button.click()

        with allure.step("Verify that login fails and user is not authenticated"):
            WebDriverWait(driver, 10).until(
                lambda d: d.current_url != base_url or len(d.find_elements(By.ID, "error_box")) > 0
            )
            current_url = driver.current_url
            allure.attach(
                driver.get_screenshot_as_png(), 
                name="Login Result Page", 
                attachment_type=allure.attachment_type.PNG
            )
            assert "login" in current_url or len(driver.find_elements(By.ID, "error_box")) > 0, "Login should have failed, but redirect or error handling was not detected."