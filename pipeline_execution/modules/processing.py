"""
Module: Data Processing
Xử lý dữ liệu: Log Transform, Outlier Handling, Scaling, KNN Imputation
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.impute import KNNImputer
from sklearn.ensemble import IsolationForest
from pathlib import Path
from typing import Dict, List, Tuple, Any
import pickle
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """Xử lý dữ liệu theo cấu hình"""
    
    def __init__(self, dataframe: pd.DataFrame, logger: logging.Logger = None):
        self.df = dataframe.copy()
        self.metadata = {
            'original_shape': self.df.shape,
            'transformations': [],
        }
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        # Loại bỏ Country và Year nếu có
        self.numeric_cols = [col for col in self.numeric_cols if col not in ['Country', 'Year']]
        
        self.scaler = None
        
        # Use provided logger or get module logger
        if logger is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger
    
    def log_transform(self, features: List[str] = None, add_constant: float = 1.0) -> pd.DataFrame:
        """
        Áp dụng Log Transform vào các cột chỉ định
        - features: List cột, nếu None sử dụng tất cả positive numeric cols
        - add_constant: Hằng số để tránh log(0)
        """
        self.logger.info(f"Step 1: Log Transform (add_constant={add_constant})...")
        
        # Xác định cột cần transform
        if features is None:
            # Chọn các cột có giá trị dương
            features = []
            for col in self.numeric_cols:
                if (self.df[col].dropna() > 0).all():
                    features.append(col)
        
        # Áp dụng
        for col in features:
            if col in self.df.columns:
                # Thêm constant để tránh log(0)
                self.df[col] = np.log10(self.df[col] + add_constant)
        
        self.metadata['transformations'].append({
            'type': 'log_transform',
            'columns': features,
            'add_constant': add_constant
        })
        
        self.logger.info(f"Applied log transform to {len(features)} columns")
        
        return self.df
    
    def handle_outliers_iqr(self, features: List[str] = None, 
                            multiplier: float = 1.5, 
                            action: str = 'clip') -> pd.DataFrame:
        """
        Xử lý outliers bằng IQR method
        - action: 'clip' (giữ và clip), 'remove' (xóa rows), 'impute' (thay bằng NaN)
        """
        self.logger.info(f"Step 2: Handle Outliers (IQR, action={action})...")
        
        if features is None:
            features = self.numeric_cols
        
        outlier_counts = {}
        
        for col in features:
            if col not in self.df.columns:
                continue
            
            q1 = self.df[col].quantile(0.25)
            q3 = self.df[col].quantile(0.75)
            iqr = q3 - q1
            
            lower_bound = q1 - multiplier * iqr
            upper_bound = q3 + multiplier * iqr
            
            outlier_mask = (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
            outlier_count = outlier_mask.sum()
            
            if outlier_count > 0:
                outlier_counts[col] = outlier_count
                
                if action == 'clip':
                    self.df[col] = self.df[col].clip(lower=lower_bound, upper=upper_bound)
                elif action == 'remove':
                    self.logger.warning(f"Removing {outlier_count} rows with outliers in {col}")
                    self.df = self.df[~outlier_mask]
                elif action == 'impute':
                    self.df.loc[outlier_mask, col] = np.nan
        
        self.metadata['transformations'].append({
            'type': 'outlier_handling_iqr',
            'action': action,
            'multiplier': multiplier,
            'outliers_found': outlier_counts
        })
        
        self.logger.info(f"Found and {action}d outliers in {len(outlier_counts)} columns")
        
        return self.df
    
    def handle_outliers_isolation_forest(self, features: List[str] = None,
                                         contamination: float = 0.05,
                                         action: str = 'clip') -> pd.DataFrame:
        """
        Xử lý outliers bằng Isolation Forest
        """
        self.logger.info(f"Step 2: Handle Outliers (Isolation Forest, contamination={contamination})...")
        
        if features is None:
            features = self.numeric_cols
        
        # Chọn các cột numeric có dữ liệu
        features_to_fit = [col for col in features if col in self.numeric_cols]
        
        # Fit Isolation Forest
        isolated_df = self.df[features_to_fit].dropna()
        if len(isolated_df) > 0:
            iso_forest = IsolationForest(contamination=contamination, random_state=42)
            outlier_predictions = iso_forest.fit_predict(isolated_df)
            
            outlier_count = (outlier_predictions == -1).sum()
            self.logger.info(f"Found {outlier_count} outliers")
            
            if action == 'clip':
                # Clip bằng percentile
                for col in features_to_fit:
                    p1, p99 = self.df[col].quantile([0.01, 0.99])
                    self.df[col] = self.df[col].clip(lower=p1, upper=p99)
            
            elif action == 'impute':
                # Gán NaN cho outliers
                for idx, is_outlier in zip(isolated_df.index, outlier_predictions):
                    if is_outlier == -1:
                        for col in features_to_fit:
                            self.df.loc[idx, col] = np.nan
        
        self.metadata['transformations'].append({
            'type': 'outlier_handling_isolation_forest',
            'action': action,
            'contamination': contamination
        })
        
        return self.df
    
    def scale_normalize(self, method: str = 'standard', 
                       features: List[str] = None) -> Tuple[pd.DataFrame, Any]:
        """
        Scaling & Normalization
        - method: 'standard' (StandardScaler), 'minmax' (MinMaxScaler), 'robust' (RobustScaler)
        - features: List cột, nếu None sử dụng tất cả numeric cols
        """
        self.logger.info(f"Step 3: Scaling & Normalization ({method})...")
        
        if features is None:
            features = self.numeric_cols
        
        # Chọn cột hợp lệ
        features_to_scale = [col for col in features if col in self.df.columns]
        
        # Tạo scaler
        if method == 'standard':
            self.scaler = StandardScaler()
        elif method == 'minmax':
            self.scaler = MinMaxScaler()
        elif method == 'robust':
            self.scaler = RobustScaler()
        else:
            raise ValueError(f"Unknown scaling method: {method}")
        
        # Fit & transform
        scaled_data = self.scaler.fit_transform(self.df[features_to_scale])
        self.df[features_to_scale] = scaled_data
        
        self.metadata['transformations'].append({
            'type': 'scaling',
            'method': method,
            'columns': features_to_scale
        })
        
        self.logger.info(f"Scaled {len(features_to_scale)} columns with {method}")
        
        return self.df, self.scaler
    
    def knn_impute(self, n_neighbors: int = 5, features: List[str] = None) -> pd.DataFrame:
        """
        KNN Imputation cho missing values
        """
        self.logger.info(f"Step 4: KNN Imputation (n_neighbors={n_neighbors})...")
        
        if features is None:
            features = self.numeric_cols
        
        # Chọn cột hợp lệ
        features_to_impute = [col for col in features if col in self.df.columns]
        
        # Kiểm tra missing values
        missing_before = self.df[features_to_impute].isna().sum().sum()
        
        if missing_before > 0:
            # Fit & transform KNN Imputer
            knn_imputer = KNNImputer(n_neighbors=n_neighbors)
            imputed_data = knn_imputer.fit_transform(self.df[features_to_impute])
            self.df[features_to_impute] = imputed_data
            
            missing_after = self.df[features_to_impute].isna().sum().sum()
            self.logger.info(f"Imputed missing values: {missing_before} -> {missing_after}")
        else:
            self.logger.info("No missing values to impute")
        
        self.metadata['transformations'].append({
            'type': 'knn_imputation',
            'n_neighbors': n_neighbors,
            'columns': features_to_impute
        })
        
        return self.df
    
    def run_processing_pipeline(self, config: Dict[str, Any]) -> Tuple[pd.DataFrame, Any]:
        """
        Chạy toàn bộ processing pipeline theo config
        
        Expected config format:
        {
            'log_transform': {'enabled': True, 'add_constant': 1.0},
            'outlier_handling': {'method': 'iqr', 'action': 'clip', 'multiplier': 1.5},
            'scaling': {'method': 'standard'},
            'imputation': {'n_neighbors': 5}
        }
        """
        self.logger.info("=" * 50)
        self.logger.info("PHASE 2: EXECUTION PIPELINE")
        self.logger.info("=" * 50)
        
        # Step 1: Log Transform
        if config.get('log_transform', {}).get('enabled', False):
            self.log_transform(
                add_constant=config.get('log_transform', {}).get('add_constant', 1.0)
            )
        
        # Step 2: Outlier Handling
        outlier_config = config.get('outlier_handling', {})
        method = outlier_config.get('method', 'iqr')
        
        if method == 'iqr':
            self.handle_outliers_iqr(
                multiplier=outlier_config.get('multiplier', 1.5),
                action=outlier_config.get('action', 'clip')
            )
        elif method == 'isolation_forest':
            self.handle_outliers_isolation_forest(
                contamination=outlier_config.get('contamination', 0.05),
                action=outlier_config.get('action', 'clip')
            )
        
        # Step 3: Scaling
        scaling_config = config.get('scaling', {})
        self.scale_normalize(
            method=scaling_config.get('method', 'standard')
        )
        
        # Step 4: Imputation
        imputation_config = config.get('imputation', {})
        self.knn_impute(
            n_neighbors=imputation_config.get('n_neighbors', 5)
        )
        
        self.logger.info("Processing pipeline complete!")
        self.logger.info(f"Final shape: {self.df.shape}")
        self.logger.info(f"Missing values: {self.df.isna().sum().sum()}")
        
        return self.df, self.scaler
    
    def save_scaler(self, output_path: str):
        """Lưu scaler model"""
        if self.scaler is None:
            raise ValueError("Scaler is None, run scaling first")
        
        with open(output_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        self.logger.info(f"Scaler saved to {output_path}")
    
    def get_metadata(self) -> Dict[str, Any]:
        """Lấy metadata về transformations"""
        return self.metadata
