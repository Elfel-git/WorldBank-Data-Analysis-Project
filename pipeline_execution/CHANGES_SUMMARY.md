# ✨ Pipeline Architecture Updates - Summary

## 📋 Thay Đổi Chính

Kiến trúc folder `outputs/` đã được cải thiện để hỗ trợ **chạy nhiều scenarios mà không mất data**.

---

## 🎯 Vấn Đề Cũ

```
outputs/
├── dataset_merged.csv      ❌ Chạy lần 2 → bị ghi đè
├── dataset_final.csv       ❌ Chạy lần 2 → bị ghi đè
├── diagnostic_report.csv   ❌ Chạy lần 2 → bị ghi đè
└── ...                     ❌ Tất cả files bị mất
```

**Kết quả:** Nếu chạy `scenario 1`, rồi chạy `scenario 2`, kết quả của `scenario 1` sẽ bị mất.

---

## ✅ Giải Pháp Mới

```
outputs/
├── scenarios/                    ← NEW: Lưu config cho các kịch bản
│   ├── baseline_config.yaml
│   ├── conservative_config.yaml
│   └── aggressive_config.yaml
│
├── runs/                         ← NEW: Lưu kết quả từng lần chạy
│   ├── run_20260411_143000_baseline/
│   │   ├── config.yaml           ← Config được dùng
│   │   ├── dataset_merged.csv
│   │   ├── dataset_final.csv
│   │   └── ... (other files)
│   │
│   ├── run_20260411_145200_conservative/
│   └── run_20260411_150430_aggressive/
│
└── latest/                       ← NEW: Copy của run mới nhất
    ├── dataset_final.csv
    └── ... (other files)
```

**Lợi ích:**
- ✅ Không bị ghi đè
- ✅ Dễ so sánh kết quả từ các scenarios khác nhau
- ✅ Lưu config cùng kết quả → dễ reproduce
- ✅ Tự động timestamps → biết khi nào chạy
- ✅ Folder `latest` → dễ access kết quả mới nhất

---

## 📝 Files Mới Được Tạo

### 1. `modules/run_manager.py` 🆕
```
Chức năng: Quản lý cấu trúc outputs/
- Tạo run directory với timestamp
- Lưu config vào run directory
- Update folder 'latest'
- Liệt kê & so sánh runs
- Generate run summaries
```

### 2. `OUTPUTS_STRUCTURE.md` 🆕
```
Tài liệu: Hướng dẫn cấu trúc mới
- Giải thích cấu trúc
- Cách chạy pipeline
- Cách quản lý runs
- FAQ
```

### 3. `QUICK_START.md` 🆕
```
Tài liệu: Quick start
- 5 phút setup
- Ví dụ cụ thể
- Troubleshooting
```

### 4. `manage_runs.py` 🆕
```
Script: Quản lý scenarios và runs
- python manage_runs.py list         # Liệt kê runs
- python manage_runs.py compare      # So sánh
- python manage_runs.py info <run>   # Chi tiết
- python manage_runs.py scenarios    # Liệt kê configs
```

### 5. `outputs/.gitignore` 🆕
```
Git ignore: Ignore outputs/ trừ scenarios/
- Các file CSV, PNG, PKL NOT tracked
- Chỉ scenarios/ được tracked
```

---

## 🔄 Files Được Sửa

### 1. `run_pipeline.py` ✏️
```
Thay đổi:
- Import RunManager
- run_phase_0/1/2 nhận run_dir parameter
- Lưu files vào run_dir (không phải outputs root)
- main() tạo run directory ở đầu
- main() update latest folder ở cuối
- main() show run list
- Nhận scenario_name từ command line
```

Trước:
```bash
python run_pipeline.py
```

Sau:
```bash
python run_pipeline.py baseline           # Scenario-aware
python run_pipeline.py conservative
```

---

## 🚀 Cách Chạy (Mới)

```bash
# Step 1: Setup (một lần)
mkdir outputs\scenarios
copy config_template.yaml outputs\scenarios\baseline_config.yaml
copy config_template.yaml outputs\scenarios\conservative_config.yaml

# Step 2: Chạy nhiều scenarios
python run_pipeline.py baseline
python run_pipeline.py conservative
python run_pipeline.py aggressive

# ✓ Tạo 3 folders riêng:
# - outputs/runs/run_20260411_143000_baseline/
# - outputs/runs/run_20260411_145200_conservative/
# - outputs/runs/run_20260411_150430_aggressive/

# Step 3: Quản lý & so sánh
python manage_runs.py list
python manage_runs.py compare
python manage_runs.py info baseline
```

