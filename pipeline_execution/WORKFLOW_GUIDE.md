# WORKFLOW GUIDE: Step-by-Step Execution
## Complete walkthrough for running the pipeline

---

## ⚡ Quick Start (5 minutes)

### For experienced users:
```bash
# 1. Open notebook and run all
jupyter notebook 00_data_integration.ipynb

# 2. Check outputs and review diagnostics
jupyter notebook 01_auto_profiling.ipynb

# 3. Copy and edit config
cp outputs/draft_config.yaml outputs/final_config.yaml
# Edit final_config.yaml with your preferred settings

# 4. Run final processing
jupyter notebook 02_execution_pipeline.ipynb
```

---

## 📖 Detailed Step-by-Step Guide

### STEP 1: Prepare Environment
**Goal:** Set up Python and verify dependencies

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install pandas numpy scikit-learn matplotlib seaborn pyyaml
```

**Verify installation:**
```python
import pandas, numpy, sklearn, matplotlib, seaborn, yaml
print("✓ All packages installed successfully")
```

---

### STEP 2: Verify Input Data
**Goal:** Confirm CSV files are ready

**Action checklist:**
- [ ] Navigate to `../nam/` folder
- [ ] Verify CSV files exist (e.g., "Access to electricity.csv")
- [ ] Note number of CSV files found
- [ ] Check file sizes (should be > 1KB each)

**Expected structure:**
```
nam/
├── Access to electricity (% of population).csv
├── Agriculture, forestry, and fishing, value added (% of GDP).csv
├── Domestic credit to private sector (% of GDP).csv
├── ... (more indicator files)
```

**If files are missing:**
- Download from World Bank: https://data.worldbank.org/
- Place in `../nam/` folder
- Ensure CSV format (comma-separated)

---

### STEP 3: Run PHASE 0 - Data Integration
**Goal:** Merge all CSV files into one dataset

**Open notebook:**
```
File: 00_data_integration.ipynb
```

**Execute steps:**

1. **Run cell 1-2:** Import modules
   - Should show: ✓ Modules imported successfully

2. **Run cell 3:** Verify input folder
   - Should show: Found N CSV files in ../nam

3. **Run cell 4:** Initialize DataIntegration
   - Should show: Loading CSV files and status updates
   - Expected: "INTEGRATION COMPLETE"

4. **Run cell 5:** Inspect merged data
   - Check Shape (should be: rows = countries × years, cols = indicators + 2)
   - Look at first few rows

5. **Run cell 6:** Check data summary
   - Note: Countries count, Records count, Missing percentage
   - Expected: Missing % should be 30-60% for World Bank data

6. **Run cell 7:** Save output
   - Should create: `outputs/dataset_merged.csv`
   - Note the file size

**Checkpoint:** ✓ dataset_merged.csv created successfully

---

### STEP 4: Run PHASE 1 - Auto Profiling & Diagnostics
**Goal:** Analyze data and create diagnostic reports

**Open notebook:**
```
File: 01_auto_profiling.ipynb
```

**Execute steps:**

1. **Run cell 1-2:** Import modules and load data
   - Should show: Loaded dataset_merged.csv

2. **Run cell 3:** Initialize Diagnostics
   - Shows: PHASE 1: AUTO PROFILING & DIAGNOSTICS

3. **Run cell 4:** Inspect results - Missing values
   - Look at: Total missing%, Columns with most missing values
   - Example: "Foreign direct investment": 45.5%

4. **Run cell 5-6:** Inspect results - Distribution analysis
   - Look at: Mean, Median, Std, Skewness
   - Highly skewed (|skewness| > 2) → need log transform

5. **Run cell 7-8:** Inspect results - Outlier detection
   - Look at: Total outlier records, Columns with outliers
   - Note: Outlier percentage helps decide IQR multiplier

6. **Run cell 9:** Save diagnostic reports
   - Creates: diagnostic_report.csv, diagnostic_report.json

7. **Run cell 10:** Create visualizations
   - Creates: boxplots.png, histograms.png
   - Review these visually before next step

8. **Run cell 11-14:** Create draft configuration
   - Shows: Recommendations based on data analysis
   - Creates: outputs/draft_config.yaml

**Checkpoint:** ✓ Diagnostic reports and draft config created

**Review outputs:**
```
outputs/
├── diagnostic_report.csv      # Open in Excel for easy viewing
├── diagnostic_report.json     # View in text editor
├── boxplots.png              # Look for extreme points
├── histograms.png            # Look for non-normal shapes
└── draft_config.yaml         # Review recommendations
```

---

### STEP 5: PHASE 1.5 - Review & Configure (MANUAL)
**Goal:** Make informed decisions about data processing

**ACTION REQUIRED - This is where you make decisions!**

#### 5a. Review Diagnostic Report

**Open:** `outputs/diagnostic_report.csv`
- Use Excel or any spreadsheet software
- Sort by `skewness` to find most skewed columns
- Sort by missing values (% of NaN)

**Key questions to ask:**
- Q1: Are there highly skewed distributions (|skewness| > 2)?
  - YES → Enable log_transform in config
  - Answer examples: GDP, FDI, Trade are often skewed

- Q2: Are there many outliers (>5% of data)?
  - YES → Consider increasing IQR multiplier (1.8, 2.0)
  - Or use isolation_forest method

- Q3: Is data very sparse (>50% missing)?
  - YES → Reduce n_neighbors in imputation (3-5)
  - Consider if data quality is acceptable

#### 5b. Review Visualizations

**Open:** `outputs/boxplots.png`
- Look at each boxplot:
  - Points above/below whiskers = outliers
  - Some outliers are expected; too many = might need preprocessing

**Open:** `outputs/histograms.png`
- Look for distribution shapes:
  - Bell curve shape = normal (good ✓)
  - Long right tail = right-skewed (log transform recommended)
  - Many spikes = discrete data (might need different approach)

#### 5c. Edit Configuration

**File to edit:** `outputs/draft_config.yaml`

**Steps:**
1. Make a copy: 
   ```bash
   cp outputs/draft_config.yaml outputs/final_config.yaml
   ```

2. Open `final_config.yaml` in text editor

3. Find these sections and decide:

**Section 1: Log Transform**
```yaml
log_transform:
  enabled: false  # Change based on skewness analysis
