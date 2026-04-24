# 🌍 Vietnam GDP Growth Analysis - Data Pipeline

**Project Goal**: Dự báo tăng trưởng GDP của Việt Nam 2024 bằng cách so sánh với các nền kinh tế tương đồng

---

## 📋 Mục Lục

1. [Quick Start](#quick-start) - 5 phút setup
2. [Project Structure](#project-structure) - Cấu trúc dự án
3. [Pipeline Overview](#pipeline-overview) - 3 Phase chính
4. [Datasets](#datasets) - Dữ liệu sử dụng
5. [Installation](#installation) - Chi tiết cài đặt
6. [Usage](#usage) - Cách chạy
7. [Output Files](#output-files) - File đầu ra
8. [Documentation](#documentation) - Tài liệu

---

## 🚀 Quick Start

```bash
# 1. Tạo environment (lần đầu)
conda env create -f environment.yml -y

# 2. Activate
conda activate worldbank-analysis

# 3. Chạy pipeline
python run_full_pipeline.py default

# 4. Xem kết quả
# Output: pipeline_execution/outputs/latest/dataset_final.csv
```

**⏱️ Time**: 5 phút setup + 1 phút chạy

---

## 📁 Project Structure

```
WorldBank-Data-Analysis-Project/
│
├── 📄 README.md                          (This file)
├── 📄 QUICK_START.md                     🔥 Start here!
├── 📄 CONDA_SETUP_GUIDE.md               Hướng dẫn Conda
├── 📄 REFACTORING_SUMMARY.md             Thay đổi refactor
├── 📄 requirements.txt                   Python packages
├── 📄 environment.yml                    Conda environment
├── 📄 run_full_pipeline.py               Master script 🎯
│
├── 📁 nam/                               Data source
│   ├── Access to electricity.csv
│   ├── GDP per capita.csv
│   ├── Individuals using Internet.csv
│   └── ... (9 indicators total)
│
├── 📁 pipeline_execution/
│   ├── 📄 run_pipeline.py                Phase orchestration
│   ├── 📄 README.md                      Pipeline details
│   ├── 📄 test_integration.py            Tests
│   │
│   ├── 📁 modules/
│   │   ├── data_integration.py           Phase 0: Merge data
│   │   ├── diagnostics.py                Phase 1: Profile & analyze
│   │   ├── processing.py                 Phase 2: Clean & prepare
│   │   ├── run_manager.py                Folder management
│   │   ├── config_handler.py             Config management
│   │   ├── logger_setup.py               Logging
│   │   └── __init__.py
│   │
│   ├── 📁 outputs/
│   │   ├── 📁 runs/
│   │   │   └── run_20260413_230212_default/  Each pipeline run
│   │   │       ├── dataset_merged.csv
│   │   │       ├── diagnostic_report.csv
│   │   │       ├── dataset_final.csv
│   │   │       ├── boxplots.png
│   │   │       ├── histograms.png
│   │   │       └── logs/
│   │   │
│   │   └── 📁 latest/                    Latest run copy
│   │       └── (Same files as above)
│   │
│   └── 📁 notebooks/
│       ├── 00_data_integration.ipynb
│       ├── 01_auto_profiling.ipynb
│       └── 02_execution_pipeline.ipynb
│
└── 📁 .git/                              Version control
```

---

## 🔄 Pipeline Overview

### PHASE 0: Data Integration

```
Input: nam/*.csv (9 indicators)
  ↓
Load 9 World Bank indicators
Standardize structure
Merge into single dataset
  ↓
Output: dataset_merged.csv (5546 rows × 11 columns)
```

**Indicators**:

1. Access to electricity (% of population)
2. Agriculture value added (% of GDP)
3. Domestic credit to private sector (% of GDP)
4. Employment in services (% of total employment)
5. Foreign direct investment, net inflows (% of GDP)
6. GDP per capita (constant 2015 US$)
7. Individuals using the Internet (% of population)
8. Industry value added (% of GDP)
9. Services value added (% of GDP)

---

Input: dataset_merged.csv
  ↓
Analyze missing values
Analyze distributions (mean, median, skewness, kurtosis)
Detect outliers (IQR/Z-score method)
Create univariate visualizations (boxplots, histograms)
Create multivariate visualizations (correlation heatmap, pairwise scatter)
Generate diagnostic report
  ↓
Output:
  - diagnostic_report.csv (Statistical summary)
  - boxplots.png (Outlier visualization)
  - histograms.png (Frequency distribution)
  - correlation_heatmap.png (Multicollinearity check)
  - pairwise_scatter.png (Non-linear relationship check)
  - config.yaml (Recommended preprocessing parameters)

---

Input: dataset_merged.csv + config.yaml
  ↓
1. Log Transform        (For highly skewed distributions)
2. Outlier Handling     (Clip method via IQR)
3. Scaling              (MinMaxScaler - Strictly no negative values)
4. Imputation           (KNN, k=5)
5. L1-Normalization     (Convert features to probability distributions: sum = 1.0)
6. Verify & Visualize   (KDE Before/After, 100% Stacked Bar)
  ↓
Output: 
  - dataset_final.csv (Clean, probability-distributed data ready for KL Divergence)
  - scaler_model.pkl (Saved scaling weights)
  - processing_metadata.json (Transformation logs)
  - kde_before_after_transform.png (Proof of normalization)
  - probability_stacked_bars.png (Proof of economic structure representation)
  
---

## 📊 Datasets

### Data Source

**World Bank Open Data**

- Coverage: 265 countries
- Time Period: 2004-2024 (21 years)
- Last Updated: Automatically from World Bank

### Current Data Snapshot (Latest Run)

```
Total Records:      5546 (countries × years)
Indicators:         9
Missing Values:     8.23% (before imputation)
After Processing:   0% missing values
Countries:          265
Years:              2004-2024
```

### Data Quality

- ✅ 90%+ complete for 2010-2021 (golden period)
- ✅ ~85% complete for 2022-2023 (recovery period)
- ⚠️ Emerging 2024 data (preliminary)

---

## 💾 Installation

### Requirements

- **Python**: 3.9, 3.10, 3.11, or 3.12
- **OS**: Windows, macOS, Linux
- **Disk Space**: ~500MB (for dependencies)

### Option 1: Conda (Recommended)

```bash
# Tạo environment
conda env create -f environment.yml -y

# Activate
conda activate worldbank-analysis

# Verify
python -c "import pandas, sklearn; print('✓ OK')"
```

### Option 2: Virtual Environment (venv)

```bash
# Create venv
python -m venv .venv

# Activate
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Option 3: Manual Install

```bash
pip install pandas numpy scikit-learn matplotlib seaborn pyyaml jupyter
```

---

## 🎯 Usage

### Run from Project Root

```bash
# Activate environment
conda activate worldbank-analysis

# Run with default scenario
python run_full_pipeline.py default

# Run with different scenario
python run_full_pipeline.py baseline
python run_full_pipeline.py conservative
```

### Or from pipeline_execution folder

```bash
cd pipeline_execution
python run_pipeline.py default
```

### With Python script

```python
import sys
from pathlib import Path

# Add pipeline to path
sys.path.insert(0, 'pipeline_execution')
from run_pipeline import main

# Run pipeline
success = main(scenario_name='default')
```

---

## 📤 Output Files

### Location

```
pipeline_execution/outputs/latest/        (Latest run - recommended)
pipeline_execution/outputs/runs/          (All historical runs)
```

### Key Files

| File                         | Size   | Purpose                         | Format |
| ---------------------------- | ------ | ------------------------------- | ------ |
| **dataset_final.csv**        | ~1MB   | Cleaned, normalized data for ML | CSV    |
| **diagnostic_report.csv**    | ~2KB   | Statistical summary             | CSV    |
| **boxplots.png**             | ~97KB  | Distribution visualization      | PNG    |
| **histograms.png**           | ~100KB | Frequency distribution          | PNG    |
| **config.yaml**              | ~1KB   | Preprocessing configuration     | YAML   |
| **scaler_model.pkl**         | ~3KB   | StandardScaler model            | Binary |
| **processing_metadata.json** | ~5KB   | Transformation details          | JSON   |
| **run_summary.json**         | ~1KB   | Run metadata                    | JSON   |

### Recommended for Use

- **For ML Models**: `dataset_final.csv`
- **For Data Quality**: `diagnostic_report.csv`
- **For Visualization**: `boxplots.png`, `histograms.png`

---

## 📚 Documentation

### Quick References

- 🔥 [QUICK_START.md](QUICK_START.md) - 5-minute setup
- 🔧 [CONDA_SETUP_GUIDE.md](CONDA_SETUP_GUIDE.md) - Detailed conda setup
- 📝 [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) - Recent changes
- 📖 [pipeline_execution/README.md](pipeline_execution/README.md) - Pipeline details

### Jupyter Notebooks

```bash
# Start Jupyter
jupyter notebook

# Open notebooks
pipeline_execution/notebooks/00_data_integration.ipynb
pipeline_execution/notebooks/01_auto_profiling.ipynb
pipeline_execution/notebooks/02_execution_pipeline.ipynb
```

---

## 🧪 Testing

### Run Tests

```bash
cd pipeline_execution
python test_integration.py
```

### Verify Pipeline

```bash
# Check if pipeline runs without errors
python run_full_pipeline.py default

# Check output files
ls pipeline_execution/outputs/latest/
```

---

## 🔍 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'pandas'`

```bash
# Solution: Activate environment
conda activate worldbank-analysis
# Or reinstall
pip install -r requirements.txt
```

**Issue**: `FileNotFoundError: nam/ folder not found`

```bash
# Solution: Check data folder exists
ls nam/
# Should have 9 CSV files
```

**Issue**: `conda: command not found`

```bash
# Solution: Install Miniconda
# https://docs.conda.io/projects/miniconda/en/latest/
```

**Issue**: Plot rendering errors

```bash
# Solution: Update matplotlib
pip install --upgrade matplotlib
```

---

## 📊 Performance

### Typical Run Times

```
Phase 0 (Integration):        5-10 seconds
Phase 1 (Diagnostics):        10-15 seconds
Phase 2 (Processing):         20-30 seconds
Total:                        35-55 seconds
```

### Memory Usage

- Peak RAM: ~200MB
- Disk Output: ~2MB per run

---

## 🎯 Project Goals & Status

### Main Objective

**Chứng minh được bộ dữ liệu đủ để thực hiện bài toán dự báo GDP của Việt Nam 2024**

### Evidence of Data Sufficiency

✅ **Định Lượng (Quantitative)**:

- 9 indicators → 5,546 data points
- 265 countries → Rich peer comparison
- 21 years → Temporal patterns captured
- 8.23% missing → Manageable with imputation
- 0% missing after processing → Clean dataset

✅ **Định Tính (Qualitative)**:

- Data quality: Good for 2004-2023, emerging for 2024
- Indicator diversity: Economic, social, structural
- Temporal coverage: Pre-crisis (2008), pandemic (2020), recovery (2022+)
- Peer countries: Full range from low to high income countries

### Status: ✅ COMPLETE

---

## 📞 Support & Documentation

- 📖 Check [QUICK_START.md](QUICK_START.md) first
- 🔍 Review [CONDA_SETUP_GUIDE.md](CONDA_SETUP_GUIDE.md) for setup
- 📝 Read [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) for recent changes
- 📚 See [pipeline_execution/README.md](pipeline_execution/README.md) for technical details

---

## 📄 License & Attribution

**Data Source**: World Bank Open Data  
**Project**: Vietnam GDP Growth Analysis  
**Version**: 1.0 (Refactored 2026-04-13)

---

**Last Updated**: 2026-04-13  
**Status**: ✅ Production Ready
