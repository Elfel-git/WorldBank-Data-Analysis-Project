# 📚 Pipeline Documentation Index

## 🚀 Start Here

### 1️⃣ **Để Chạy Pipeline Nhanh Nhất (5 phút)**
👉 Đọc: [QUICK_START.md](QUICK_START.md)
- Setup scenarios
- Chạy 3 scenarios khác nhau
- Xem kết quả

### 2️⃣ **Để Hiểu Cấu Trúc Mới**
👉 Đọc: [OUTPUTS_STRUCTURE.md](OUTPUTS_STRUCTURE.md)
- Giải thích kiến trúc mới
- Workflow ví dụ
- Tích hợp Jupyter

### 3️⃣ **Để Hiểu Gì Đã Thay Đổi**
👉 Đọc: [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)
- Vấn đề cũ và giải pháp mới
- Files mới/sửa
- Benefit summary

---

## 📂 File Reference

### 📖 Tài Liệu (Documentation)
| File | Mục Đích | Ai Nên Đọc |
|------|---------|-----------|
| [QUICK_START.md](QUICK_START.md) | 5 phút setup + chạy | Người mới/bận |
| [OUTPUTS_STRUCTURE.md](OUTPUTS_STRUCTURE.md) | Chi tiết cấu trúc | Người muốn hiểu sâu |
| [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md) | Thay đổi gì | Tech lead/review |
| [README.md](README.md) (cũ) | Tổng quan pipeline | Background reading |
| [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) (cũ) | Step-by-step cũ | Tham khảo |

### 🐍 Python Scripts
| File | Mục Đích | Usage |
|------|---------|-------|
| `run_pipeline.py` | Chạy pipeline | `python run_pipeline.py baseline` |
| `manage_runs.py` | Quản lý runs | `python manage_runs.py list` |
| `modules/run_manager.py` | Core manager class | Internal use |

### 📓 Jupyter Notebooks
| File | Mục Đích | Khi Nào Dùng |
|------|---------|-------------|
| `00_data_integration.ipynb` | PHASE 0: Merge CSVs | Interactive data exploration |
| `01_auto_profiling.ipynb` | PHASE 1: Analysis | Review diagnostics visually |
| `02_execution_pipeline.ipynb` | PHASE 2: Processing | Test configurations |

### ⚙️ Config & Setup
| File | Mục Đích |
|------|---------|
| `config_template.yaml` | Template cho các scenarios |
| `outputs/scenarios/*.yaml` | Scenario configs (bạn tạo) |
| `outputs/.gitignore` | Git ignore rules |

---

## 🎯 Scenarios Thường Dùng

