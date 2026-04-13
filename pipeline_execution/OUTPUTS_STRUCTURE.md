# Pipeline Execution - Updated Structure Guide

## 📁 Cấu Trúc Outputs Mới

```
pipeline_execution/outputs/
├── scenarios/                          # Lưu config cho các kịch bản (scenarios)
│   ├── baseline_config.yaml           # Config 1: Chuẩn (conservative)
│   ├── conservative_config.yaml       # Config 2: Cực kỳ cảnh báo
│   └── aggressive_config.yaml         # Config 3: Nới lỏng outlier
│
├── runs/                              # Lưu kết quả từng lần chạy (được tạo tự động)
│   ├── run_20260411_143000_baseline/
│   │   ├── config.yaml                # Config được dùng cho run này
│   │   ├── dataset_merged.csv
│   │   ├── dataset_final.csv
│   │   ├── diagnostic_report.csv
│   │   ├── diagnostic_report.json
│   │   ├── boxplots.png
│   │   ├── histograms.png
│   │   ├── scaler_model.pkl
│   │   ├── processing_metadata.json
│   │   └── run_summary.json
│   │
│   ├── run_20260411_145200_conservative/
│   │   └── (các file tương tự)
│   │
│   └── run_20260411_150430_aggressive/
│       └── (các file tương tự)
│
└── latest/                            # Copy của run mới nhất (cập nhật tự động)
    ├── config.yaml
    ├── dataset_merged.csv
    ├── dataset_final.csv
    ├── diagnostic_report.csv
    ├── diagnostic_report.json
    ├── boxplots.png
    ├── histograms.png
    ├── scaler_model.pkl
    ├── processing_metadata.json
    └── run_summary.json
```

---

## ✨ Lợi Ích Của Kiến Trúc Mới

| Lợi ích | Giải thích |
|--------|----------|
| ✅ Không mất dữ liệu | Mỗi run có folder riêng → không bị ghi đè |
| ✅ Dễ so sánh | Có thể so sánh kết quả từ các config khác nhau |
| ✅ Lịch sử đầy đủ | Giữ lại tất cả runs để trace back |
| ✅ Config cùng dữ liệu | Mỗi run lưu config được dùng → dễ reproduce |
| ✅ Latest folder | Dễ truy cập dữ liệu mới nhất |
| ✅ Timestamps | Biết chính xác khi nào chạy |

---

## 🚀 Cách Chạy Pipeline

### Bước 1: Tạo Các Config Scenarios

Tạo folder `scenarios/` với các file config:

```bash
cd e:\WorldBank-Data-Analysis-Project\pipeline_execution\outputs\scenarios

# Copy template
copy ..\config_template.yaml baseline_config.yaml
copy ..\config_template.yaml conservative_config.yaml
copy ..\config_template.yaml aggressive_config.yaml
```

**Hoặc tạo bằng Python:**
```python
import yaml
from pathlib import Path

scenarios_dir = Path('./outputs/scenarios')
scenarios_dir.mkdir(exist_ok=True)

# Baseline: tiêu chuẩn
baseline = {
    'pipeline': {'name': 'WorldBank Data processing', 'version': '1.0'},
    'phase1': {
        'log_transform': {'enabled': True},
        'outlier_detection': {'method': 'iqr', 'iqr_multiplier': 1.5, 'action': 'clip'}
    },
    'phase2': {
        'scaling': {'method': 'standard'},
        'imputation': {'n_neighbors': 5}
    }
}

with open(scenarios_dir / 'baseline_config.yaml', 'w') as f:
    yaml.dump(baseline, f)
```

### Bước 2: Chạy Pipeline Với Scenario Khác Nhau

```bash
# Kích hoạt environment
cd e:\WorldBank-Data-Analysis-Project\pipeline_execution
& .\.venv\bin\Activate.ps1

# Chạy với scenario mặc định
python run_pipeline.py default

# Chạy với scenario 'baseline'
python run_pipeline.py baseline

# Chạy với scenario 'conservative'
python run_pipeline.py conservative

# Chạy với scenario 'aggressive'
python run_pipeline.py aggressive
```

### Bước 3: Kết Quả

Mỗi lần chạy sẽ:
1. ✓ Tạo folder `run_YYYYMMDD_HHMMSS_scenario_name/`
2. ✓ Lưu tất cả files vào folder đó
3. ✓ Tạo `run_summary.json` với thông tin run
4. ✓ Copy tất cả vào folder `latest/`

