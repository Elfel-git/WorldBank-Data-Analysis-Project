# 🎨 Architecture Visualization

## Cũ vs Mới

### ❌ CẤU TRÚC CŨ (Vấn Đề)

```
First Run:                  Second Run (khác config):
outputs/                    outputs/
├── dataset_merged.csv ✓    ├── dataset_merged.csv ✗ (ghi đè)
├── dataset_final.csv ✓     ├── dataset_final.csv ✗ (ghi đè)
├── diagnostic_*.csv ✓      └── diagnostic_*.csv ✗ (ghi đè)
└── scaler_model.pkl ✓      
                            ❌ Kết quả lần 1 BỊ MẤT!
```

---

### ✅ CẤU TRÚC MỚI (Giải Pháp)

```
outputs/
│
├─ scenarios/               (Configurations)
│  ├─ baseline_config.yaml
│  ├─ conservative_config.yaml
│  └─ aggressive_config.yaml
│
├─ runs/                    (Results - Auto-created)
│  ├─ run_20260411_143000_baseline/
│  │  ├─ config.yaml        (Config for this run)
│  │  ├─ dataset_merged.csv
│  │  ├─ dataset_final.csv  ✓ SEPARATE COPY
│  │  ├─ diagnostic_*.csv
│  │  ├─ scaler_model.pkl
│  │  └─ run_summary.json
│  │
│  ├─ run_20260411_145200_conservative/
│  │  ├─ config.yaml
│  │  ├─ dataset_final.csv  ✓ SEPARATE COPY
│  │  └─ ... (10 files)
│  │
│  └─ run_20260411_150430_aggressive/
│     ├─ config.yaml
│     ├─ dataset_final.csv  ✓ SEPARATE COPY
│     └─ ... (10 files)
│
└─ latest/                 (Latest results - auto-copied)
   ├─ config.yaml          (Copy from newest run)
   ├─ dataset_final.csv    (Link/copy to newest)
   └─ ... (all files)

Benefits:
✅ Không mất data
✅ Dễ so sánh
✅ Config cùng results
✅ Lịch sử đầy đủ
✅ Quick access via 'latest'
```

---

## Pipeline Execution Flow

```
┌─────────────────────────────────────┐
│  User Command                        │
│  python run_pipeline.py baseline    │
└──────────────┬──────────────────────┘
               │
               │ RunManager.create_run_directory()
               │ ↓ Creates: run_20260411_143000_baseline/
               │
        ┌──────┴──────┐
        ▼             ▼
   ┌─────────────────────────────────────┐
   │ PHASE 0: Data Integration           │
   │ • Load CSVs from ../nam/            │
   │ • Merge into dataset_merged.csv     │
   │ • Save to: run_*/dataset_merged.csv │
   └──────────────┬──────────────────────┘
                  │
                  ▼
   ┌─────────────────────────────────────┐
   │ PHASE 1: Auto Profiling             │
   │ • Analyze data distributions        │
   │ • Detect outliers, missing values   │
   │ • Create visualizations             │
   │ • Auto-generate config              │
   │ • Save to: run_*/diagnostic_*.csv   │
   └──────────────┬──────────────────────┘
                  │
                  ▼
   ┌─────────────────────────────────────┐
   │ PHASE 2: Execution Pipeline         │
   │ • Log Transform (if enabled)        │
   │ • Handle Outliers                   │
   │ • Scale & Normalize                 │
   │ • KNN Imputation                    │
   │ • Save to: run_*/dataset_final.csv  │
   └──────────────┬──────────────────────┘
                  │
                  ▼
   ┌─────────────────────────────────────┐
   │ RunManager.update_latest()          │
   │ • Copy run_*/ → latest/             │
   └──────────────┬──────────────────────┘
                  │
                  ▼
   ┌─────────────────────────────────────┐
   │ ✅ COMPLETE                          │
   │ Results in:                         │
   │ • run_20260411_143000_baseline/     │
   │ • latest/                           │
   └─────────────────────────────────────┘
```

---

## Usage Flow - 3 Scenarios

