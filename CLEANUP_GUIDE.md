# 🧹 CLEANUP GUIDE - Remove Old/Redundant Files

## Overview

Sau khi refactor, một số file cũ/redundant nên được xóa để tiết kiệm không gian disk.

---

## Files to Remove

### 1. Old Diagnostic JSON (Redundant)

**Location**: `pipeline_execution/outputs/`

```
❌ diagnostic_report.json          (Redundant - use CSV instead)
❌ draft_config.yaml               (Old - use from runs/ folder)
❌ final_config.yaml               (Old - use from runs/ folder)
```

**Why**:

- Replaced by `diagnostic_report.csv` (more compatible)
- Config files now saved per run in `runs/` folder

**How to Remove** (Windows PowerShell):

```powershell
cd pipeline_execution/outputs
rm diagnostic_report.json
rm draft_config.yaml
rm final_config.yaml
```

**How to Remove** (macOS/Linux):

```bash
cd pipeline_execution/outputs
rm diagnostic_report.json draft_config.yaml final_config.yaml
```

---

### 2. Keep These Old Runs (Optional)

**Location**: `pipeline_execution/outputs/runs/`

These are historical snapshots - delete if disk space is needed:

```powershell
# Remove specific old run
rm -r pipeline_execution/outputs/runs/run_20260413_143000_default

# Remove all but latest 3 runs
cd pipeline_execution/outputs/runs
ls -t | Select-Object -Skip 3 | Remove-Item -Recurse -Force
```

---

### 3. Auto-Cleanup Strategy

To automatically clean up old files, add to your pipeline:

```python
# After successful run, cleanup old diagnostics
import os
from pathlib import Path

outputs_dir = Path('pipeline_execution/outputs')

# Remove old JSON files
for json_file in outputs_dir.glob('diagnostic_report.json'):
    json_file.unlink()
    print(f"Removed: {json_file}")

# Remove old config files
for cfg_file in outputs_dir.glob('*_config.yaml'):
    cfg_file.unlink()
    print(f"Removed: {cfg_file}")

# Keep only latest 5 runs
runs_dir = outputs_dir / 'runs'
runs = sorted(runs_dir.glob('run_*'), key=lambda x: x.stat().st_mtime, reverse=True)
for old_run in runs[5:]:
    import shutil
    shutil.rmtree(old_run)
    print(f"Removed old run: {old_run}")
```

---

## Disk Space Before & After

```
BEFORE (with redundant files):
├── diagnostic_report.json           (8 KB)   ❌
├── diagnostic_report.csv            (2 KB)   ✅
├── draft_config.yaml                (1 KB)   ❌
├── final_config.yaml                (1 KB)   ❌
├── runs/                            (varies)
└── Total: ~12 KB (redundant)

AFTER (cleaned):
├── diagnostic_report.csv            (2 KB)   ✅
├── runs/
│   └── run_20260413_230212_default/
│       ├── diagnostic_report.csv    (2 KB)   ✅
│       └── config.yaml              (1 KB)   ✅
└── latest/ (symlink to latest run)
```

**Space Saved**: ~10 KB per run × number of old runs

---

## Safe Cleanup Checklist

- [ ] Verify `outputs/latest/` has all needed files
- [ ] Confirm recent runs in `outputs/runs/` are complete
- [ ] Backup important results before deletion
- [ ] Remove JSON files: `diagnostic_report.json`
- [ ] Remove old configs: `draft_config.yaml`, `final_config.yaml`
- [ ] Consider keeping last 5 runs for reference
- [ ] Delete very old runs (> 1 month) if needed

---

## Restore from Version Control

If you accidentally deleted needed files:

```bash
# See git history
git log --name-status

# Restore specific file
git checkout HEAD~N -- pipeline_execution/outputs/diagnostic_report.json

# Or entire folder
git checkout HEAD~N -- pipeline_execution/outputs/
```

---

## Notes

✅ **Safe to delete**:

- Old JSON diagnostic reports
- Old draft/final config files (copies in runs/ directory)
- Old runs > 1 month old (keep outputs/latest/)

⚠️ **Don't delete**:

- `outputs/latest/` folder or its contents
- Most recent run in `runs/` folder
- `outputs/runs/` folder structure itself
- `.gitignore` file

---

**Last Updated**: 2026-04-13  
**Status**: Optional cleanup