Log output example:
```
======================================================================
PHASE 0: DATA INTEGRATION
======================================================================
✓ PHASE 0 Complete: E:\...outputs\runs\run_20260411_143000_baseline\dataset_merged.csv
  Shape: (156, 20)
  File size: 0.15 MB

======================================================================
PHASE 1: AUTO PROFILING & DIAGNOSTICS
======================================================================
✓ PHASE 1 Complete
  Reports: diagnostic_report.csv, diagnostic_report.json
  Visualizations: boxplots.png, histograms.png

======================================================================
PHASE 2: EXECUTION PIPELINE
======================================================================
✓ PHASE 2 Complete
  Final shape: (156, 20)
  Missing values: 0

======================================================================
🎉 PIPELINE EXECUTION COMPLETE
======================================================================

📂 Run Directory: E:\...outputs\runs\run_20260411_143000_baseline

📋 Generated Files:
  ✓ boxplots.png                             0.23 MB
  ✓ config.yaml                              0.00 MB
  ✓ dataset_final.csv                        0.33 MB
  ✓ dataset_merged.csv                       0.15 MB
  ✓ diagnostic_report.csv                    0.01 MB
  ✓ diagnostic_report.json                   0.02 MB
  ✓ histograms.png                           0.45 MB
  ✓ processing_metadata.json                 0.01 MB
  ✓ run_summary.json                         0.00 MB
  ✓ scaler_model.pkl                         0.01 MB

======================================================================
📁 Latest run: E:\...outputs\latest
📊 Use outputs/latest/dataset_final.csv for ML models!
======================================================================

📚 ALL RUNS:

  1. BASELINE               | 20260411_143000 | 1.21 MB
  2. CONSERVATIVE           | 20260411_145200 | 1.18 MB
  3. AGGRESSIVE             | 20260411_150430 | 1.22 MB
```

---

## 📊 Cách Quản Lý Runs

### 1. Liệt Kê Tất Cả Runs

```python
from modules.run_manager import RunManager

rm = RunManager('./outputs')

# Liệt kê 10 runs gần đây nhất
runs = rm.get_run_list()
for i, (run_name, run_path) in enumerate(runs[:10], 1):
    info = rm.get_run_info(run_path)
    print(f"{i}. {info['scenario']} | {info['timestamp']} | {info['total_size_mb']} MB")
```

### 2. So Sánh Runs

```python
# So sánh 3 runs khác nhau
run1 = Path('./outputs/runs/run_20260411_143000_baseline')
run2 = Path('./outputs/runs/run_20260411_145200_conservative')
run3 = Path('./outputs/runs/run_20260411_150430_aggressive')

comparison = rm.compare_runs([run1, run2, run3])
print(comparison)

# Output:
# {
#     'baseline': {'timestamp': '20260411_143000', 'size_mb': 1.21, 'files_present': 10},
#     'conservative': {'timestamp': '20260411_145200', 'size_mb': 1.18, 'files_present': 10},
#     'aggressive': {'timestamp': '20260411_150430', 'size_mb': 1.22, 'files_present': 10}
# }
```

### 3. Truy Cập Run Mới Nhất

```python
import pandas as pd

# Đọc dataset_final.csv mới nhất
df_latest = pd.read_csv('./outputs/latest/dataset_final.csv')

# Đọc scaler model mới nhất
import pickle
with open('./outputs/latest/scaler_model.pkl', 'rb') as f:
    scaler = pickle.load(f)
```

---

## 🧪 Workflow Ví Dụ: Chạy 3 Scenarios

```bash
# Terminal 1: Chạy baseline
cd e:\WorldBank-Data-Analysis-Project\pipeline_execution
& .\.venv\bin\Activate.ps1
python run_pipeline.py baseline
# ✓ Tạo: run_20260411_143000_baseline/

# Terminal 2: Chạy conservative
python run_pipeline.py conservative
# ✓ Tạo: run_20260411_145200_conservative/

# Terminal 3: Chạy aggressive
python run_pipeline.py aggressive
# ✓ Tạo: run_20260411_150430_aggressive/

# Xem tất cả runs
python -c "from modules.run_manager import RunManager, print_run_list; rm = RunManager(); print_run_list(rm)"

# Output:
# ================================================================================
# RUN LIST (newest first)
# ================================================================================
# 
# 1. AGGRESSIVE
#    Timestamp: 20260411_150430
#    Size: 1.22 MB
#    Files: 10/10
#    Path: E:\...\outputs\runs\run_20260411_150430_aggressive
# 
# 2. CONSERVATIVE
#    Timestamp: 20260411_145200
#    Size: 1.18 MB
#    Files: 10/10
#    Path: E:\...\outputs\runs\run_20260411_145200_conservative
# 
# 3. BASELINE
#    Timestamp: 20260411_143000
#    Size: 1.21 MB
#    Files: 10/10
#    Path: E:\...\outputs\runs\run_20260411_143000_baseline
```

