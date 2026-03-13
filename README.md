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