```
Step 1: Setup (One-time)
┌──────────────────────────────────┐
│ mkdir outputs/scenarios          │
│ cp config_template.yaml *.yaml   │
│ [Edit 3 config files]            │
└──────────────────────────────────┘

Step 2: Run Scenario 1
┌──────────────────────────────┐
│ python run_pipeline.py       │
│ baseline                     │
│        ↓                     │
│ Creates:                    │
│ run_...baseline/**files     │
│ latest/**files              │
└──────────────────────────────┘

Step 3: Run Scenario 2 (Data lost? NO!)
┌──────────────────────────────┐
│ python run_pipeline.py       │
│ conservative                 │
│        ↓                     │
│ Creates NEW folder:         │
│ run_...conservative/**files │ ← original baseline still there!
│ latest/**files (updated)    │
└──────────────────────────────┘

Step 4: Run Scenario 3
┌──────────────────────────────┐
│ python run_pipeline.py       │
│ aggressive                   │
│        ↓                     │
│ Creates NEW folder:         │
│ run_...aggressive/**files   │ ← both previous runs intact!
│ latest/**files (updated)    │
└──────────────────────────────┘

Step 5: Compare All 3
┌──────────────────────────────┐
│ python manage_runs.py compare│
│        ↓                     │
│ ┌────────────────────────────┐
│ │ BASELINE    | 1.21 MB | ✓ │
│ │ CONSERVATIVE| 1.18 MB | ✓ │
│ │ AGGRESSIVE  | 1.22 MB | ✓ │
│ └────────────────────────────┘
└──────────────────────────────┘

✅ ALL 3 RUNS PRESERVED!
```

---

## File Organization Tree

```
Before (Data Loss):
outputs/
├── dataset_merged.csv      [Overwritten each run]
├── dataset_final.csv       [Overwritten each run]
├── diagnostic_report.csv   [Overwritten each run]
└── scaler_model.pkl        [Overwritten each run]

After (All Preserved):
outputs/
├── scenarios/
│  ├── baseline_config.yaml
│  ├── conservative_config.yaml  ← Easy to modify & rerun
│  └── aggressive_config.yaml
│
├── runs/
│  ├── run_20260411_143000_baseline/
│  │  ├── config.yaml            ← Original config saved
│  │  ├── dataset_merged.csv     ← Preserved
│  │  ├── dataset_final.csv      ← Preserved
│  │  ├── diagnostic_report.csv  ← Preserved
│  │  ├── diagnostic_report.json ← Preserved
│  │  ├── boxplots.png          ← Preserved
│  │  ├── histograms.png        ← Preserved
│  │  ├── scaler_model.pkl      ← Preserved
│  │  ├── processing_metadata.json
│  │  └── run_summary.json
│  │
│  ├── run_20260411_145200_conservative/  ← Run 2 results
│  │  └── (same 10 files) ...
│  │
│  └── run_20260411_150430_aggressive/    ← Run 3 results
│     └── (same 10 files) ...
│
└── latest/                              ← Always points to newest
   ├── config.yaml                       (copies from newest run)
   ├── dataset_final.csv
   ├── diagnostic_report.csv
   ├── scaler_model.pkl
   └── ... (all 10 files)
```

---

## Command Comparison

### Old Way
```bash
python run_pipeline.py   # Generic
# Run 1 → outputs/*.csv
# Run 2 → OVERWRITES outputs/*.csv   ❌ Lost run 1!
```

### New Way
```bash
python run_pipeline.py baseline
# Run 1 → outputs/runs/run_20260411_143000_baseline/
#      → outputs/latest/

python run_pipeline.py conservative
# Run 2 → outputs/runs/run_20260411_145200_conservative/  ✓ Run 1 still exists!
#      → outputs/latest/  (updated)

python run_pipeline.py aggressive
# Run 3 → outputs/runs/run_20260411_150430_aggressive/    ✓ All 3 exist!
#      → outputs/latest/  (updated)

# All preserved + easily comparable!
python manage_runs.py compare
# Shows all 3 side-by-side ✓
```

---

## Data Access Patterns