---

## 🛠️ Tích Hợp Với Jupyter Notebooks

Nếu dùng Jupyter notebooks, bạn cần cập nhật:

### 📓 `00_data_integration.ipynb`

Thêm cell này ở cuối:
```python
from pathlib import Path
from modules.run_manager import RunManager

# Lưu vào run directory nếu được cấp
run_dir = Path('./outputs/latest')  # Hoặc get từ argument
run_dir.mkdir(parents=True, exist_ok=True)

output_path = run_dir / 'dataset_merged.csv'
merged_df.to_csv(output_path, index=False, encoding='utf-8')
print(f"✓ Saved to: {output_path}")
```

### 📓 `01_auto_profiling.ipynb`

Thay `'./outputs'` bằng `'./outputs/latest'` (hoặc `run_dir`

### 📓 `02_execution_pipeline.ipynb`

Tương tự

---

## 📋 Cấu Hình Scenarios Ví Dụ

### baseline_config.yaml
```yaml
pipeline:
  name: 'WorldBank Data Processing Pipeline'
  version: '1.0'

phase1:
  log_transform:
    enabled: true      # Log transform cho columns skewed
    base: 10
    add_constant: 1.0
  
  outlier_detection:
    method: 'iqr'
    iqr_multiplier: 1.5
    action: 'clip'

phase2:
  scaling:
    method: 'standard'      # Z-score normalization
  
  imputation:
    method: 'knn'
    n_neighbors: 5
```

### conservative_config.yaml
```yaml
phase1:
  log_transform:
    enabled: true
  
  outlier_detection:
    method: 'iqr'
    iqr_multiplier: 2.0      # Nới lỏng hơn - ít loại outliers
    action: 'clip'

phase2:
  scaling:
    method: 'robust'         # Dùng percentiles, an toàn hơn
  
  imputation:
    method: 'knn'
    n_neighbors: 3           # Ít neighbors cho sparse data
```

### aggressive_config.yaml
```yaml
phase1:
  log_transform:
    enabled: true
  
  outlier_detection:
    method: 'isolation_forest'   # Advanced method
    isolation_forest_contamination: 0.05
    action: 'impute'             # Thay bằng NaN để KNN xử lý

phase2:
  scaling:
    method: 'standard'
  
  imputation:
    method: 'knn'
    n_neighbors: 7               # Nhiều neighbors
```

---

## ❓ FAQ

**Q: Sao có tất cả các outputs ở runs/ ? Thay vì chỉ dataset_final.csv?**  
A: Để dễ debug and reproduce. Nếu kết quả không đúng, bạn có diagnostic reports, config, metadata...

**Q: Folder latest/ là gì?**  
A: Copy của run mới nhất. Tiện khi bạn cần lúc luôn access kết quả mới nhất.

**Q: Có thể xóa runs cũ không?**  
A: Có! Chỉ cần xóa folder `outputs/runs/run_*` cũ. Nhưng nên lưu trữ ngay để khỏi mất.

**Q: Cách tạo scenario config mới?**  
A: Copy `config_template.yaml` thành `outputs/scenarios/YOUR_NAME_config.yaml`, edit, rồi chạy `python run_pipeline.py YOUR_NAME`.

**Q: Có thể chạy song song (parallel) không?**  
A: Có! Mở nhiều terminal chạy scenarios khác nhau - Mỗi cái có folder run riêng.

---

## 🗂️ Migration Từ Cấu Trúc Cũ

Nếu có file outputs cũ:

```bash
# Backup cũ
move outputs outputs_old

# Tạo cấu trúc mới
mkdir outputs
mkdir outputs/scenarios
mkdir outputs/runs

# Move file cũ vào run mới nếu muốn
mkdir outputs/runs/run_20260410_000000_old
move outputs_old/* outputs/runs/run_20260410_000000_old/
```

---

## 📝 Tóm Tắt

| Bước | Lệnh | Kết quả |
|------|------|---------|
| 1 | `python run_pipeline.py baseline` | `outputs/runs/run_*_baseline/` |
| 2 | `python run_pipeline.py conservative` | `outputs/runs/run_*_conservative/` |
| 3 | `python run_pipeline.py aggressive` | `outputs/runs/run_*_aggressive/` |
| 4 | Check `outputs/latest/` | Kết quả mới nhất |
| 5 | Compare | So sánh results từ 3 runs |

🎉 **Bây giờ bạn có thể chạy unlimited scenarios mà không mất data!**
