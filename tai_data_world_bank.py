from pathlib import Path
import pandas as pd
import re

# Lấy đường dẫn thư mục hiện tại
BASE_DIR = Path(__file__).resolve().parent

# ĐỊNH DẠNG: "Tên_File_Gốc.csv": "Tên_Cột_Sẽ_Đặt"
INPUT_FILES = {
    "Edu_Spending_GDP_raw.csv": "Edu_Spending_GDP",
    "GDP_per_Capita_raw.csv": "GDP_per_Capita",
    "Health_Spending_GDP_raw.csv": "Health_Spending_GDP",
    "Internet_Usage_raw.csv": "Internet_Usage",
    "Learning_Outcome_raw.csv": "Learning_Outcome",
    "Unemployment_Rate_raw.csv": "Unemployment_Rate",
    "Population_Total_raw.csv": "Population_Total",
    "Inflation_Rate_raw.csv": "Inflation_Rate",
    "Trade_Openness_GDP_raw.csv": "Trade_Openness_GDP",
    # Sửa lại 3 dòng mới cho đúng định dạng của bạn:
    "GFCF_GDP_raw.csv": "GFCF_GDP",
    "Population_Growth_raw.csv": "Population_Growth",
    "Labor_Force_raw.csv": "Labor_Force",
}

OUTPUT_FILE = BASE_DIR / "merged_raw_data.csv"

def to_long_format(df: pd.DataFrame, value_name: str) -> pd.DataFrame:
    # Tìm các cột có định dạng năm (ví dụ: YR2004 hoặc 2004)
    year_columns = [col for col in df.columns if re.search(r"(\d{4})", str(col))]
    
    long_df = df.melt(
        id_vars=["economy"],
        value_vars=year_columns,
        var_name="Year",
        value_name=value_name,
    )
    
    # Dùng extract số để xử lý cả 'YR2004' và '2004' một cách an toàn
    long_df["Year"] = long_df["Year"].astype(str).str.extract(r"(\d+)").astype(int)
    return long_df

def main() -> None:
    merged_df = None

    for file_name, indicator_name in INPUT_FILES.items():
        file_path = BASE_DIR / file_name
        
        # Kiểm tra file có tồn tại không để tránh crash
        if not file_path.exists():
            print(f"⚠️ Cảnh báo: Không tìm thấy {file_name}. Bỏ qua...")
            continue
            
        current_df = pd.read_csv(file_path)
        
        # Đảm bảo cột đầu tiên là 'economy' (wbgapi đôi khi để tên khác)
        if 'economy' not in current_df.columns:
            current_df.rename(columns={current_df.columns[0]: 'economy'}, inplace=True)
            
        current_long = to_long_format(current_df, indicator_name)

        if merged_df is None:
            merged_df = current_long
        else:
            merged_df = merged_df.merge(current_long, on=["economy", "Year"], how="outer")

    if merged_df is not None:
        # Sắp xếp lại cho đẹp theo nước và năm
        merged_df = merged_df.sort_values(["economy", "Year"]).reset_index(drop=True)
        merged_df.to_csv(OUTPUT_FILE, index=False)
        print(f"✅ Đã gộp thành công {len(merged_df.columns)-2} chỉ số vào file: {OUTPUT_FILE}")
    else:
        print("❌ Không có dữ liệu nào được gộp!")

if __name__ == "__main__":
    main()