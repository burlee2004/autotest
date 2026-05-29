import pytest
import allure
import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from allure_commons.types import AttachmentType

# =====================================================================
# PHẦN 1: UI AUTOMATION TESTING (TEST GIAO DIỆN DUCKDUCKGO)
# =====================================================================
@allure.epic("Cross-Project Testing")
@allure.feature("DuckDuckGo Search Engine")
class TestSearchEngineUI:

    @allure.title("UI_01: Kiểm tra giao diện Trang chủ hiển thị đúng")
    def test_homepage_ui(self, driver):
        target_url = "https://duckduckgo.com"
        
        with allure.step(f"1. Truy cập vào {target_url}"):
            driver.get(target_url)
            time.sleep(2)
            
        with allure.step("2. Xác minh Tiêu đề và Ô tìm kiếm xuất hiện"):
            # Kiểm tra tiêu đề web
            assert "DuckDuckGo" in driver.title
            # Kiểm tra ô nhập chữ có tồn tại không
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            assert search_box.is_displayed(), "Lỗi: Không hiển thị ô tìm kiếm!"
            
        with allure.step("Chụp ảnh màn hình trang chủ"):
            allure.attach(driver.get_screenshot_as_png(), name="Anh_Trang_Chu_DDG", attachment_type=AttachmentType.PNG)

    @allure.title("UI_02: Tìm kiếm từ khóa thành công có kết quả")
    def test_search_basic(self, driver):
        target_url = "https://duckduckgo.com"
        
        with allure.step(f"1. Truy cập vào {target_url}"):
            driver.get(target_url)
            time.sleep(2) 
            
        with allure.step("2. Nhập từ khóa 'Automation Test' và tìm kiếm"):
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.send_keys("Automation Test")
            search_box.send_keys(Keys.RETURN)
            time.sleep(3) 
            
        with allure.step("3. Xác minh kết quả tìm kiếm hiển thị"):
            # Khi tìm kiếm xong, tiêu đề tab sẽ có chữ Automation Test
            assert "Automation Test" in driver.title
            
        with allure.step("Chụp ảnh màn hình kết quả tìm kiếm"):
            allure.attach(driver.get_screenshot_as_png(), name="Anh_Ket_Qua_Tim_Kiem", attachment_type=AttachmentType.PNG)


# =====================================================================
# PHẦN 2: API & BACKEND TESTING
# =====================================================================
@allure.epic("Cross-Project Testing")
@allure.feature("Search Engine API & Performance")
class TestSearchEngineAPI:

    @allure.title("API_01: Ping Trang chủ (Đảm bảo Web không bị sập)")
    def test_homepage_status(self):
        target_url = "https://duckduckgo.com"
        
        with allure.step(f"1. Gửi request GET tới {target_url}"):
            response = requests.get(target_url)
            
        with allure.step("2. Xác minh HTTP Status Code là 200 (Thành công)"):
            assert response.status_code == 200
            
        with allure.step("3. Xác minh thời gian phản hồi dưới 2 giây (Performance)"):
            response_time = response.elapsed.total_seconds()
            assert response_time < 2.0

    @allure.title("API_02: Test API Gợi ý từ khóa (Autocomplete API)")
    def test_autocomplete_api(self):
        # API gợi ý của DuckDuckGo
        api_url = "https://duckduckgo.com/ac/"
        params = {"q": "kiem thu phan mem"}
        
        with allure.step(f"1. Gửi request GET tới API Autocomplete với từ khóa: '{params['q']}'"):
            response = requests.get(api_url, params=params)
            
        with allure.step("2. Xác minh API phản hồi thành công và trả về dữ liệu JSON"):
            assert response.status_code == 200
            data = response.json()
            assert len(data) > 0, "Không có dữ liệu trả về"
            
        with allure.step("3. Xác minh có chứa các từ khóa gợi ý liên quan"):
            # DDG trả về list các object, ta lấy gợi ý đầu tiên
            first_suggestion = data[0].get("phrase", "")
            assert first_suggestion != "", "Không lấy được từ khóa gợi ý!"