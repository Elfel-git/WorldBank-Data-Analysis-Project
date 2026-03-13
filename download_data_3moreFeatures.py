import wbgapi as wb
from pathlib import Path

# Thêm 3 chỉ số quan trọng để bộ dữ liệu "xịn" hơn
NEW_INDICATORS = {
    "SP.POP.TOTL": "Population_Total_raw.csv", # Tổng dân số - biến này có xu hướng tăng tuyến tính hoặc hàm mũ nhẹ nếu tăng đột ngột thì có thể là nhiễu hoặc thay đổi về địa giới hành chính 
    "FP.CPI.TOTL.ZG": "Inflation_Rate_raw.csv", # Tỷ lệ lam phát (Theo chỉ số tiêu dùng CPI )
    "NE.TRD.GNFS.ZS": "Trade_Openness_GDP_raw.csv", # Độ mở thương mại (Xuất khẩu + Nhập khẩu ) / GDP x 100 
}

BASE_DIR = Path(__file__).resolve().parent

def download_extra():
    print("--- Đang tải bổ sung 3 chỉ số chiến lược (2004 - nay) ---")
    years = range(2004, 2025)
    
    for code, file_name in NEW_INDICATORS.items():
        try:
            print(f"Đang lấy dữ liệu: {file_name}...")
            # Tải dữ liệu từ API
            data = wb.data.DataFrame(code, time=years, labels=False)
            data.index.name = 'economy'
            
            # Lưu file CSV
            data.to_csv(BASE_DIR / file_name)
            print(f"✅ Xong: {file_name}")
        except Exception as e:
            print(f"❌ Lỗi khi tải {file_name}: {e}")

    print("\n--- Hoàn tất tải bổ sung! ---")

if __name__ == "__main__":
    download_extra()