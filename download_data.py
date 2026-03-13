import wbgapi as wb
from pathlib import Path

# Danh sách mã chỉ số khớp với yêu cầu của nhóm bạn
INDICATORS = {
    "NY.ADJ.AEDU.GN.ZS": "Edu_Spending_GDP_raw.csv", # Chi tiêu cho giáo dục tính theo % thu nhập quốc gia 
    "NY.GDP.PCAP.CD": "GDP_per_Capita_raw.csv", # Tổng sản phẩm quốc nội bình quân đầu người (Theo USD hiện giá)
    "SH.XPD.CHEX.GD.ZS": "Health_Spending_GDP_raw.csv", # CHi tiêu y tế hiện hành so với GDP
    "IT.NET.USER.ZS": "Internet_Usage_raw.csv", # Tỷ lệ người dùng Internet - Phân bố thường là đường cong chữ S trong quá trình phát triển một quốc gia 
    "SE.PRM.CMPT.ZS": "Learning_Outcome_raw.csv", # Tỷ lệ hoàn thành bậc tiểu học 
    "SL.UEM.TOTL.ZS": "Unemployment_Rate_raw.csv", # Tỷ lệ thất nghiệp, một số biến số có chu kỳ cao 
    'NE.GDI.FTOT.ZS': 'GFCF_GDP_raw.csv', # Tỷ lệ hình thành vốn cố định sơ cấp trong GDP, thước đó vào tài sản cố định (nhà máy , hạ tầng )
    'SP.POP.GROW': 'Population_Growth_raw.csv', # Tốc độ tăng trưởng dân số hằng năm 
    'SL.TLF.TOTL.IN': 'Labor_Force_raw.csv', # Tổng lực lượng lao động . quy mô mẫu của quần thể tham gia vào hoạt động konh tế (bao gồm cả người đang làm việc, người đang tìm việc)
}

BASE_DIR = Path(__file__).resolve().parent

def download():
    print("--- Bắt đầu tải 6 file CSV từ World Bank (2004 - nay) ---")
    years = range(2004, 2025) # Lấy từ 2004 đến mới nhất
    
    for code, file_name in INDICATORS.items():
        try:
            print(f"Đang tải: {file_name}...")
            # labels=False để lấy mã quốc gia (như VNM, USA) làm cột 'economy'
            data = wb.data.DataFrame(code, time=years, labels=False)
            data.index.name = 'economy'
            
            # Lưu file vào đúng thư mục
            data.to_csv(BASE_DIR / file_name)
            print(f"✅ Đã xong: {file_name}")
        except Exception as e:
            print(f"❌ Lỗi khi tải {file_name}: {e}")

    print("\n--- Hoàn tất! Bây giờ bạn đã có đủ 6 file CSV ---")

if __name__ == "__main__":
    download()