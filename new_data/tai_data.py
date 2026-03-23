# 1. Cài đặt thư viện (Chạy cái này trước nếu chưa cài)
# !pip install wbgapi -q
# Code này dùng để chạy trên nền tảng Kaggle
import wbgapi as wb
from pathlib import Path
import os

# Danh sách mã chỉ số khớp với yêu cầu của nhóm bạn
INDICATORS = {
    "FS.AST.PRVT.GD.ZS": "Domestic credit to private sector.csv", 
    "CM.MKT.LCAP.GD.ZS": "Market capitalization of listed domestic companies.csv", 
    "IT.NET.USER.ZS": "Individuals using the Internet.csv", 
    "EG.ELC.ACCS.ZS": "Access to electricity.csv", 
    "NV.AGR.TOTL.ZS": "Agriculture, forestry, and fishing, value added.csv",  
    "NV.SRV.TOTL.ZS": "Services, value added.csv", 
    'NE.TRD.GNFS.ZS': 'Trade.csv', 
    'BX.KLT.DINV.WD.GD.ZS': 'FDI inflows.csv', 
    'NY.GDP.PCAP.PP.KD' : 'GDP per capita.csv' # Thêm đuôi .csv để đồng bộ
}

# 2. Chỉnh lại đường dẫn cho Kaggle
# Mặc định Kaggle lưu file vào /kaggle/working/
BASE_DIR = Path('/kaggle/working/') 

def download():
    print("--- Bắt đầu tải file CSV từ World Bank (2004 - 2024) ---")
    years = range(2004, 2025) 
    
    for code, file_name in INDICATORS.items():
        try:
            print(f"Đang tải: {file_name}...")
            # labels=False để lấy mã quốc gia (như VNM, USA)
            data = wb.data.DataFrame(code, time=years, labels=False)
            
            # Kiểm tra nếu data trống (tránh lỗi save file rỗng)
            if data.empty:
                print(f"⚠️ Cảnh báo: Dữ liệu cho {code} trống.")
                continue
                
            data.index.name = 'economy'
            
            # Lưu file
            save_path = BASE_DIR / file_name
            data.to_csv(save_path)
            print(f"✅ Đã xong: {file_name}")
            
        except Exception as e:
            print(f"❌ Lỗi khi tải {file_name}: {e}")

    print("\n--- Hoàn tất! Check mục /kaggle/working/ ở panel bên phải ---")

if __name__ == "__main__":
    download()