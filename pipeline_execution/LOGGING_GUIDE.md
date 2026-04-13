# Pipeline Logging Guide

## Overview

Thêm từ phiên bản mới, pipeline tự động lưu toàn bộ logs vào các file riêng biệt cho từng module.

## Log File Structure

Khi chạy pipeline, logs được tổ chức như sau:

```
outputs/
├── runs/
│   └── run_20260412_143000_baseline/
│       ├── logs/
│       │   ├── pipeline.log          # Main pipeline logs
│       │   ├── data_integration.log  # PHASE 0 logs
│       │   ├── diagnostics.log       # PHASE 1 logs
│       │   └── processing.log        # PHASE 2 logs
│       ├── dataset_merged.csv
│       ├── dataset_final.csv
│       ├── diagnostic_report.csv
│       ├── diagnostic_report.json
│       ├── boxplots.png
│       ├── histograms.png
│       ├── config.yaml
│       ├── scaler_model.pkl
│       └── processing_metadata.json
│
└── latest/                   # Symlink/copy của run mới nhất
    └── logs/
        ├── pipeline.log
        ├── data_integration.log
        ├── diagnostics.log
        └── processing.log
```

## Log Files Details

### 1. `pipeline.log` (Main Pipeline)
- **Mục đích:** Logs chung của toàn bộ pipeline execution
- **Nội dung:**
  - Pipeline start/complete messages
  - Phase completion status
  - Overall statistics
  - Summary of all runs

### 2. `data_integration.log` (PHASE 0)
- **Mục đích:** Logs chi tiết từ quá trình tích hợp dữ liệu
- **Nội dung:**
  - CSV files loaded
  - Data structure standardization
  - Merging process
  - Final shape and data info

### 3. `diagnostics.log` (PHASE 1)
- **Mục đích:** Logs từ quá trình phân tích chẩn đoán
- **Nội dung:**
  - Missing value analysis
  - Distribution analysis
  - Outlier detection results
  - Visualization creation
  - Recommendation generation

### 4. `processing.log` (PHASE 2)
- **Mục đích:** Logs từ quá trình xử lý dữ liệu
- **Nội dung:**
  - Log transform steps
  - Outlier handling details
  - Scaling & normalization process
  - KNN imputation results
  - Final dataset statistics

## How to Use Logs

### View Logs During Execution
```bash
# Tail main pipeline log in real-time
tail -f outputs/runs/run_TIMESTAMP_SCENARIO/logs/pipeline.log

# Tail specific module log
tail -f outputs/runs/run_TIMESTAMP_SCENARIO/logs/data_integration.log
```

### View Latest Run Logs
```bash
# View logs from latest run
tail -f outputs/latest/logs/pipeline.log
```

### Search for Errors
```bash
# Find all ERROR level logs
grep "ERROR" outputs/runs/run_TIMESTAMP_SCENARIO/logs/*.log

# Find specific errors in processing
grep "ERROR" outputs/runs/run_TIMESTAMP_SCENARIO/logs/processing.log
```

### Analyze Processing Steps
```bash
# Check all transformation steps
grep "Step" outputs/runs/run_TIMESTAMP_SCENARIO/logs/processing.log

# Check memory usage during execution
grep "Shape\|Size\|Missing" outputs/runs/run_TIMESTAMP_SCENARIO/logs/*.log
```

## Log Levels

Logs sử dụng Python logging với các levels:
- **DEBUG:** Chi tiết cho debugging (currently disabled, có thể enable)
- **INFO:** Thông tin chung (mặc định)
- **WARNING:** Cảnh báo, e.g., rows removed for outliers  
- **ERROR:** Lỗi hoặc vấn đề
- **CRITICAL:** Lỗi nghiêm trọng

## Log Format

Tất cả logs sử dụng format thống nhất:
```
2026-04-12 14:30:00,123 - module_name - INFO - Message content
2026-04-12 14:30:01,456 - processing - WARNING - Removing 5 rows with outliers in 'GDP'
```

## Troubleshooting with Logs

### Pipeline không hoàn thành
```bash
# Check main pipeline log
tail -20 outputs/latest/logs/pipeline.log

# Check which phase failed
grep "PHASE\|Complete\|ERROR" outputs/latest/logs/pipeline.log
```

### Data mismatch between phases
```bash
# Compare shapes
grep "Shape:" outputs/latest/logs/*.log

# Check values during processing
grep "Missing\|Outlier\|Found" outputs/latest/logs/processing.log
```

### Performance tracking
```bash
# Check how long each phase took
grep "PHASE.*COMPLETE" outputs/latest/logs/pipeline.log
```

## Notes

- Logs tự động được tạo và lưu mỗi khi chạy pipeline
- Mỗi run có riêng folder logs (không bị ghi đè)
- Folder `outputs/latest/` luôn chứa logs từ run mới nhất
- Log files là plain text, có thể mở bằng bất kỳ text editor nào
- Tổng size logs thường < 10 MB cho mỗi run đầy đủ
