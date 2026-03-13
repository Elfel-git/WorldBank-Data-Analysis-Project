import wbgapi as wb
from pathlib import Path

# Danh sách mã chỉ số khớp với yêu cầu của nhóm bạn
INDICATORS = {
    #"NY.ADJ.AEDU.GN.ZS": "Edu_Spending_GDP_raw.csv",
    #"NY.GDP.PCAP.CD": "GDP_per_Capita_raw.csv",
    #"SH.XPD.CHEX.GD.ZS": "Health_Spending_GDP_raw.csv",
    #"IT.NET.USER.ZS": "Internet_Usage_raw.csv",
    #"SE.PRM.CMPT.ZS": "Learning_Outcome_raw.csv",
    #"SL.UEM.TOTL.ZS": "Unemployment_Rate_raw.csv",
    'NE.GDI.FTOT.ZS': 'GFCF_GDP_raw.csv',
    'SP.POP.GROW': 'Population_Growth_raw.csv',
    'SL.TLF.TOTL.IN': 'Labor_Force_raw.csv',
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