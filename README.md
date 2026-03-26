# World Bank Data Analysis Project (2004 - Present)

## 📌 Giới thiệu
Dự án này tập trung vào việc thu thập và phân tích các chỉ số kinh tế - xã hội từ World Bank API nhằm mục đích [Ví dụ: dự báo GDP hoặc phân tích tác động của giáo dục]. Dữ liệu được giới hạn từ năm 2004 đến nay để đảm bảo tính nhất quán và đầy đủ của các biến số.

## Để tránh tình trạng Data Dumping (Thu thập dữ liệu một cách mù quáng )

1. Xác định biến mục tiêu:
- GDP của mỗi quốc gia

2. Mỗi bài toán cần một không gian mẫu khác nhau 
- Bài toán phân cụm: Các biến có độ biến thiên lớn để phân tách các quốc gia 
- Bài toán hồi quy: các biến số có mối tương quan tuyến tính hoặc phi tuyến mạnh mẽ với mục tiêu 
- Chuỗi thời gian: Dữ liệu liên tục , không bị ngắt quãng

3. Việc thu thập dữ liệu thực chất đang thực hiện một một kiểm định giả thuyết thống kê (Hypothesis Testing)
 Ví dụ: Chi tiêu giáo dục (X) có tác động tích cực đến thu nhập bình quân (Y) sau một khoảng trễ n năm. 
 -> Các chỉ số World Bank có đủ để chứng minh giả thuyết đó hay không ? 


 Bài toán: Trong lịch sử, quốc gia nào đã từng trải qua trạng thái giống Việt Nam hiện tại, và sau đó họ đã phát triển như thế nào? 

 1. Data cần những indicators nào ?
 - Nhóm nội lực: Tỷ trọng công nghiệp (NV.IND.TOTL.ZS) , Tỷ trọng nông nghiệp (Tỷ trọng nông nghiệp) - Giả định rằng: Một quố gia công nghiệp hóa sẽ có quỹ đạo khác hoàn toàn quốc gia thuần nông
 - Nhóm Hội nhập: BX.KLT.DINV.WD.GD.ZS (FDI/GDP) và NE.TRD.GNFS.ZS (Độ mở thương mại). Việt Nam cực kỳ giống các "Con hổ Á Đông" ở đặc điểm này.
 - Nhóm nguồn lực: NE.GDI.FTOT.ZS (Tỷ lệ đầu tư tài sản cố định) và SE.SEC.ENRR (Tỷ lệ nhập học trung học - phản ánh chất lượng lao động cho nhà máy).
 - NY.GDP.PCAP.CD (GDP bình quân đầu người - biến này dùng để "neo" thời điểm).

 2. Tư tưởng chung:
 - Giả sử Việt Nam năm 2024, chúng ta sẽ quét ngược dòng lịch sử của các nước khác để tìm thời điểm mà bộ chỉ số của họ khớp với Việt Nam nhất
 - Toán học: f(t) ~ g(t - deltat)

3. Mô hình
- Dynamic Time Warping: So sánh độ tương đồng giữa hai chuỗi thời gian ngay cả khi chúng nhanh chậm khác nhau 

4. Mục tiêu tối ưu:
Distance = min tổng (trọng số(w) nhân trị tuyệt đối ( X việt nam - X nước nào đó))
- Việc lựa chọn là lấy giá trị absolute hay là giá trị square phụ thuộc vào việc nghiên cứu thêm nữa. 
- Trọng số w: ưu tiên giống về Công nghệ hay là giống về Dân số 

5. Kết quả đầu ra:
- Bản báo cáo định lượng:
      + Danh sách quốc  gia tham chiếu: Việt Nam tương đồng 85 % với Hàn Quốc, ...
      + Vẽ đường biểu diễn của Việt Nam đè lên đường biểu diễn lịch sử của nước tham chiếu
      + Dự báo kịch bản: Nếu Việt Nam tiếp tục đi theo quỹ đạo của Hàn Quốc: thì 10 năm tới tỷ trọng dịch vụ tăng thêm bao nhiêu phần trăm, GDP sẽ đạt ngưỡng y USD 
      * Thay đổi tư tưởng: Thay vì dự đoán cứng ngắt (sử dụng khoảng cách Euclidean) thì chúng ta sử dụng khoảng cách Mahalanobis để thực hiện tinh thần 'Scenario Coverage Optimization'