```
Pattern 1: Always Use Latest
import pandas as pd
df = pd.read_csv('./outputs/latest/dataset_final.csv')  ✓ Always newest


Pattern 2: Access Specific Run
df_baseline = pd.read_csv('./outputs/runs/run_20260411_143000_baseline/dataset_final.csv')
df_conservative = pd.read_csv('./outputs/runs/run_20260411_145200_conservative/dataset_final.csv')
print("Comparison:", df_baseline.shape, "vs", df_conservative.shape)  ✓ Easy compare


Pattern 3: Loop Through All Runs
from pathlib import Path
for run_dir in sorted(Path('outputs/runs').glob('run_*')):
    df = pd.read_csv(run_dir / 'dataset_final.csv')
    print(f"{run_dir.name}: {df.shape}")  ✓ Process all runs
```

---

## Integration Points

```
Jupyter Notebooks (Old):
00_data_integration.ipynb
  └─ Save to: outputs/dataset_merged.csv

01_auto_profiling.ipynb
  └─ Read from: outputs/dataset_merged.csv
  └─ Save to: outputs/diagnostic_*.csv

02_execution_pipeline.ipynb
  └─ Read from: outputs/dataset_merged.csv
  └─ Save to: outputs/dataset_final.csv

Jupyter Notebooks (New):
Same notebooks can work with:
  └─ ./outputs/latest/  (always newest)
  └─ Or specific run_dir if passed as parameter
```

---

## Timeline Visualization

```
Time ──►

Run 1 (baseline)
├─ 14:30 | Phase 0,1,2
├─ 14:35 | ✓ Complete
├─ Path: run_20260411_143000_baseline/
└─ latest/ ← copies here

Run 2 (conservative)
├─ 14:52 | Phase 0,1,2
├─ 14:57 | ✓ Complete
├─ Path: run_20260411_145200_conservative/
└─ latest/ ← updates here (run1 still exists!)

Run 3 (aggressive)
├─ 15:04 | Phase 0,1,2
├─ 15:09 | ✓ Complete
├─ Path: run_20260411_150430_aggressive/
└─ latest/ ← updates here (run1,2 still exist!)

All 3 runs preserved forever!
Easy to compare:
python manage_runs.py compare
```

---

## Summary Diagram

```
                     ┌─────────────────────────────┐
                     │   User Runs Pipeline        │
                     │  (3 different scenarios)    │
                     └────────────┬────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
              Run Baseline   Run Cons.    Run Aggr.
              
                    │             │             │
        ┌───────────┼─────────────┼─────────────┤
        │           │             │             │
        ▼           ▼             ▼             ▼
    [PHASE 0]   [PHASE 0]    [PHASE 0]    → datasets_merged
        │           │             │
    [PHASE 1]   [PHASE 1]    [PHASE 1]    → diagnostic reports
        │           │             │
    [PHASE 2]   [PHASE 2]    [PHASE 2]    → datasets_final
        │           │             │
        └─────┬─────┴─────┬───────┘
              │           │ 
        Save RUN 1    Save RUN 2    Save RUN 3
        in folder    in folder    in folder
              │
              ▼
        Copy Latest (Run 3)
        
Results Structure:
        run_1/  ✓ Preserved
        run_2/  ✓ Preserved  
        run_3/  ✓ Preserved
        latest/ ← Points to run_3

All accessible:
✅ outputs/runs/run_*/dataset_final.csv
✅ outputs/latest/dataset_final.csv
✅ python manage_runs.py compare
```

---

## Before & After Comparison Chart

| Aspect | Before ❌ | After ✅ |
|--------|----------|---------|
| **Run 1** | Save | Save in `run_*/` |
| **Run 2** | Overwrites Run1 data | Saves in NEW `run_*/` |
| **Run 3** | Overwrites Run1,2 data | Saves in NEW `run_*/` |
| **Preserve past?** | NO ❌ | YES ✅ |
| **Compare Results?** | NO ❌ | YES ✅ |
| **Know which config?** | NO ❌ | YES ✅ (saved) |
| **Latest?** | Only Run 3 | `latest/` folder |
| **History?** | NO ❌ | Full ✅ |
| **Size overhead** | Minimal | ~3x (3 runs kept) |

---

🎨 **Visual Guide Complete!**
Choose your preferred documentation style above.
