import pytest
import requests
import allure

BASE_URL = "http://host.docker.internal:5000" 

@allure.epic("API & Backend Testing")
@allure.feature("Backend Endpoints Validation")
class TestBackendAPI:

    @allure.title("API_01: Đăng nhập Admin qua Form Request")
    def test_api_admin_login(self):
        client = requests.Session()
        payload = {"email": "admin@gmail.com", "password": "123"}
        response = client.post(f"{BASE_URL}/login", data=payload, allow_redirects=False)
        with allure.step("Xác minh chuyển hướng đến trang dashboard"):
            assert response.status_code == 302
            assert "/admin/dashboard" in response.headers.get("Location", "")

    @allure.title("API_02: Kiểm tra bảo mật (Chặn truy cập Admin khi chưa login)")
    def test_api_security_admin_route(self):
        response = requests.get(f"{BASE_URL}/admin/dashboard", allow_redirects=False)
        with allure.step("Xác minh bị đẩy về trang đăng nhập"):
            assert response.status_code == 302
            assert "/login" in response.headers.get("Location", "")

    @allure.title("API_03: Đặt phòng thành công (Gửi đầy đủ thông tin & Ngày tháng)")
    def test_api_book_room_success(self):
        with allure.step("Setup: Đăng nhập Admin và Reset phòng số 1 về Trống"):
            client = requests.Session()
            client.post(f"{BASE_URL}/login", data={"email": "admin@gmail.com", "password": "123"})
            client.post(f"{BASE_URL}/admin/rooms/reset/1")

        payload = {
            "room_id": 1, 
            "customer_name": "API Tester",
            "phone": "0999888777",
            "check_in": "2026-10-10",
            "check_out": "2026-10-15"
        }
        with allure.step("Gửi request POST /api/book dạng JSON"):
            response = requests.post(f"{BASE_URL}/api/book", json=payload)
            
        with allure.step("Kiểm tra phản hồi 201 Thành công"):
            assert response.status_code == 201
            assert "thành công" in response.json().get("message", "").lower()

    @allure.title("API_04: Đặt phòng thất bại (Phòng đang giữ/đã đặt)")
    def test_api_book_room_fail_already_booked(self):
        # Phòng 1 vừa được đặt ở API_03, nên giờ đặt lại sẽ lỗi
        payload = {
            "room_id": 1, 
            "customer_name": "Ghost User",
            "phone": "000",
            "check_in": "2026-11-01",
            "check_out": "2026-11-05"
        }
        response = requests.post(f"{BASE_URL}/api/book", json=payload)
        with allure.step("Xác minh API báo lỗi 400"):
            assert response.status_code == 400
            assert "đã có người đặt" in response.json().get("error", "").lower()

    @allure.title("API_05: Đặt phòng thất bại (Gửi ID phòng không tồn tại)")
    def test_api_book_room_fail_not_exist(self):
        payload = {"room_id": 99999, "customer_name": "Ghost", "phone": "000", "check_in": "2026-01-01", "check_out": "2026-01-02"}
        response = requests.post(f"{BASE_URL}/api/book", json=payload)
        with allure.step("Xác minh API chặn lại"):
            assert response.status_code == 400

    @allure.title("API_06: Admin duyệt đơn đặt phòng")
    def test_api_admin_approve_booking(self):
        client = requests.Session()
        client.post(f"{BASE_URL}/login", data={"email": "admin@gmail.com", "password": "123"})
        
        with allure.step("Admin gửi request duyệt đơn số 1"):
            response = client.post(f"{BASE_URL}/admin/bookings/action/1", data={"action": "approve"}, allow_redirects=False)
            assert response.status_code == 302 # redirect về dashboard

    @allure.title("API_07: Admin cập nhật trạng thái phòng")
    def test_api_admin_update_room_status(self):
        client = requests.Session()
        client.post(f"{BASE_URL}/login", data={"email": "admin@gmail.com", "password": "123"})
        
        with allure.step("Đổi trạng thái phòng 2 thành Bảo trì"):
            response = client.post(f"{BASE_URL}/admin/rooms/status/2", data={"status": "Bảo trì"}, allow_redirects=False)
            assert response.status_code == 302

    @allure.title("API_08: Admin Reset phòng về Trống")
    def test_api_admin_reset_room(self):
        client = requests.Session()
        client.post(f"{BASE_URL}/login", data={"email": "admin@gmail.com", "password": "123"})
        
        with allure.step("Reset phòng số 2"):
            response = client.post(f"{BASE_URL}/admin/rooms/reset/2", allow_redirects=False)
            assert response.status_code == 302

    @allure.title("API_09: Admin tạo tài khoản ảo rồi xóa thành công")
    def test_api_admin_create_then_delete_user(self):
        import re
        import random
        client = requests.Session()
        
        # Bước 1: Tạo tài khoản ảo với email ngẫu nhiên để không bị trùng
        fake_email = f"api_delete_{random.randint(1000, 9999)}@gmail.com"
        with allure.step(f"1. Khách đăng ký tài khoản ảo ({fake_email})"):
            reg_payload = {
                "full_name": "Acc Test Xóa",
                "email": fake_email,
                "phone": "0123456789",
                "password": "123"
            }
            client.post(f"{BASE_URL}/register", data=reg_payload)
            
        # Bước 2: Đăng nhập quyền Admin
        with allure.step("2. Đăng nhập quyền Admin"):
            client.post(f"{BASE_URL}/login", data={"email": "admin@gmail.com", "password": "123"})
            
        # Bước 3: Vào Dashboard và dùng Regex để "móc" cái ID của email vừa tạo ra
        with allure.step("3. Quét trang Dashboard để tìm ID của tài khoản vừa tạo"):
            dash_resp = client.get(f"{BASE_URL}/admin/dashboard")
            
            # Mẫu Regex tìm ID dựa vào email trong cấu trúc thẻ <td> của bảng
            regex_pattern = r"<td>(\d+)</td>\s*<td><b>.*?</b></td>\s*<td>" + re.escape(fake_email) + r"</td>"
            match = re.search(regex_pattern, dash_resp.text)
            
            if match:
                user_id = match.group(1)
            else:
                pytest.fail("LỖI: Không tìm thấy tài khoản ảo vừa tạo trên Dashboard!")

        # Bước 4: Gọi API xóa đúng cái ID đó
        with allure.step(f"4. Gọi API xóa tài khoản mang ID {user_id}"):
            del_resp = client.post(f"{BASE_URL}/admin/users/delete/{user_id}", allow_redirects=False)
            
            # Xác minh API chạy thành công và trả về mã điều hướng (302)
            assert del_resp.status_code == 302
            assert "/admin/dashboard" in del_resp.headers.get("Location", "")