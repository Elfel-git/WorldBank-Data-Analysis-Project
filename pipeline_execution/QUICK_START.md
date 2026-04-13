# Pipeline Quick Start - Kiến Trúc Mới

## 🎯 Mục Tiêu

Chạy pipeline **nhiều lần** với **config khác nhau** mà **không mất data**.

---

## ⚡ 5 Phút Quick Start

### Step 1: Tạo Scenarios

```bash
cd e:\WorldBank-Data-Analysis-Project\pipeline_execution

# Tạo folder scenarios
mkdir outputs\scenarios

# Copy config template
copy config_template.yaml outputs\scenarios\baseline_config.yaml
copy config_template.yaml outputs\scenarios\conservative_config.yaml
copy config_template.yaml outputs\scenarios\aggressive_config.yaml
```

### Step 2: Activate Virtual Environment

```bash
& .\.venv\bin\Activate.ps1
```

### Step 3: Chạy 3 Scenarios

```bash
# Scenario 1: Chuẩn
python run_pipeline.py baseline
# ✓ Tạo: outputs/runs/run_20260411_143000_baseline/

# Scenario 2: Cảnh báo
python run_pipeline.py conservative
# ✓ Tạo: outputs/runs/run_20260411_145200_conservative/

# Scenario 3: Nới lỏng
python run_pipeline.py aggressive
# ✓ Tạo: outputs/runs/run_20260411_150430_aggressive/
```

### Step 4: Xem Kết Quả

```bash
# Liệt kê tất cả runs
python manage_runs.py list

# So sánh 3 scenarios
python manage_runs.py compare

# Chi tiết về run baseline
python manage_runs.py info baseline

# Xem run mới nhất
python manage_runs.py latest
```

### Step 5: Xem Logs

```bash
# Xem logs của run mới nhất
tail -f outputs/latest/logs/pipeline.log

# Xem logs chi tiết từ PHASE 0 (Data Integration)
tail -f outputs/latest/logs/data_integration.log

# Xem logs từ PHASE 1 (Diagnostics)
tail -f outputs/latest/logs/diagnostics.log

# Xem logs từ PHASE 2 (Processing)
tail -f outputs/latest/logs/processing.log

# Search errors trong tất cả logs
grep "ERROR" outputs/latest/logs/*.log
```

✅ **Done!** Bây giờ bạn có 3 folders riêng với kết quả từ 3 scenarios khác nhau, cùng logs chi tiết từ mỗi phase.

---

## 📝 Log Structure

Mỗi run tạo folder `logs/` chứa 4 files:
- **pipeline.log** - Logs chính của pipeline
- **data_integration.log** - Logs từ PHASE 0 (merge CSVs)
- **diagnostics.log** - Logs từ PHASE 1 (phân tích)
- **processing.log** - Logs từ PHASE 2 (xử lý dữ liệu)

Chi tiết xem [LOGGING_GUIDE.md](LOGGING_GUIDE.md)

---

## 📂 Cấu Trúc Kết Quả

```
outputs/
├── scenarios/
│   ├── baseline_config.yaml
│   ├── conservative_config.yaml
│   └── aggressive_config.yaml
│
├── runs/
│   ├── run_20260411_143000_baseline/
│   │   ├── logs/                    # ✨ NEW: Folder logs
│   │   │   ├── pipeline.log
│   │   │   ├── data_integration.log
│   │   │   ├── diagnostics.log
│   │   │   └── processing.log
│   │   ├── config.yaml
│   │   ├── dataset_final.csv
│   │   ├── ... (other files)
│   │   └── run_summary.json
│   │
│   ├── run_20260411_145200_conservative/
│   │   └── (same structure)
│   │
│   └── run_20260411_150430_aggressive/
│       └── (same structure)
│
└── latest/                              # Copy của run mới nhất
    ├── config.yaml
    ├── dataset_final.csv
    └── (other files)
```

