"""
Module: Tree-based Modeling (Phase 3 Extra / Phase 4)
Chứng minh sức mạnh của Tiền xử lý dữ liệu qua 3 kịch bản và trích xuất Feature Importance.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_squared_error, r2_score
from pathlib import Path
import logging

# Khởi tạo module-level logger phòng trường hợp không có custom logger truyền vào
logger = logging.getLogger(__name__)

class TreeModeler:
    """Mô hình hóa dữ liệu vĩ mô bằng cấu trúc Cây quyết định và kiểm chứng kịch bản dữ liệu khuyết"""
    
    def __init__(self, df: pd.DataFrame, target_col: str = 'GDPC_2015', custom_logger: logging.Logger = None):
        """
        Khởi tạo mô hình Tree-based với dữ liệu đầu vào.
        """
        self.raw_df = df.copy()
        self.target_col = target_col
        self.drop_cols = ['Country', 'Year', 'Country Code', 'ID']
        
        # Ưu tiên sử dụng logger hệ thống truyền từ pipeline chính xuống
        self.logger = custom_logger if custom_logger else logger
        self.scenario_scores = {}

    def _prepare_features(self, df: pd.DataFrame):
        """Hàm nội bộ tách tập thuộc tính X và biến mục tiêu y"""
        cols_to_drop = [c for c in self.drop_cols if c in df.columns] + [self.target_col]
        X = df.drop(columns=cols_to_drop, errors='ignore')
        y = df[self.target_col] if self.target_col in df.columns else None
        return X, y

    def run_scenario_1_no_handling(self):
        """Kịch bản 1: Để nguyên NaN và đưa vào huấn luyện (Chứng minh lỗi Crash)"""
        self.logger.info("=" * 60)
        self.logger.info("SCENARIO 1: HUẤN LUYỆN VỚI DỮ LIỆU KHUYẾT THIẾU (RAW NAN)")
        self.logger.info("=" * 60)
        
        X, y = self._prepare_features(self.raw_df)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        
        try:
            self.logger.info("Đang thử nghiệm fit mô hình Random Forest trực tiếp với NaN...")
            rf.fit(X_train, y_train)
        except Exception as e:
            # Ghi nhận lỗi trực tiếp vào log hệ thống để làm bằng chứng cho báo cáo
            self.scenario_scores['1. Raw NaN (Crash)'] = 0.0
            self.logger.error(f"🚨 MÔ HÌNH BỊ CRASH THÀNH CÔNG! Loại lỗi: [{type(e).__name__}]")
            self.logger.error(f"Chi tiết lỗi hệ thống: {str(e)}")
            self.logger.warning("=> KẾT LUẬN: Thuật toán Random Forest của scikit-learn không chấp nhận dữ liệu rỗng.")

    def run_scenario_2_wrong_handling(self):
        """Kịch bản 2: Xử lý sai cách (Target Imputation & Data Leakage trước khi split)"""
        self.logger.info("=" * 60)
        self.logger.info("SCENARIO 2: XỬ LÝ SAI CÁCH (DATA LEAKAGE & DIỀN BÙ BIẾN TARGET Y)")
        self.logger.info("=" * 60)
        
        bad_df = self.raw_df.copy()
        self.logger.info("Thực hiện lỗi sai kinh điển: Điền bù số Mean cho toàn bộ bảng bao gồm cả cột Target Y...")
        
        for col in bad_df.select_dtypes(include=np.number).columns:
            bad_df[col] = bad_df[col].fillna(bad_df[col].mean())
            
        X, y = self._prepare_features(bad_df)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X_train, y_train)
        
        y_pred = rf.predict(X_test)
        r2 = r2_score(y_test, y_pred)

        self.scenario_scores['2. Data Leakage (Fake R²)'] = r2
        
        self.logger.info(f"✓ Mô hình chạy thông qua thành công nhờ lấp liếm dữ liệu.")
        self.logger.info(f"📊 Kết quả đánh giá 'Ảo': R2 Score = {r2:.4f}")
        self.logger.warning("=> KẾT LUẬN: Điểm số cao là do rò rỉ dữ liệu (Data Leakage). Mô hình đã biết trước phân phối tổng.")

    def run_scenario_3_correct_handling(self, output_folder: Path):
        """Kịch bản 3: Tiền xử lý chuẩn chỉnh và Trích xuất Feature Importance"""
        self.logger.info("=" * 60)
        self.logger.info("SCENARIO 3: TIỀN XỬ LÝ CHUẨN MLOPS (XÓA Y, CHIA TRAIN/TEST, KNN IMPUTE X)")
        self.logger.info("=" * 60)
        
        df = self.raw_df.copy()
        
        # 1. Trảm sạch các hàng khuyết Y trước
        initial_len = len(df)
        df = df.dropna(subset=[self.target_col])
        self.logger.info(f"Step 1: Đã xóa {initial_len - len(df)} hàng khuyết thiếu biến mục tiêu '{self.target_col}'.")
        
        X, y = self._prepare_features(df)
        
        # 2. Chia tách dữ liệu TRƯỚC khi can thiệp toán học
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.logger.info(f"Step 2: Phân tách dữ liệu: Tập Train ({len(X_train)} rows) | Tập Test ({len(X_test)} rows).")
        
        # 3. Sử dụng KNN Imputer học luật trên Train, áp đặt lên Test (Ngăn chặn Data Leakage hoàn toàn)
        self.logger.info("Step 3: Khởi tạo KNN Imputer (k=5). Tiến hành huấn luyện bộ điền bù trên tập Train...")
        imputer = KNNImputer(n_neighbors=5)
        
        X_train_imputed = pd.DataFrame(imputer.fit_transform(X_train), columns=X_train.columns)
        X_test_imputed = pd.DataFrame(imputer.transform(X_test), columns=X_test.columns)
        self.logger.info("✓ Quá trình nội suy dữ liệu khuyết thiếu cho các chỉ số vĩ mô (X) hoàn tất trung thực.")
        
        # 4. Huấn luyện mô hình thực chất
        self.logger.info("Step 4: Khởi chạy mô hình Random Forest Regressor (100 cây)...")
        rf = RandomForestRegressor(n_estimators=100, random_state=42)
        rf.fit(X_train_imputed, y_train)
        
        # 5. Đánh giá chất lượng mô hình
        y_pred = rf.predict(X_test_imputed)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        self.scenario_scores['3. MLOps Standard (Real R²)'] = r2
        
        self.logger.info(f"📊 KẾT QUẢ ĐÁNH GIÁ THỰC TẾ: R2 Score = {r2:.4f} | RMSE = {rmse:.2f} USD")
        
        # 6. Xuất đồ thị kiểm chứng đóng góp của Features
        self._plot_feature_importance(rf, X_train.columns, r2, output_folder)

    def _plot_scenario_comparison(self, output_dir: Path):
        """Vẽ biểu đồ so sánh hiệu suất giữa 3 kịch bản xử lý dữ liệu"""
        self.logger.info("Đang tạo biểu đồ so sánh 3 kịch bản...")
        
        scenarios = list(self.scenario_scores.keys())
        scores = list(self.scenario_scores.values())
        
        plt.figure(figsize=(10, 6))
        
        # Màu sắc mang ý nghĩa: Đỏ (Lỗi) - Cam (Cảnh báo ảo) - Xanh lá (Chuẩn)
        colors = ['#e74c3c', '#f39c12', '#2ecc71'] 
        
        bars = plt.bar(scenarios, scores, color=colors, edgecolor='black', alpha=0.85)
        
        plt.ylim(0, 1.15) # Kéo dài trục Y lên chút để có chỗ viết text
        plt.title('Impact of Data Imputation on Model Accuracy (R² Score)', fontsize=15, fontweight='bold', pad=20)
        plt.ylabel('R² Score (Accuracy)', fontsize=12)
        
        # Ghi chú từng con số lên đầu mỗi cột
        for bar, score in zip(bars, scores):
            yval = bar.get_height()
            # Nếu điểm = 0 thì ghi chữ CRASH, ngược lại ghi điểm R2
            label = f"CRASH!" if score == 0 else f"{score:.3f}"
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.02, 
                     label, ha='center', va='bottom', fontsize=12, fontweight='bold')
            
        # Thêm đường grid ngang cho dễ nhìn
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        
        # Xuất file
        out_path = output_dir / 'scenario_comparison.png'
        plt.savefig(out_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        self.logger.info(f"✓ Đã lưu biểu đồ so sánh kịch bản tại: {out_path}")

    def _plot_feature_importance(self, model, feature_names, r2_score, output_folder: Path):
        """Hàm nội bộ vẽ đồ thị Gini Feature Importance"""
        self.logger.info("Đang tạo biểu đồ Feature Importance...")
        importances = model.feature_importances_
        
        feat_imp = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
        feat_imp = feat_imp.sort_values(by='Importance', ascending=False)
        
        plt.figure(figsize=(11, 6))
        sns.barplot(x='Importance', y='Feature', data=feat_imp, palette='coolwarm')
        plt.title(f"Macroeconomic Drivers of GDP per Capita (GDPC_2015)\n[Random Forest Regressor R² = {r2_score:.2f}]", 
                  fontsize=13, fontweight='bold', pad=15)
        plt.xlabel("Gini Importance (Relative Contribution Score)", fontsize=11)
        plt.ylabel("Macroeconomic Indicators (Features)", fontsize=11)
        plt.grid(axis='x', linestyle='--', alpha=0.5)
        plt.tight_layout()
        
        # Lưu kết quả trực tiếp vào thư mục runtime tự động của pipeline
        out_path = output_folder / 'rf_feature_importance.png'
        plt.savefig(out_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        self.logger.info(f"✓ Đã lưu file đồ thị đóng góp thuộc tính tại: {out_path}")

    def run_all_scenarios(self, output_folder: str):
        """Hàm tổng kích hoạt chuỗi kịch bản từ Pipeline"""
        out_path = Path(output_folder)
        out_path.mkdir(parents=True, exist_ok=True)
        
        self.logger.info("=" * 60)
        self.logger.info("PHASE 3: TREE-BASED MODELING & FEATURE IMPORTANCE EXPERIMENT")
        self.logger.info("=" * 60)
        
        self.run_scenario_1_no_handling()
        self.run_scenario_2_wrong_handling()
        self.run_scenario_3_correct_handling(out_path)
        
        self._plot_scenario_comparison(out_path)
        
        self.logger.info("All Tree-based Phase 3 modeling scenarios executed successfully!")