## 📊 Danh mục các chỉ số (Indicators)
Dữ liệu bao gồm các nhóm biến chính sau:

| Nhóm | Mã Chỉ Số | Tên File | Mô tả |
| :--- | :--- | :--- | :--- |
| **Kinh tế** | `NY.GDP.PCAP.CD` | `GDP_per_Capita_raw.csv` | GDP bình quân đầu người (USD). |
| **Kinh tế** | `FP.CPI.TOTL.ZG` | `Inflation_Rate_raw.csv` | Tỷ lệ lạm phát hàng năm (%). |
| **Thương mại** | `NE.TRD.GNFS.ZS` | `Trade_Openness_raw.csv` | Độ mở thương mại (% của GDP). |
| **Dân số** | `SP.POP.TOTL` | `Population_Total_raw.csv` | Tổng dân số quốc gia. |
| **Lao động** | `SL.UEM.TOTL.ZS` | `Unemployment_Rate_raw.csv` | Tỷ lệ thất nghiệp (%). |
| **Giáo dục** | `SE.PRM.CMPT.ZS` | `Learning_Outcome_raw.csv` | Tỷ lệ hoàn thành tiểu học. |

## 🛠 Cài đặt & Sử dụng
1. **Yêu cầu:** Python 3.x, thư viện `wbgapi` hoặc `pandas`.
2. **Cài đặt thư viện:**
   ```bash
   pip install wbgapi pandas matplotlib seaborn



   PHẦN 1: KẾT QUẢ "CHỤP X-QUANG" TẬP DỮ LIỆU HIỆN TẠI
1. Tính đầy đủ (Completeness) - Cảnh báo đỏ ở năm 2024

Phát hiện: Mặc dù số lượng dòng (266 quốc gia/khu vực) khớp nhau hoàn hảo ở cả 6 file, nhưng dữ liệu năm 2024 gần như là một "điểm mù".

Cột Access to electricity năm 2024 trống 100% (thiếu 266/266).

Cột Individuals using the Internet năm 2024 thiếu tới 184/266 (khoảng 70%).

Đánh giá: Nếu bạn cố đưa năm 2024 vào mô hình học máy, toàn bộ các vector đặc trưng của các quốc gia sẽ bị rỗng ở đoạn cuối, khiến việc tính toán quỹ đạo (trajectory) bị gãy.

2. Tính đa dạng & Sự phù hợp (Diversity & Relevance) - Lỗi sai cốt lõi

Phát hiện: Bài toán yêu cầu phân tích "phân bổ nhân lực" và "tỷ trọng dịch vụ", nhưng bạn không hề có 2 biến số này. Bạn đang có Điện, Internet, Nông nghiệp, Tín dụng, FDI, và GDP.

Đánh giá: Bạn không thể dùng dữ liệu Nông nghiệp hay Điện để nội suy ra tỷ trọng Dịch vụ được. Đây là lỗi sai chí mạng về nghiệp vụ (Domain Knowledge) mà Hội đồng chấm đồ án sẽ bắt lỗi ngay lập tức.

3. Tính chính xác (Accuracy) - Nhiễu cực lớn ở FDI

Phát hiện: Khi quét các điểm bất thường (Outliers - sử dụng phương pháp Interquartile Range), tôi thấy:

Biến FDI inflows có khoảng giá trị quá biến động: Nhỏ nhất là -1303, lớn nhất là 1709, với số lượng Outliers chiếm tới 11%.

Dữ liệu FDI này có thể bị bóp méo bởi các sự kiện như đại dịch, sụp đổ tài chính, hoặc các quốc gia thiên đường thuế.

Đánh giá: Nếu đưa thẳng FDI vào thuật toán tính khoảng cách (để tìm quốc gia tương đồng 85%), mô hình sẽ bị "đánh lừa" bởi các năm dòng tiền tăng/giảm đột biến, dẫn đến việc ghép sai quốc gia tham chiếu cho Việt Nam.

4. Tính nhất quán (Consistency) - Xung đột thang đo

Phát hiện: Dữ liệu Internet dao động từ 0 đến 100, nhưng GDP per capita lại nhảy từ 803 USD lên tới mức cao nhất là 174,569 USD.

Đánh giá: Các thuật toán Machine Learning (như k-NN, DTW hay K-Means) rất nhạy cảm với độ lớn của con số. Cột GDP với đơn vị hàng chục nghìn sẽ hoàn toàn lấn át và làm lu mờ tác động của cột Điện hay Internet.

PHẦN 2: THỨ TỰ ƯU TIÊN VÀ KỊCH BẢN CẢI THIỆN CHI TIẾT
Để đồ án này không bị "gãy", bạn phải thực hiện Data Preprocessing theo đúng thứ tự (Pipeline) sau đây:

ƯU TIÊN SỐ 1: Bổ sung "Linh hồn" của bộ dữ liệu (Khắc phục Tính Đa dạng)
Bạn phải tạm dừng việc xử lý code và lên trang World Bank Open Data tải ngay 2 file sau (format giống hệt 6 file bạn đang có):

Employment in services (% of total employment) - Giải quyết yêu cầu "phân bổ nhân lực".

Services, value added (% of GDP) - Giải quyết yêu cầu "tỷ trọng dịch vụ".

Hành động: Ghép (Merge) 2 file này vào tập dữ liệu cũ dựa trên khóa economy để có tổng cộng 8 chiều đặc trưng (8 features).

ƯU TIÊN SỐ 2: Cắt tỉa không gian thời gian và không gian mẫu (Khắc phục Tính Đầy đủ)
Đừng cố gắng cứu những dữ liệu rỗng. Hãy chủ động cắt bỏ để tập trung vào phần lõi chất lượng.

Bước 1 (Xóa Cột): Xóa ngay lập tức toàn bộ cột YR2024 vì dữ liệu trống quá nhiều. Giới hạn khung thời gian phân tích từ 2004 đến 2023.

Bước 2 (Lọc Dòng): Tính tỷ lệ phần trăm thiếu dữ liệu của từng quốc gia (từ 2004-2023). Đặt ngưỡng (Threshold): Những quốc gia nào bị thiếu quá 30% dữ liệu ở bất kỳ tiêu chí nào -> Xóa hẳn quốc gia đó khỏi bảng. Điều này sẽ giúp bạn loại bỏ các quốc gia quá nghèo hoặc có hệ thống thống kê yếu kém, giữ lại những nền kinh tế có số liệu minh bạch để tham chiếu cho Việt Nam.

Bước 3 (Điền khuyết - Imputation): Với những lỗ hổng nhỏ (vài năm trống rải rác ở các quốc gia giữ lại), hãy dùng thuật toán Linear Interpolation (Nội suy tuyến tính) hoặc K-Nearest Neighbors Imputer (KNN Imputer) để lấp đầy số liệu một cách mượt mà nhất.

ƯU TIÊN SỐ 3: Bóp nắn dữ liệu (Khắc phục Tính Chính xác & Nhất quán)
Trước khi chạy mô hình so sánh Việt Nam và Hàn Quốc, hãy đưa dữ liệu qua "máy ép":

Bước 1 (Xử lý Outliers cho FDI & Tín dụng): Dùng kỹ thuật Capping / Winsorization. Ví dụ: Ép tất cả các giá trị FDI nằm dưới mức -50% về thành -50%, và các giá trị trên 500% về thành 500%. Việc này giúp đường xu hướng kinh tế không bị giật cục.

Bước 2 (Đồng bộ Thang đo): Chạy toàn bộ dữ liệu (trừ cột tên quốc gia và năm) qua hàm MinMaxScaler() của thư viện Scikit-Learn. Việc này sẽ ép mọi chỉ số từ GDP (hàng nghìn) hay Internet (phần trăm) về chung một hệ quy chiếu là từ 0 đến 1. Nhờ vậy, máy tính sẽ đánh giá mức độ quan trọng của các yếu tố (Hạ tầng, Tín dụng, GDP, Nhân lực) là ngang nhau.