---

## 🔧 Cách Chỉnh Sửa Scenarios

### Ví Dụ 1: Sửa Config Baseline

Edit `outputs/scenarios/baseline_config.yaml`:

```yaml
# Baseline: chuẩn (vừa phải)
pipeline:
  name: 'WorldBank Data Processing'
  version: '1.0'

phase1:
  log_transform:
    enabled: true           # Dùng log transform
    base: 10
    add_constant: 1.0
  
  outlier_detection:
    method: 'iqr'
    iqr_multiplier: 1.5     # Chuẩn: 1.5
    action: 'clip'          # Clip outliers

phase2:
  scaling:
    method: 'standard'      # Z-score
  
  imputation:
    method: 'knn'
    n_neighbors: 5          # 5 neighbors
```

### Ví Dụ 2: Sửa Config Conservative (Cảnh báo)

Edit `outputs/scenarios/conservative_config.yaml`:

```yaml
# Conservative: nới lỏng hơn (ít loại outliers, robust scaling)
phase1:
  log_transform:
    enabled: true
  
  outlier_detection:
    method: 'iqr'
    iqr_multiplier: 2.0     # Nới lỏng: 2.0 (ít loại outliers)
    action: 'clip'

phase2:
  scaling:
    method: 'robust'        # Robust scaling (tốt với outliers)
  
  imputation:
    method: 'knn'
    n_neighbors: 3          # Ít neighbors (sparse data)
```

### Ví Dụ 3: Sửa Config Aggressive (Nới Lỏng)

Edit `outputs/scenarios/aggressive_config.yaml`:

```yaml
# Aggressive: chặt chẽ (tìm nhiều outliers)
phase1:
  log_transform:
    enabled: true
  
  outlier_detection:
    method: 'isolation_forest'  # Advanced method
    isolation_forest_contamination: 0.05
    action: 'impute'            # Thay bằng NaN
  
  phase2:
    scaling:
      method: 'standard'
    
    imputation:
      method: 'knn'
      n_neighbors: 7            # Nhiều neighbors
```

---

## 📊 Ví Dụ Chạy Full Workflow

```bash
# 1. Tạo 3 scenarios (một lần setup)
mkdir outputs\scenarios
copy config_template.yaml outputs\scenarios\baseline_config.yaml
copy config_template.yaml outputs\scenarios\conservative_config.yaml
copy config_template.yaml outputs\scenarios\aggressive_config.yaml

# 2. Edit config files (baseline, conservative, aggressive)
# ... edit outputs/scenarios/*.yaml files ...

# 3. Chạy 3 scenarios
python run_pipeline.py baseline
python run_pipeline.py conservative
python run_pipeline.py aggressive

# ✓ Tạo 3 folders riêng:
# - outputs/runs/run_20260411_143000_baseline/
# - outputs/runs/run_20260411_145200_conservative/
# - outputs/runs/run_20260411_150430_aggressive/

# 4. View results
python manage_runs.py list
python manage_runs.py compare
python manage_runs.py info baseline

# 5. So sánh 3 scenarios
python -c "
import pandas as pd
from pathlib import Path

paths = [
    'outputs/runs/run_20260411_143000_baseline/dataset_final.csv',
    'outputs/runs/run_20260411_145200_conservative/dataset_final.csv',
    'outputs/runs/run_20260411_150430_aggressive/dataset_final.csv',
]

for path in paths:
    df = pd.read_csv(path)
    name = Path(path).parent.name
    print(f'{name}: shape={df.shape}, missing={df.isna().sum().sum()}')
"

# Output:
# run_20260411_143000_baseline: shape=(156, 20), missing=0
# run_20260411_145200_conservative: shape=(156, 20), missing=0
# run_20260411_150430_aggressive: shape=(156, 20), missing=5
```

---

## 🎯 Usage Patterns

### Pattern 1: Chạy Tuần Tự (Lần Lượt)