### Scenario 1: "Tôi muốn chạy 1 lần nhanh nhất"
```bash
cd pipeline_execution
python run_pipeline.py baseline
```
⏱️ ~2 phút | 📖 Xem: [QUICK_START.md](QUICK_START.md#5-phút-quick-start)

### Scenario 2: "Tôi muốn so sánh 3 configs khác nhau"
```bash
python run_pipeline.py baseline
python run_pipeline.py conservative
python run_pipeline.py aggressive
python manage_runs.py compare
```
⏱️ ~10 phút | 📖 Xem: [OUTPUTS_STRUCTURE.md](OUTPUTS_STRUCTURE.md#🧪-workflow-ví-dụ-chạy-3-scenarios)

### Scenario 3: "Tôi muốn hiểu cách kết quả được lưu"
⏱️ ~15 phút | 📖 Xem: [OUTPUTS_STRUCTURE.md](OUTPUTS_STRUCTURE.md#📁-cấu-trúc-outputs-mới)

### Scenario 4: "Tôi muốn biết gì đã thay đổi"
⏱️ ~10 phút | 📖 Xem: [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)

### Scenario 5: "Tôi muốn sử dụng results trong code"
```python
import pandas as pd
df = pd.read_csv('./outputs/latest/dataset_final.csv')
```
📖 Xem: [OUTPUTS_STRUCTURE.md](OUTPUTS_STRUCTURE.md#🛠️-tích-hợp-với-jupyter-notebooks)

---

## 🔧 Manage_runs.py Commands

```bash
# Liệt kê tất cả runs
python manage_runs.py list

# So sánh runs (3 mới nhất)
python manage_runs.py compare

# Chi tiết về 1 run
python manage_runs.py info baseline

# Liệt kê scenarios
python manage_runs.py scenarios

# Latest run info
python manage_runs.py latest
```

📖 Full details: [manage_runs.py](manage_runs.py) or `python manage_runs.py help`

---

## 📊 Cấu Trúc Outputs Mới (At a Glance)

```
outputs/
├── scenarios/              # Các config files
│   ├── baseline_config.yaml
│   └── conservative_config.yaml
│
├── runs/                   # Kết quả từng lần chạy
│   ├── run_20260411_143000_baseline/
│   ├── run_20260411_145200_conservative/
│   └── ...
│
└── latest/                 # Copy run mới nhất
    ├── dataset_final.csv
    └── ...
```

📖 Chi tiết: [OUTPUTS_STRUCTURE.md](OUTPUTS_STRUCTURE.md#📁-cấu-trúc-outputs-mới)

---

## ❓ FAQ

**Q: Tôi không hiểu cấu trúc mới, nên đọc gì?**
A: [OUTPUTS_STRUCTURE.md](OUTPUTS_STRUCTURE.md) → Section "📁 Cấu Trúc Outputs Mới"

**Q: Tôi muốn chạy nhanh, nên đọc gì?**
A: [QUICK_START.md](QUICK_START.md) → Section "⚡ 5 Phút Quick Start"

**Q: Tôi muốn biết gì đã thay đổi so với version cũ?**
A: [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md) → Section "🔄 Files Được Sửa"

**Q: Tôi muốn so sánh kết quả từ 2 scenarios?**
A: [OUTPUTS_STRUCTURE.md](OUTPUTS_STRUCTURE.md) → Section "📊 Cách Quản Lý Runs" → "2. So Sánh Runs"

**Q: Tôi muốn access kết quả mới nhất trong Python code?**
A: [OUTPUTS_STRUCTURE.md](OUTPUTS_STRUCTURE.md) → Section "🛠️ Tích Hợp Với Jupyter Notebooks"

**Q: có lỗi gì không?**
A: Xem [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md) → Section "Backward Compatibility"

---

## 📈 Learning Path

### 👶 Beginner (5 phút)
1. [QUICK_START.md](QUICK_START.md) - Just run it!
2. `python manage_runs.py list` - See results

### 🚶 Intermediate (30 phút)
1. [OUTPUTS_STRUCTURE.md](OUTPUTS_STRUCTURE.md) - Understand structure
2. Create 3 scenario configs
3. `python run_pipeline.py baseline/conservative/aggressive`
4. `python manage_runs.py compare` - View comparison

### 🏃 Advanced (1 hour)
1. [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md) - Technical details
2. Review `run_manager.py` source code
3. Integrate with your own scripts
4. Automate scenario runs

---

## 🚀 Next Steps

- [ ] Read [QUICK_START.md](QUICK_START.md)
- [ ] Create scenario configs
- [ ] Run: `python run_pipeline.py baseline`
- [ ] Check: `outputs/runs/run_*/` or `outputs/latest/`
- [ ] Use: `outputs/latest/dataset_final.csv` for ML

---

## 📞 Support

- **Pipeline won't run?** → Check [QUICK_START.md#%EF%B8%8F-troubleshooting](QUICK_START.md#️-troubleshooting)
- **Can't find results?** → Check [OUTPUTS_STRUCTURE.md#📂-cấu-trúc-outputs-mới](OUTPUTS_STRUCTURE.md#📂-cấu-trúc-outputs-mới)
- **How to update code?** → See relevant `.ipynb` notebooks
- **Questions?** → Ask or check documentation again!

---

## 📚 All Documentation Files

```
pipeline_execution/
├── 📖 README.md                    (Old - tổng quan)
├── 📖 WORKFLOW_GUIDE.md            (Old - detailed guide)
├── 📖 QUICK_START.md               (NEW! - 5 min setup)
├── 📖 OUTPUTS_STRUCTURE.md         (NEW! - architecture)
├── 📖 CHANGES_SUMMARY.md           (NEW! - what changed)
├── 📖 INDEX.md                     (YOU ARE HERE)
├── 🐍 run_pipeline.py              (Updated)
├── 🐍 manage_runs.py               (NEW!)
└── modules/
    ├── run_manager.py              (NEW!)
    └── ... (others unchanged)
```

---

🎉 **Pick a document and start reading!**

Real quick? → [QUICK_START.md](QUICK_START.md)  
Want details? → [OUTPUTS_STRUCTURE.md](OUTPUTS_STRUCTURE.md)  
Technical? → [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)
