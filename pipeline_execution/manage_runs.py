"""
Helper Script: Manage Pipeline Scenarios and Runs
==================================================

Ứng dụng: Quản lý scenarios, runs, so sánh kết quả

Usage:
    python manage_runs.py list                    # Liệt kê tất cả runs
    python manage_runs.py compare                 # So sánh runs (3 mới nhất)
    python manage_runs.py info baseline           # Info về run baseline
    python manage_runs.py scenarios               # Liệt kê scenarios
    python manage_runs.py latest                  # Show latest run info
"""

import sys
import json
from pathlib import Path
from tabulate import tabulate

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent / 'modules'))

from run_manager import RunManager


def cmd_list(rm: RunManager, limit: int = None):
    """Liệt kê tất cả runs"""
    runs = rm.get_run_list()
    
    if not runs:
        print("❌ No runs found.")
        return
    
    if limit:
        runs = runs[:limit]
    
    print("\n" + "="*100)
    print(f"📚 RUN LIST ({len(rm.get_run_list())} total)")
    print("="*100 + "\n")
    
    data = []
    for i, (run_name, run_path) in enumerate(runs, 1):
        info = rm.get_run_info(run_path)
        files_count = sum(1 for v in info['files'].values() if v)
        data.append([
            i,
            info['scenario'].upper(),
            info['timestamp'],
            f"{info['total_size_mb']} MB",
            f"{files_count}/{len(info['files'])}",
            Path(info['path']).name
        ])
    
    headers = ["#", "Scenario", "Timestamp", "Size", "Files", "Folder"]
    print(tabulate(data, headers=headers, tablefmt='grid'))
    print()


def cmd_scenarios(rm: RunManager):
    """Liệt kê tất cả scenario configs"""
    scenarios = rm.list_scenarios()
    
    print("\n" + "="*100)
    print("🎯 SCENARIO CONFIGS")
    print("="*100 + "\n")
    
    if not scenarios:
        print("❌ No scenarios found in outputs/scenarios/")
        print("   Create: outputs/scenarios/baseline_config.yaml")
        print("           outputs/scenarios/conservative_config.yaml")
        print("           outputs/scenarios/aggressive_config.yaml")
        return
    
    for i, scenario in enumerate(sorted(scenarios), 1):
        path = rm.scenarios_dir / scenario
        size = path.stat().st_size
        print(f"  {i}. {scenario:<35} ({size/1024:.2f} KB)")
    
    print()


def cmd_compare(rm: RunManager, limit: int = 3):
    """So sánh runs (mặc định 3 mới nhất)"""
    runs = rm.get_run_list()[:limit]
    
    if len(runs) < 2:
        print("❌ Need at least 2 runs to compare.")
        return
    
    print("\n" + "="*100)
    print(f"🔄 COMPARING {len(runs)} RUNS")
    print("="*100 + "\n")
    
    run_dirs = [run_path for _, run_path in runs]
    comparison = rm.compare_runs(run_dirs)
    
    data = []
    for scenario, metrics in comparison.items():
        data.append([
            scenario.upper(),
            metrics['timestamp'],
            metrics['size_mb'],
            metrics['files_present'],
        ])
    
    headers = ["Scenario", "Timestamp", "Size (MB)", "Files Present"]
    print(tabulate(data, headers=headers, tablefmt='grid'))
    print()


def cmd_info(rm: RunManager, scenario_or_run: str):
    """Lấy chi tiết về một run"""
    runs = rm.get_run_list()
    
    # Tìm run matching scenario_or_run
    run_path = None
    for run_name, path in runs:
        if scenario_or_run.lower() in run_name.lower() or scenario_or_run.lower() == rm.get_run_info(path)['scenario'].lower():
            run_path = path
            break
    
    if not run_path:
        print(f"❌ Run not found: {scenario_or_run}")
        print("   Available scenarios:", [rm.get_run_info(p)['scenario'] for _, p in runs[:5]])
        return
    
    info = rm.get_run_info(run_path)
    
    print("\n" + "="*100)
    print(f"📋 RUN DETAILS: {info['run_name']}")
    print("="*100 + "\n")
    
    print(f"Scenario:     {info['scenario'].upper()}")
    print(f"Timestamp:    {info['timestamp']}")
    print(f"Total Size:   {info['total_size_mb']} MB")
    print(f"Path:         {info['path']}")
    
    print(f"\nFiles ({sum(1 for v in info['files'].values() if v)}/{len(info['files'])}):")
    for file_name, exists in sorted(info['files'].items()):
        status = "✓" if exists else "✗"
        print(f"  {status} {file_name}")
    
    # Try to load run_summary.json
    summary_path = run_path / 'run_summary.json'
    if summary_path.exists():
        with open(summary_path, 'r') as f:
            summary = json.load(f)
        
        if 'summary' in summary:
            print(f"\nRun Summary:")
            for key, value in summary['summary'].items():
                print(f"  {key}: {value}")
    
    print()


def cmd_latest(rm: RunManager):
    """Hiển thị info về run mới nhất"""
    runs = rm.get_run_list()
    
    if not runs:
        print("❌ No runs found.")
        return
    
    latest_run = runs[0][1]
    info = rm.get_run_info(latest_run)
    
    print("\n" + "="*100)
    print("⭐ LATEST RUN")
    print("="*100 + "\n")
    
    print(f"Scenario:     {info['scenario'].upper()}")
    print(f"Timestamp:    {info['timestamp']}")
    print(f"Path:         {info['path']}")
    print(f"Latest also:  {rm.latest_dir}")
    print()


def cmd_cleanup(rm: RunManager, days_old: int = 30):
    """Cleanup runs cũ (experimental)"""
    from datetime import datetime, timedelta
    
    runs = rm.get_run_list()
    cutoff = datetime.now() - timedelta(days=days_old)
    
    print(f"\n⚠️  Finding runs older than {days_old} days...")
    
    old_runs = []
    for run_name, run_path in runs:
        # Parse timestamp
        timestamp_str = run_name.split('_')[1:3]
        if len(timestamp_str) == 2:
            date_str = timestamp_str[0][:8]  # YYYYMMDD
            try:
                run_date = datetime.strptime(date_str, '%Y%m%d')
                if run_date < cutoff:
                    old_runs.append((run_name, run_path))
            except:
                pass
    
    if not old_runs:
        print(f"✓ No runs older than {days_old} days found.")
        return
    
    print(f"\nFound {len(old_runs)} old runs:")
    for run_name, run_path in old_runs:
        print(f"  - {run_name}")
    
    print("\n⚠️  Use caution! Backup before deleting.")
    print("TODO: Implement with user confirmation")


def main():
    """Main CLI"""
    rm = RunManager('./outputs')
    
    if len(sys.argv) < 2:
        # Show help
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
        cmd_list(rm, limit=limit)
    
    elif command == 'scenarios':
        cmd_scenarios(rm)
    
    elif command == 'compare':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        cmd_compare(rm, limit=limit)
    
    elif command == 'info':
        if len(sys.argv) < 3:
            print("❌ Usage: python manage_runs.py info <scenario|run_name>")
            return
        cmd_info(rm, sys.argv[2])
    
    elif command == 'latest':
        cmd_latest(rm)
    
    elif command == 'cleanup':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        cmd_cleanup(rm, days_old=days)
    
    else:
        print(f"❌ Unknown command: {command}")
        print(__doc__)


if __name__ == '__main__':
    main()
