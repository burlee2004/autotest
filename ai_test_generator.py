import os
import time
import google.generativeai as genai
import re
from dotenv import load_dotenv

load_dotenv()
# 1. Cấu hình API Key từ file .env
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Sử dụng model Gemini thế hệ mới (Năm 2026)
model = genai.GenerativeModel('gemini-3.5-flash-lite')

def generate_test_script(scenario_description):
    print(f"\n[AI] Dang suy nghi va viet code cho kich ban: '{scenario_description}'...")
    
    prompt = f"""
    Bạn là một kỹ sư kiểm thử tự động (QA Automation Engineer) chuyên nghiệp.
    Dự án của tôi sử dụng Python, Pytest, Selenium và Allure Report.
    
    Các hàm hỗ trợ đã có sẵn:
    - fixture `driver` (trả về đối tượng Selenium WebDriver).
    - KHÔNG DÙNG fixture config để lấy URL. Phải sử dụng ĐÚNG địa chỉ URL được yêu cầu trong kịch bản.
    
    Yêu cầu:
    Hãy viết một file code hoàn chỉnh (.py) chứa kịch bản kiểm thử cho tình huống sau:
    "{scenario_description}"
    
    Quy tắc viết code:
    1. Sử dụng `@allure.title` và `with allure.step():`.
    2. Import đầy đủ các thư viện cần thiết (pytest, allure, time, selenium By, WebDriverWait...).
    3. Tự giả định các ID hoặc Class của các phần tử HTML sao cho hợp lý nhất với ngữ cảnh.
    4. CHỈ TRẢ VỀ CODE PYTHON, KHÔNG GIẢI THÍCH, KHÔNG CHỨA DẤU MARKDOWN ```python ở đầu và cuối.
    """
    
    try:
        response = model.generate_content(prompt)
        code = response.text.strip()
        
        # Xóa thẻ markdown nếu AI lỡ sinh ra
        if code.startswith("```python"):
            code = code[9:]
        if code.endswith("```"):
            code = code[:-3]
            
        return code.strip()
    except Exception as e:
        print(f"[LOI] Khong the ket noi voi Gemini API: {e}")
        return None

if __name__ == "__main__":
    import sys
    print("="*50)
    print("CHUONG TRINH AI TU DONG SINH CODE TEST BANG GEMINI")
    print("="*50)
    
    # Nếu chạy qua Jenkins (truyền tham số)
    if len(sys.argv) > 1:
        scenario = sys.argv[1]
        print(f"Kich ban nhan tu Jenkins: {scenario}")
    else:
        scenario = input("\nNhap kich ban ban muon AI viet: ")

    
    if scenario:
        code_result = generate_test_script(scenario)
        
        if code_result:
            # Tạo tên file tự động dựa vào timestamp
            file_name = f"test_ai_generated_{int(time.time())}.py"
            file_path = os.path.join("tests", "ai_generated", file_name)
            
            # Đảm bảo thư mục tồn tại
            os.makedirs(os.path.join("tests", "ai_generated"), exist_ok=True)
            
            # Lưu code vào file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code_result)
                
            print(f"\n[THANH CONG] AI da viet xong code va luu vao file: {file_path}")
            print("Ban co the mo file do ra de xem hoac chay ngay bang lenh: pytest " + file_path)