---

## 📊 Ví Dụ: Chạy 3 Scenarios

```bash
# Run 1: Baseline
python run_pipeline.py baseline

Log Output:
---
PHASE 0: DATA INTEGRATION
PHASE 1: AUTO PROFILING & DIAGNOSTICS
PHASE 2: EXECUTION PIPELINE
✓ PHASE 2 Complete

📂 Run Directory: E:\...\outputs\runs\run_20260411_143000_baseline
📋 Generated Files:
  ✓ boxplots.png                             0.23 MB
  ✓ config.yaml                              0.00 MB
  ✓ dataset_final.csv                        0.33 MB
  ... (10 files total)

ALL RUNS:
  1. BASELINE               | 20260411_143000 | 1.21 MB
---

# Run 2: Conservative (mà không mất kết quả từ baseline)
python run_pipeline.py conservative

Log Output:
---
✓ PHASE 2 Complete

📂 Run Directory: E:\...\outputs\runs\run_20260411_145200_conservative

ALL RUNS:
  1. CONSERVATIVE           | 20260411_145200 | 1.18 MB
  2. BASELINE               | 20260411_143000 | 1.21 MB
---

# Run 3: Aggressive
python run_pipeline.py aggressive

# ALL RUNS:
#   1. AGGRESSIVE             | 20260411_150430 | 1.22 MB
#   2. CONSERVATIVE           | 20260411_145200 | 1.18 MB
#   3. BASELINE               | 20260411_143000 | 1.21 MB
```

---

## 🔗 So Sánh Kết Quả 3 Scenarios

```bash
python manage_runs.py compare

Output:
┌─────────────┬──────────────────┬──────────────┬───────────────┐
│ Scenario    │ Timestamp        │ Size (MB)    │ Files Present │
├─────────────┼──────────────────┼──────────────┼───────────────┤
│ AGGRESSIVE  │ 20260411_150430  │ 1.22         │ 10            │
│ CONSERVATIVE│ 20260411_145200  │ 1.18         │ 10            │
│ BASELINE    │ 20260411_143000  │ 1.21         │ 10            │
└─────────────┴──────────────────┴──────────────┴───────────────┘
```

---

## 💾 Truy Cập Dữ Liệu

### Cách 1: Folder Latest (Mới Nhất)
```python
import pandas as pd

df = pd.read_csv('./outputs/latest/dataset_final.csv')
print(df.shape)
```

### Cách 2: Specific Run
```python
# Baseline results
df_baseline = pd.read_csv('./outputs/runs/run_20260411_143000_baseline/dataset_final.csv')

# Conservative results
df_conservative = pd.read_csv('./outputs/runs/run_20260411_145200_conservative/dataset_final.csv')

# So sánh
print("Baseline shape:", df_baseline.shape)
print("Conservative shape:", df_conservative.shape)
```

---

## 🔄 Backward Compatibility

Jupyter notebooks hiện tại không cần sửa nếu:
- Chỉ dùng `./outputs/latest/` (hoặc `./outputs/` nếu dùng latest)
- Nếu dùng direct path, sửa thành `./outputs/latest/`

Cách thêm RunManager support vào notebooks:
```python
# Thêm cell này ở đầu notebook
from modules.run_manager import RunManager
from pathlib import Path

rm = RunManager('./outputs')
run_dir = rm.latest_dir  # Hoặc specific run folder

# Sau đó dùng run_dir thay vì './outputs'
```

---

## 📚 Tài Liệu Thêm

- `OUTPUTS_STRUCTURE.md` - Chi tiết cấu trúc
- `QUICK_START.md` - Quick start guide
- `manage_runs.py --help` - Script help

---

## ✨ Benefit Summary

| Trường Hợp | Trước | Sau |
|-----------|-------|-----|
| Chạy scenario 1 | ✓ OK | ✓ OK |
| Chạy scenario 2 | ✗ Mất 1 | ✓ OK (have both) |
| Chạy scenario 3 | ✗ Mất 1,2 | ✓ OK (have all 3) |
| So sánh 3 scenarios | ✗ Không thể | ✓ Dễ dàng |
| Biết config được dùng | ✗ Không biết | ✓ Lưu cùng results |
| Lịch sử (trace back) | ✗ Không có | ✓ Tất cả runs |

---

## 🎉 Ready to Use!

1. ✅ Cập nhật code → Ready
2. ✅ Tài liệu chi tiết
3. ✅ Helper scripts
4. ✅ Backward compatible với notebooks cũ

**Bây giờ bạn có thể chạy unlimited scenarios mà không sợ mất data!** 🚀
