# WorldBank Data Processing Pipeline

## Complete Multi-Phase Data Integration & Processing Workflow

---

## 📋 Table of Contents

1. [Pipeline Overview](#pipeline-overview)
2. [Getting Started](#getting-started)
3. [Folder Structure](#folder-structure)
4. [Phase-by-Phase Guide](#phase-by-phase-guide)
5. [Configuration Guide](#configuration-guide)
6. [Output Files](#output-files)
7. [Troubleshooting](#troubleshooting)

---

## Pipeline Overview

This pipeline implements a complete data processing workflow with 4 phases:

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 0: DATA INTEGRATION                                        │
│ Merge all CSV indicators → dataset_merged.csv                     │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: AUTO PROFILING & DIAGNOSTICS                           │
│ Analyze distributions, detect outliers, create reports           │
│ Output: diagnostic_report, boxplots, histograms                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1.5: HUMAN REVIEW & CONFIG (MANUAL)                       │
│ Review diagnostics & edit draft_config.yaml → final_config.yaml │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 2: EXECUTION PIPELINE                                      │
│ Apply config: Log Transform → Outlier Handling → Scaling         │
│ → Imputation → dataset_final.csv + scaler_model.pkl              │
└─────────────────────────────────────────────────────────────────┘
```

**Key Features:**

- ✅ Fully automated data integration
- ✅ Comprehensive diagnostics & profiling
- ✅ Human-in-the-loop configuration review
- ✅ Robust data preprocessing pipeline
- ✅ Exportable scaler for future transformations

---

## Getting Started

### Prerequisites

```
Python 3.8+
pandas, numpy, scikit-learn, matplotlib, seaborn, pyyaml
```

### Installation

```bash
# Install required packages
pip install pandas numpy scikit-learn matplotlib seaborn pyyaml

# Or use conda
conda install pandas numpy scikit-learn matplotlib seaborn pyyaml
```

### Quick Start

1. **Verify input data:** Check that CSV files are in the `../nam` folder
2. **Run PHASE 0:** Open and run `00_data_integration.ipynb`
3. **Run PHASE 1:** Open and run `01_auto_profiling.ipynb`
4. **Review & Edit:** Edit `outputs/draft_config.yaml` → save as `outputs/final_config.yaml`
5. **Run PHASE 2:** Open and run `02_execution_pipeline.ipynb`

### Run With CLI (Separated Phases)

```bash
# Run full pipeline (same behavior as before)
python run_pipeline.py full --scenario default

# Backward-compatible full run
python run_pipeline.py default

# Phase 0 only: integration + diagnostics + draft YAML
python run_pipeline.py phase0 --scenario default

# Phase 1 only: read YAML + preprocess merged dataset
python run_pipeline.py phase1 --scenario default --config ./outputs/latest/config.yaml --input ./outputs/latest/dataset_merged.csv

# Phase 1 with auto-detected input/config (if available in default paths)
python run_pipeline.py phase1 --scenario default
```

---

## Folder Structure

```
pipeline_execution/
├── 00_data_integration.ipynb      # PHASE 0: Merge CSVs
├── 01_auto_profiling.ipynb        # PHASE 1: Auto profiling & diagnostics
├── 02_execution_pipeline.ipynb    # PHASE 2: Data processing
│
├── config_template.yaml           # Configuration template (reference)
├── modules/
│   ├── __init__.py
│   ├── config_handler.py          # Configuration management
│   ├── data_integration.py        # Phase 0: Data merging
│   ├── diagnostics.py             # Phase 1: Profiling & analysis
│   └── processing.py              # Phase 2: Data processing
│
├── outputs/                       # Generated files (auto-created)
│   ├── dataset_merged.csv         # Phase 0 output
│   ├── diagnostic_report.csv      # Phase 1 statistics
│   ├── diagnostic_report.json     # Phase 1 detailed report
│   ├── boxplots.png               # Phase 1 visualization
│   ├── histograms.png             # Phase 1 visualization
│   ├── draft_config.yaml          # Phase 1 auto-generated config
│   ├── final_config.yaml          # Phase 1.5 reviewed config
│   ├── dataset_final.csv          # Phase 2 final output
│   ├── scaler_model.pkl           # Phase 2 scaler model
│   └── processing_metadata.json   # Phase 2 metadata
│
└── README.md                      # This file

# Input data location (must exist)
../nam/
├── Access to electricity (% of population).csv
├── Agriculture, forestry, and fishing, value added (% of GDP).csv
├── ... (other indicator CSVs)
```

---

## Phase-by-Phase Guide

### PHASE 0: Data Integration

**File:** `00_data_integration.ipynb`

**What it does:**

- Loads all CSV files from `../nam` folder
- Merges them based on Country and Year
- Standardizes structure: Countries (rows), Years (columns)
- Outputs: `dataset_merged.csv`

**How to run:**

```
1. Open 00_data_integration.ipynb
2. Run all cells (Shift+Enter)
3. Check output/dataset_merged.csv is created
```

**Expected output:**

- Shape: (countries × years, indicators)
- All indicators as columns
- Missing values marked as NaN

**Typical issues & solutions:**
| Issue | Solution |
|-------|----------|
| CSV not found | Verify CSV files in `../nam/` |
| Memory error | Check available RAM (reduce dataset size if needed) |
| Shape mismatch | Ensure all CSVs have Country names in rows |

---

### PHASE 1: Auto Profiling & Diagnostics

**File:** `01_auto_profiling.ipynb`

**What it does:**

- Analyzes data distributions for each column
- Detects missing values
- Identifies outliers (IQR method by default)
- Creates visualizations: boxplots, histograms
- Generates diagnostic report in CSV & JSON formats
- **Auto-generates draft configuration** (draft_config.yaml)

**How to run:**

```
1. Ensure PHASE 0 is complete (dataset_merged.csv exists)
2. Open 01_auto_profiling.ipynb
3. Run all cells
4. Review diagnostic reports and visualizations
```

**Generated files:**

- `diagnostic_report.csv` - Statistics table (Mean, Median, Std, Skewness, ...)
- `diagnostic_report.json` - Detailed results in JSON format
- `boxplots.png` - Boxplots for all columns (outlier detection)
- `histograms.png` - Histograms for all columns (distribution analysis)
- `draft_config.yaml` - Auto-generated configuration (**_ MUST REVIEW _**)

**Key metrics explained:**

- **Missing %:** Percentage of NaN values (>50% = problematic)
- **Skewness:** Distribution symmetry (-1 to 1 = moderate, >2 = highly skewed)
- **Outlier count:** Physical outliers detected by IQR method
- **Kurtosis:** Tail heaviness (>3 = heavy tails, unusual events)

---

### PHASE 1.5: Human Review & Configuration

**⚠️ CRITICAL STEP - Manual work required**

**What to do:**

1. **Review diagnostic reports:**
   - Open `outputs/diagnostic_report.json` in a text editor
   - Check which columns have high missing % or skewness
2. **Review visualizations:**
   - Open `outputs/boxplots.png` - Look for extreme outliers
   - Open `outputs/histograms.png` - Check distribution shapes

3. **Edit configuration:**
   - Open `outputs/draft_config.yaml`
   - Adjust parameters based on findings:
     - **log_transform:** Enable for highly skewed data (skewness > 2)
     - **outlier_detection:** Choose action (clip/remove/impute)
     - **scaling:** Choose method (standard/minmax/robust)
     - **imputation:** Adjust n_neighbors based on data sparsity

4. **Save configuration:**
   - Save edited file as `outputs/final_config.yaml`
   - DO NOT modify draft_config.yaml

**Configuration recommendations:**

**Scenario 1: Data is already well-distributed**

```yaml
log_transform: { enabled: false }
outlier_detection: { method: iqr, iqr_multiplier: 2.0, action: clip }
scaling: { method: standard }
imputation: { n_neighbors: 5 }
```

**Scenario 2: Highly skewed data (TYPICAL)**

```yaml
log_transform: { enabled: true, add_constant: 1.0 }
outlier_detection: { method: iqr, iqr_multiplier: 1.5, action: clip }
scaling: { method: standard }
imputation: { n_neighbors: 5 }
```

**Scenario 3: Very noisy data with many outliers**

```yaml
log_transform: { enabled: true }
outlier_detection: { method: isolation_forest, action: impute }
scaling: { method: robust }
imputation: { n_neighbors: 3 }
```

---

### PHASE 2: Execution Pipeline

**File:** `02_execution_pipeline.ipynb`

**What it does:**

1. Loads merged data
2. Loads configuration from `final_config.yaml`
3. Applies transformations in sequence:
   - **Step 1:** Log transform (if enabled)
   - **Step 2:** Outlier handling (IQR/Isolation Forest)
   - **Step 3:** Scaling/Normalization
   - **Step 4:** KNN Imputation
4. Exports final dataset and scaler model

**How to run:**

```
1. Ensure PHASE 1.5 is complete (final_config.yaml exists)
2. Open 02_execution_pipeline.ipynb
3. Run all cells
4. Check outputs/dataset_final.csv
```

**Generated files:**

- `dataset_final.csv` - Final processed dataset (ready for ML)
- `scaler_model.pkl` - Scikit-learn StandardScaler object
- `processing_metadata.json` - Record of all transformations applied

**Key outputs explained:**

- **dataset_final.csv:** Rows = (countries × years), Columns = scaled indicators
  - All numeric columns are normalized (mean ≈ 0, std ≈ 1 for standard scaler)
  - No missing values (imputed with KNN)
  - Ready for machine learning

- **scaler_model.pkl:** Saved scaler object for applying same transformation to new data
  - Use with: `sklearn.externals.joblib.load()` or `pickle.load()`
  - Apply to new data: `scaler.transform(new_data)`

---

## Configuration Guide

### Config File Format (YAML)

**Top-level sections:**

```yaml
pipeline: # Project metadata
phase1: # Diagnostics settings (auto-generated)
phase2: # Processing pipeline settings
diagnostics: # Analysis parameters
```

**PHASE 1: Log Transform**

```yaml
log_transform:
  enabled: true/false # Enable log transformation
  features: null # null = auto-detect; or list specific features
  base: 10 # Log base (10 or e)
  add_constant: 1.0 # Prevents log(0)
```

**PHASE 1: Outlier Detection**

```yaml
outlier_detection:
  method: "iqr" # iqr, zscore, isolation_forest
  iqr_multiplier: 1.5 # Higher = fewer outliers (1.8, 2.0)
  zscore_threshold: 3.0 # Std devs from mean
  action: "clip" # clip, remove, impute
```

**PHASE 2: Scaling**

```yaml
scaling:
  method: "standard" # standard (z-score), minmax, robust
  features: null # null = all numeric columns
```

**PHASE 2: Imputation**

```yaml
imputation:
  method: "knn" # knn, mean, forward_fill
  n_neighbors: 5 # Reduce to 3-5 for sparse data
  weight_type: "distance"
```

---

## Output Files

### Phase 0 Outputs

| File                 | Type | Description                        |
| -------------------- | ---- | ---------------------------------- |
| `dataset_merged.csv` | CSV  | Merged dataset with all indicators |

### Phase 1 Outputs

| File                     | Type | Description                                   |
| ------------------------ | ---- | --------------------------------------------- |
| `diagnostic_report.csv`  | CSV  | Summary statistics table                      |
| `diagnostic_report.json` | JSON | Detailed diagnostic results                   |
| `boxplots.png`           | PNG  | Boxplot visualizations (~500KB)               |
| `histograms.png`         | PNG  | Histogram visualizations (~500KB)             |
| `draft_config.yaml`      | YAML | Auto-generated configuration (⚠️ must review) |

### Phase 1.5 Outputs

| File                | Type | Description                                     |
| ------------------- | ---- | ----------------------------------------------- |
| `final_config.yaml` | YAML | Human-reviewed configuration (created manually) |

### Phase 2 Outputs

| File                       | Type | Description                            |
| -------------------------- | ---- | -------------------------------------- |
| `dataset_final.csv`        | CSV  | Final processed dataset (ready for ML) |
| `scaler_model.pkl`         | PKL  | Scikit-learn scaler object (~1KB)      |
| `processing_metadata.json` | JSON | Record of transformations applied      |

---

## Troubleshooting

### Issue: "Module not found" error

**Solution:**

```python
# Ensure modules folder is in Python path
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / 'modules'))
```

### Issue: "FileNotFoundError: dataset_merged.csv"

**Solution:**

- Run PHASE 0 first (00_data_integration.ipynb)
- Verify CSV files exist in `../nam/` folder

### Issue: Memory error when running pipeline

**Solution:**

- Reduce dataset size (filter by years/countries)
- Process in chunks instead of all at once
- Check available RAM: `import psutil; psutil.virtual_memory()`

### Issue: "KeyError" in config loading

**Solution:**

- Verify final_config.yaml has correct YAML formatting
- Use online YAML validator: https://www.yamllint.com/
- Check indentation (use spaces, not tabs)

### Issue: Very different results after Phase 2

**Solution:**

- Check draft_config.yaml recommendations
- Log transform can cause significant shifts (expected)
- Standard scaler centers at 0 (expected)
- Review processing_metadata.json to see which transforms were applied

### Issue: "Cannot read final_config.yaml"

**Solution:**

- If final_config.yaml doesn't exist, Phase 2 automatically uses draft_config.yaml
- Ensure at least draft_config.yaml exists (created by Phase 1)
- To avoid auto-generation, explicitly create final_config.yaml

### Finding Logs from Previous Runs

**Solution:**

- All logs are automatically saved in `outputs/runs/run_TIMESTAMP_SCENARIO/logs/`
- Each run has 4 log files:
  - `pipeline.log` - Main pipeline execution
  - `data_integration.log` - PHASE 0 details
  - `diagnostics.log` - PHASE 1 analysis
  - `processing.log` - PHASE 2 processing

**Example:**

```bash
# View logs from latest run
tail -f outputs/latest/logs/pipeline.log

# Find errors in all logs
grep "ERROR" outputs/runs/run_*/logs/*.log

# Check processing steps
grep "Step" outputs/latest/logs/processing.log
```

See [LOGGING_GUIDE.md](LOGGING_GUIDE.md) for detailed logging documentation.

---

## Performance Notes

### Runtime Estimates

- **PHASE 0:** 10-60 seconds (depends on CSV sizes)
- **PHASE 1:** 30-120 seconds
- **PHASE 2:** 20-60 seconds
- **Total:** 1-5 minutes for typical datasets

### Memory Usage

- CSV files in `../nam/`: ~50-200 MB
- Merged dataset: ~100-400 MB
- Processing operations: In-place (minimal overhead)
- Visualizations: ~2-5 MB per file

### Data Considerations

- Maximum rows: 10,000+ (limited by available RAM)
- Numeric columns: 50+ supported
- Missing data: Handled automatically by KNN imputation
- Outliers: Conservative handling (clip by default)

---

## Using the Scaler Model

After Phase 2, you can apply the same transformation to new data:

```python
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the saved scaler
with open('outputs/scaler_model.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Load new data
new_data = pd.read_csv('new_dataset.csv')

# Select numeric columns (same as training)
numeric_cols = new_data.select_dtypes(include=['number']).columns

# Apply transformation
transformed = scaler.transform(new_data[numeric_cols])

# Create dataframe with transformed values
result = pd.DataFrame(transformed, columns=numeric_cols)
```

---

## Tips & Best Practices

1. **Always review Phase 1 diagnostics** before editing config
2. **Test config locally** before final run (use subset of data)
3. **Keep original data** - don't modify ../nam/ folder
4. **Version your configs** - save copies of final_config.yaml
5. **Document annotations** - add comments to final_config.yaml for future reference
6. **Monitor logs** - check console output for warnings
7. **Validate outputs** - check summary statistics after Phase 2

---

## References

- **Pandas Documentation:** https://pandas.pydata.org/docs/
- **Scikit-learn Preprocessing:** https://scikit-learn.org/stable/modules/preprocessing.html
- **YAML Format:** https://yaml.org/spec/1.2/spec.html
- **Data Preprocessing Best Practices:** https://towardsdatascience.com/feature-scaling-normalization-vs-standardization-...

---

**Questions or Issues?** Check the Troubleshooting section or review the notebook markdown cells for detailed explanations.