```
- Change to `true` if skewness > 2
- Common in economic indicators (GDP, FDI, Trade)

**Section 2: Outlier Detection**
```yaml
outlier_detection:
  method: 'iqr'
  iqr_multiplier: 1.5  # Can adjust to 1.8, 2.0
  action: 'clip'  # Options: clip, remove, impute
```
- Use 'clip' for most cases (safe)
- Use 'impute' if many outliers (will replace with NaN for KNN to fill)

**Section 3: Scaling**
```yaml
scaling:
  method: 'standard'  # Options: standard, minmax, robust
```
- 'standard' = z-score normalization (recommended)
- 'robust' = uses percentiles (better for extreme outliers)
- 'minmax' = scales to [0,1] (rarely needed)

**Section 4: Imputation**
```yaml
imputation:
  n_neighbors: 5  # Reduce to 3-5 if data is sparse
```
- Higher values (5-7) better if data is dense
- Lower values (3-5) better if data is sparse (>30% missing)

**Example configurations:**

*For typical clean data:*
```yaml
log_transform: {enabled: true}
outlier_detection: {iqr_multiplier: 1.5, action: clip}
scaling: {method: standard}
imputation: {n_neighbors: 5}
```

*For very noisy data:*
```yaml
log_transform: {enabled: true}
outlier_detection: {iqr_multiplier: 2.0, action: clip}
scaling: {method: robust}
imputation: {n_neighbors: 3}
```

4. Save the file as `final_config.yaml`

**Verify:**
- Check indentation (use spaces, not tabs)
- No duplicate YAML keys
- Use online YAML validator if unsure

**Checkpoint:** ✓ final_config.yaml saved and ready

---

### STEP 6: Run PHASE 2 - Execution Pipeline
**Goal:** Apply processing and generate final dataset

**Open notebook:**
```
File: 02_execution_pipeline.ipynb
```

**Execute steps:**

1. **Run cell 1-2:** Import modules
   - Should show: ✓ Modules imported successfully

2. **Run cell 3:** Load merged data
   - Should show: Loaded dataset_merged.csv with shape

3. **Run cell 4:** Load configuration
   - Should show: Loaded config from final_config.yaml
   - If final_config.yaml doesn't exist, will use draft_config.yaml
   - Should show: ✓ Config validation passed

4. **Run cell 5:** Display configuration
   - Verify settings before processing
   - Last chance to check if config is correct!

5. **Run cell 6:** Initialize processor
   - Shows: DataProcessor initialized

6. **Run cell 7:** Run processing pipeline
   - Shows steps:
     - Step 1: Log Transform...
     - Step 2: Handle Outliers...
     - Step 3: Scaling & Normalization...
     - Step 4: KNN Imputation...
   - Should show: PROCESSING COMPLETE

7. **Run cell 8:** Inspect results
   - Check: Shape remains same, Missing values = 0
   - Look at: First few rows (should be normalized)

8. **Run cell 9:** Check statistics
   - Verify: Mean values close to 0, Std values close to 1
   - This confirms scaling worked

9. **Run cell 10:** Save outputs
   - Creates: dataset_final.csv, scaler_model.pkl

10. **Run cell 11-12:** Save metadata and final summary
    - Creates: processing_metadata.json
    - Shows: Complete pipeline output summary

**Checkpoint:** ✓ All processing complete!

**Final outputs:**
```
outputs/
├── dataset_final.csv          # ← Use this for ML!
├── scaler_model.pkl           # ← Save for later use
└── processing_metadata.json   # ← Log of transformations
```

---

## ✅ Completion Checklist

After successfully running all phases:

- [ ] PHASE 0 complete
  - [ ] dataset_merged.csv exists (~50-200 MB)
  
- [ ] PHASE 1 complete
  - [ ] diagnostic_report.csv generated
  - [ ] diagnostic_report.json generated
  - [ ] boxplots.png generated
  - [ ] histograms.png generated
  - [ ] draft_config.yaml generated

- [ ] PHASE 1.5 complete
  - [ ] Reviewed diagnostic reports
  - [ ] Reviewed visualizations
  - [ ] Created final_config.yaml

- [ ] PHASE 2 complete
  - [ ] dataset_final.csv generated (ready for ML!)
  - [ ] scaler_model.pkl generated
  - [ ] processing_metadata.json generated

---

## 🎓 What Each Output File Means

| File | What It Is | How To Use |
|------|-----------|-----------|
| `dataset_merged.csv` | Raw data combined | Diagnostic reference |
| `diagnostic_report.csv` | Statistics table | Decision-making |
| `boxplots.png` | Outlier visualization | Visual inspection |
| `histograms.png` | Distribution plots | Distribution analysis |
| `draft_config.yaml` | AI recommendation | Starting point for config |
| `final_config.yaml` | Your final config | Used by Phase 2 |
| `dataset_final.csv` | **FINAL PRODUCT** | Use for ML models! |
| `scaler_model.pkl` | Transformation object | Apply to new data |
| `processing_metadata.json` | Processing log | Audit trail |

---

## 🔧 Troubleshooting During Execution

### Notebook runs but shows warnings

**Warning: "FutureWarning: Attempting to set a value on a copy"**
- Safe to ignore (pandas internal behavior)

**Warning: "SettingWithCopyWarning"**
- Also safe to ignore for this pipeline

### Notebook stops with error

| Error | Cause | Solution |
|-------|-------|----------|
| ModuleNotFoundError | Missing package | `pip install [package_name]` |
| FileNotFoundError | Wrong path | Check folder structure |
| MemoryError | Dataset too large | Process in chunks |
| ValueError: inconsistent | Different column types | Check data types |

### Results seem wrong

**Check:**
1. Are you using correct input file?
2. Did you run previous phases?
3. Is config reasonable?
4. Are missing values expected?

---

## 🚀 Next Steps After Pipeline

**Your dataset is ready!** Now you can:

1. **Load for Machine Learning:**
   ```python
   import pandas as pd
   df = pd.read_csv('outputs/dataset_final.csv')
   
   # Separate features and target
   X = df[relevant_columns]
   y = df[target_column]
   
   # Train your model!
   from sklearn.ensemble import RandomForestClassifier
   model = RandomForestClassifier()
   model.fit(X, y)
   ```

2. **Apply to New Data:**
   ```python
   import pickle
   
   # Load scaler
   with open('outputs/scaler_model.pkl', 'rb') as f:
       scaler = pickle.load(f)
   
   # Transform new data
   new_scaled = scaler.transform(new_raw_data[numeric_cols])
   ```

3. **Analyze Results:**
   ```python
   # Check feature importance, correlations, etc.
   import matplotlib.pyplot as plt
   plt.hist(X.values, bins=50)
   ```

---

## 📞 Getting Help

- Review README.md for detailed documentation
- Check config_template.yaml for parameter explanations
- Review notebook markdown cells for explanations
- Check console output messages (often descriptive)

---

**Happy Data Processing!** 🎉