```bash
# Week 1
python run_pipeline.py baseline
# → outputs/runs/run_20260411_143000_baseline/

# Week 2: Chạy lại (dùng data mới)
python run_pipeline.py baseline
# → outputs/runs/run_20260418_143000_baseline/  (folder MỚI!)

# So sánh
python manage_runs.py compare baseline
```

### Pattern 2: So Sánh Scenarios

```bash
# Tạo 3 scenarios khác nhau
python run_pipeline.py baseline
python run_pipeline.py conservative
python run_pipeline.py aggressive

# So sánh
python manage_runs.py compare 3

# Output:
# ┌─────────────┬──────────────────┬──────────────┬───────────────┐
# │ Scenario    │ Timestamp        │ Size (MB)    │ Files Present │
# ├─────────────┼──────────────────┼──────────────┼───────────────┤
# │ AGGRESSIVE  │ 20260411_150430  │ 1.22         │ 10            │
# │ CONSERVATIVE│ 20260411_145200  │ 1.18         │ 10            │
# │ BASELINE    │ 20260411_143000  │ 1.21         │ 10            │
# └─────────────┴──────────────────┴──────────────┴───────────────┘
```

### Pattern 3: Lưu Trữ & Backup

```bash
# Liệt kê tất cả runs
python manage_runs.py list

# Tìm runs cũ
python manage_runs.py cleanup 30

# Backup runs (thủ công)
xcopy outputs\runs\run_20260411_143000_baseline backup\
```

---

## 🐛 Troubleshooting

| Vấn đề | Nguyên nhân | Cách Fix |
|-------|----------|---------|
| "No runs found" | Folder outputs/runs chưa có | Chạy `python run_pipeline.py baseline` |
| "Scenario config not found" | File config không ở outputs/scenarios/ | Copy config vào outputs/scenarios/ |
| "latest folder empty" | Chưa chạy run nào | Chạy `python run_pipeline.py default` |
| Python ModuleNotFoundError | Virtual env chưa activate | Run `.\.venv\bin\Activate.ps1` |

---

## 📋 Tóm Tắt Commands

```bash
# Setup (một lần)
mkdir outputs\scenarios
copy config_template.yaml outputs\scenarios\baseline_config.yaml

# Run pipeline
python run_pipeline.py baseline           # Chạy scenario baseline
python run_pipeline.py conservative       # Chạy scenario conservative

# Manage runs
python manage_runs.py list                # Liệt kê tất cả runs
python manage_runs.py compare             # So sánh runs
python manage_runs.py info baseline       # Chi tiết về run
python manage_runs.py latest              # Run mới nhất

# Access results
outputs/runs/run_20260411_143000_baseline/dataset_final.csv
outputs/latest/dataset_final.csv
```

---

## ✨ Lợi Ích So Với Cấu Trúc Cũ

| Yếu tố | Cũ | Mới |
|--------|----|----|
| Chạy nhiều lần | ❌ Ghi đè | ✅ Folder riêng |
| So sánh configs | ❌ Khó | ✅ Dễ (folder riêng) |
| Lưu config | ❌ Không | ✅ Cùng kết quả |
| Trace history | ❌ Không | ✅ Tất cả runs |
| Timestamps | ❌ Không | ✅ Tự động |
| Latest access | ❌ Không | ✅ `outputs/latest/` |

---

## 🚀 Next Steps

1. ✅ Setup scenarios: `outputs/scenarios/*.yaml`  
2. ✅ Chạy pipeline: `python run_pipeline.py <scenario>`
3. ✅ Xem kết quả: `outputs/runs/` hoặc `outputs/latest/`
4. ✅ So sánh: `python manage_runs.py compare`
5. ✅ Dùng kết quả: `outputs/latest/dataset_final.csv` cho ML models

🎉 **Bạn đã sẵn sàng chạy unlimited scenarios mà không mất data!**
