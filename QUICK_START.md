# 🚀 QUICK START GUIDE

## ⏱️ 5 Phút Setup & Chạy Pipeline

### Step 1: Mở PowerShell/Terminal

Windows:

```powershell
# Mở PowerShell tại folder dự án
cd e:\WorldBank-Data-Analysis-Project
```

macOS/Linux:

```bash
cd ~/path/to/WorldBank-Data-Analysis-Project
```

---

### Step 2: Tạo Conda Environment (lần đầu tiên)

```bash
# Cách tốt nhất (1 command)
conda env create -f environment.yml -y

# Activate environment
conda activate worldbank-analysis
```

⏱️ **Thời gian**: 2-3 phút (phụ thuộc vào internet)

---

### Step 3: Chạy Pipeline

```bash
# Chạy với mặc định
python run_full_pipeline.py default

# Hoặc với scenario khác
python run_full_pipeline.py baseline
```

⏱️ **Thời gian**: 30-60 giây

---

### Step 4: Xem Kết Quả ✅

```bash
# Mở kết quả
open pipeline_execution/outputs/latest/dataset_final.csv

# Hoặc xem diagnostic report
cat pipeline_execution/outputs/latest/diagnostic_report.csv
```

---

## 📊 Output Files

```
pipeline_execution/outputs/latest/
├── dataset_final.csv           📊 Dữ liệu đã xử lý (5546 rows, 11 columns)
├── diagnostic_report.csv       📋 Báo cáo chẩn đoán
├── boxplots.png                📈 Biểu đồ phân phối
├── histograms.png              📉 Histogram
├── config.yaml                 ⚙️ Configuration
├── scaler_model.pkl            🔧 Preprocessing model
└── processing_metadata.json    📝 Metadata
```

---

## ✅ Verification

Nếu không gặp lỗi, pipeline hoạt động bình thường:

```
🎉 PIPELINE EXECUTION COMPLETE
├── PHASE 0: DATA INTEGRATION ✓
├── PHASE 1: AUTO PROFILING & DIAGNOSTICS ✓
└── PHASE 2: EXECUTION PIPELINE ✓
```

---

## ❌ Troubleshooting

### "conda not recognized"

```bash
# Cài Miniconda từ: https://docs.conda.io/projects/miniconda/
# Sau đó khởi động lại Terminal/PowerShell
```

### "ModuleNotFoundError"

```bash
# Activate environment lại
conda activate worldbank-analysis

# Hoặc reinstall packages
pip install -r requirements.txt
```

### "Dataset not found"

```bash
# Kiểm tra folder nam/ có file CSV không
ls nam/
# Phải có 9 file: Access to electricity.csv, GDP per capita.csv, ...
```

---

## 📚 Tài Liệu Chi Tiết

- `CONDA_SETUP_GUIDE.md` - Hướng dẫn setup chi tiết
- `REFACTORING_SUMMARY.md` - Các thay đổi refactoring
- `pipeline_execution/README.md` - Pipeline documentation

---

## 💡 Tips

✅ **Lần đầu**: Activation environment

```bash
conda activate worldbank-analysis
```

✅ **Chạy lại**: Không cần tạo environment

```bash
conda activate worldbank-analysis
python run_full_pipeline.py default
```

✅ **Deactivate** (nếu cần)

```bash
conda deactivate
```

---

## 🎯 Tiếp Theo

- Xem `outputs/latest/dataset_final.csv` cho ML models
- Xem `outputs/latest/diagnostic_report.csv` cho data quality
- Xem biểu đồ: `boxplots.png`, `histograms.png`

---

**Status**: Ready to use ✅  
**Last Updated**: 2026-04-13
