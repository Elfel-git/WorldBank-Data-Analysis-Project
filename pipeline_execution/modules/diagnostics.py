"""
Module: Diagnostics
Phân tích phân phối, phát hiện outliers, tạo báo cáo chẩn đoán
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Tuple, Any
import logging
import json

logger = logging.getLogger(__name__)


class DataDiagnostics:
    """Phân tích chẩn đoán dữ liệu"""
    
    def __init__(self, dataframe: pd.DataFrame, logger: logging.Logger = None):
        self.df = dataframe.copy()
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.diagnostic_report = {}
        self.outlier_indices = {}
        
        # Use provided logger or get module logger
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger
    
    def analyze_missing_values(self) -> Dict[str, Any]:
        """Phân tích giá trị bị thiếu"""
        missing_report = {
            'total_missing': self.df.isna().sum().sum(),
            'total_records': self.df.shape[0] * self.df.shape[1],
            'missing_percentage': round(
                (self.df.isna().sum().sum() / (self.df.shape[0] * self.df.shape[1])) * 100, 
                2
            ),
            'columns_missing': {}
        }
        
        for col in self.numeric_cols:
            missing_count = self.df[col].isna().sum()
            if missing_count > 0:
                missing_report['columns_missing'][col] = {
                    'count': int(missing_count),
                    'percentage': round((missing_count / len(self.df)) * 100, 2)
                }
        
        return missing_report
    
    def analyze_distribution(self) -> Dict[str, Any]:
        """Phân tích phân phối các cột numeric"""
        distribution_report = {}
        
        for col in self.numeric_cols:
            data = self.df[col].dropna()
            
            if len(data) == 0:
                continue
            
            distribution_report[col] = {
                'count': len(data),
                'mean': round(float(data.mean()), 4),
                'median': round(float(data.median()), 4),
                'std': round(float(data.std()), 4),
                'min': round(float(data.min()), 4),
                'max': round(float(data.max()), 4),
                'q25': round(float(data.quantile(0.25)), 4),
                'q75': round(float(data.quantile(0.75)), 4),
                'skewness': round(float(data.skew()), 4),
                'kurtosis': round(float(data.kurtosis()), 4),
                # Một đại lượng thống kê đo lường độ nhọn , độ dày của một phân phối xác suất 
                # k > 0 đỉnh rất cao, đuôi nhọn còn, k < 0 thì đỉnh thấp bằng phẳng
            }
        
        return distribution_report
    
    def detect_outliers_iqr(self, multiplier: float = 1.5) -> Dict[str, List[int]]:
        """Phát hiện outliers bằng IQR method"""
        outliers = {}
        
        for col in self.numeric_cols:
            q1 = self.df[col].quantile(0.25)
            q3 = self.df[col].quantile(0.75)
            iqr = q3 - q1
            
            lower_bound = q1 - multiplier * iqr
            upper_bound = q3 + multiplier * iqr
            
            # Tìm outliers
            outlier_mask = (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
            outlier_indices = self.df[outlier_mask].index.tolist()
            
            if outlier_indices:
                outliers[col] = {
                    'count': len(outlier_indices),
                    'bounds': {
                        'lower': round(float(lower_bound), 4),
                        'upper': round(float(upper_bound), 4),
                    }
                }
                self.outlier_indices[col] = outlier_indices
        
        return outliers
    
    def detect_outliers_zscore(self, threshold: float = 3.0) -> Dict[str, List[int]]:
        """Phát hiện outliers bằng Z-score method"""
        outliers = {}
        
        for col in self.numeric_cols:
            data = self.df[col]
            mean = data.mean()
            std = data.std()
            
            if std == 0:
                continue
            
            z_scores = np.abs((data - mean) / std)
            outlier_mask = z_scores > threshold
            outlier_indices = self.df[outlier_mask].index.tolist()
            
            if outlier_indices:
                outliers[col] = {
                    'count': len(outlier_indices),
                    'threshold': threshold
                }
                self.outlier_indices[f"{col}_zscore"] = outlier_indices
        
        return outliers
    
    def run_diagnostics(self, outlier_method: str = 'iqr', 
                       iqr_multiplier: float = 1.5,
                       zscore_threshold: float = 3.0) -> Dict[str, Any]:
        """Chạy toàn bộ quy trình chẩn đoán"""
        self.logger.info("=" * 50)
        self.logger.info("PHASE 1: AUTO PROFILING & DIAGNOSTICS")
        self.logger.info("=" * 50)
        
        # Step 1: Missing values
        self.logger.info("Step 1: Analyzing missing values...")
        missing_report = self.analyze_missing_values()
        
        # Step 2: Distribution
        self.logger.info("Step 2: Analyzing distributions...")
        distribution_report = self.analyze_distribution()
        
        # Step 3: Outlier detection
        self.logger.info(f"Step 3: Detecting outliers ({outlier_method})...")
        if outlier_method == 'iqr':
            outlier_report = self.detect_outliers_iqr(iqr_multiplier)
        elif outlier_method == 'zscore':
            outlier_report = self.detect_outliers_zscore(zscore_threshold)
        else:
            outlier_report = {}
        
        self.diagnostic_report = {
            'timestamp': pd.Timestamp.now().isoformat(),
            'data_shape': self.df.shape,
            'numeric_columns': len(self.numeric_cols),
            'missing_analysis': missing_report,
            'distribution_analysis': distribution_report,
            'outlier_detection': {
                'method': outlier_method,
                'outliers': outlier_report,
                'total_outlier_records': len(set([item for sublist in self.outlier_indices.values() for item in sublist]))
            }
        }
        
        self.logger.info("Diagnostics complete!")
        self.logger.info(f"Found {self.diagnostic_report['outlier_detection']['total_outlier_records']} outlier records")
        
        return self.diagnostic_report
    
    def save_report_csv(self, output_path: str):
        """Lưu báo cáo dưới dạng CSV"""
        report_data = []
        
        dist_report = self.diagnostic_report.get('distribution_analysis', {})
        
        for col, stats in dist_report.items():
            row = {'Indicator': col}
            row.update(stats)
            report_data.append(row)
        
        if report_data:
            df_report = pd.DataFrame(report_data)
            df_report.to_csv(output_path, index=False, encoding='utf-8')
            self.logger.info(f"Report saved to {output_path}")
    
    def save_report_json(self, output_path: str):
        """Lưu báo cáo dưới dạng JSON"""
        # Convert numpy types to Python native types
        import numpy as np
        
        def convert_types(obj):
            if isinstance(obj, dict):
                return {key: convert_types(val) for key, val in obj.items()}
            elif isinstance(obj, (list, tuple)):
                return [convert_types(item) for item in obj]
            elif isinstance(obj, (np.integer, np.floating)):
                return float(obj) if isinstance(obj, np.floating) else int(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            else:
                return obj
        
        converted_report = convert_types(self.diagnostic_report)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(converted_report, f, indent=2, ensure_ascii=False)
        self.logger.info(f"Report saved to {output_path}")
    
    def create_visualizations(self, output_folder: str, figsize: Tuple[int, int] = (15, 10)):
        """Tạo visualizations: boxplots, histograms"""
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)
        
        # Boxplots
        fig, axes = plt.subplots(nrows=(len(self.numeric_cols) + 1) // 2, ncols=2, figsize=figsize)
        axes = axes.flatten()
        
        for idx, col in enumerate(self.numeric_cols):
            axes[idx].boxplot(self.df[col].dropna())
            axes[idx].set_title(f'Boxplot: {col}', fontsize=10)
            axes[idx].set_ylabel('Value')
            axes[idx].grid(True, alpha=0.3)
        
        # Xóa subplot trống
        for idx in range(len(self.numeric_cols), len(axes)):
            fig.delaxes(axes[idx])
        
        plt.tight_layout()
        plt.savefig(output_folder / 'boxplots.png', dpi=100, bbox_inches='tight')
        self.logger.info("Saved: boxplots.png")
        plt.close()
        
        # Histograms
        fig, axes = plt.subplots(nrows=(len(self.numeric_cols) + 1) // 2, ncols=2, figsize=figsize)
        axes = axes.flatten()
        
        for idx, col in enumerate(self.numeric_cols):
            axes[idx].hist(self.df[col].dropna(), bins=30, alpha=0.7, edgecolor='black')
            axes[idx].set_title(f'Histogram: {col}', fontsize=10)
            axes[idx].set_xlabel('Value')
            axes[idx].set_ylabel('Frequency')
            axes[idx].grid(True, alpha=0.3, axis='y')
        
        # Xóa subplot trống
        for idx in range(len(self.numeric_cols), len(axes)):
            fig.delaxes(axes[idx])
        
        plt.tight_layout()
        plt.savefig(output_folder / 'histograms.png', dpi=100, bbox_inches='tight')
        self.logger.info("Saved: histograms.png")
        plt.close()
