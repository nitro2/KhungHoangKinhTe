# Công Cụ Mô Phỏng và Phân Tích Chu Kỳ Khủng Hoảng Kinh Tế

## 🎯 Giới Thiệu

Đây là một công cụ phân tích và mô phỏng tiên tiến các chu kỳ khủng hoảng kinh tế, được phát triển để hiểu sâu về các nguyên nhân, quy luật và mô hình lặp lại của các cuộc khủng hoảng kinh tế trong lịch sử. Công cụ sử dụng Python để tạo ra các biểu đồ trực quan hóa chu kỳ kinh tế dựa trên dữ liệu lịch sử từ NBER (National Bureau of Economic Research) và các nguồn dữ liệu quốc tế.

## ✨ Tính Năng Chính

- **📊 Mô phỏng 6 chu kỳ nguyên nhân chính** gây ra khủng hoảng kinh tế
- **📈 Hiển thị trực quan khoảng thời gian** của suy thoái và khủng hoảng
- **🎨 Phân biệt màu sắc rõ ràng**: Suy thoái (xanh dương) và Khủng hoảng (đỏ)
- **📅 Dữ liệu lịch sử đầy đủ** từ 1929 đến hiện tại
- **🔍 Tạo biểu đồ SVG** có thể phóng to và xem chi tiết
- **⚙️ Phân tích tổng hợp** các yếu tố tác động đồng thời
- **🔮 Dự báo xu hướng** dựa trên các chu kỳ lịch sử

## 📈 Các Chu Kỳ Được Phân Tích

### Chu Kỳ Chính (Primary Cycles)

| Chu Kỳ | Thời Gian (năm) | Trọng Số | Mô Tả |
|---------|-----------------|----------|-------|
| 🏦 **Tín dụng** | 14.0 | 1.00 | Chu kỳ cho vay và tín dụng ngân hàng |
| 🏠 **Bất động sản** | 18.0 | 0.90 | Chu kỳ thị trường nhà đất và bất động sản |
| 📈 **Kinh doanh–tồn kho** | 4.0 | 0.55 | Chu kỳ kinh doanh và quản lý tồn kho |
| 💰 **Lãi suất/thanh khoản** | 6.0 | 0.80 | Chu kỳ chính sách tiền tệ và thanh khoản |
| 🌍 **Đô la/toàn cầu hóa vốn** | 8.0 | 0.70 | Chu kỳ đồng đô la và dòng vốn toàn cầu |


### Chu Kỳ Phụ (Secondary Cycles)

| Chu Kỳ | Thời Gian (năm) | Trọng Số | Mô Tả |
|---------|-----------------|----------|-------|
| 👥 **Nhân khẩu học/đổi mới CN** | 45.0 | 0.65 | Chu kỳ dân số và cách mạng công nghiệp |
| 📊 **Chứng khoán** | 9.0 | 0.60 | Chu kỳ thị trường chứng khoán |

## 🛠️ Cài Đặt và Sử Dụng

### Yêu Cầu Hệ Thống
- **Python**: 3.7 trở lên
- **pip3**: Trình quản lý gói Python

### Cài Đặt Dependencies

```bash
pip3 install -r requirements.txt
```

### Chạy Công Cụ

```bash
python3 generate_graph.py
```

### Dependencies

```
numpy>=1.21.0      # Tính toán số học và mảng
pandas>=1.3.0      # Thao tác dữ liệu và chuỗi thời gian
matplotlib>=3.5.0  # Vẽ biểu đồ và trực quan hóa
```

## 📊 Phương Pháp Hiển Thị

### Biểu Đồ 1: Chu Kỳ Chính + Suy Thoái + Khủng Hoảng

#### 🔴 Khủng hoảng (Crisis)
- **Vị trí**: Đoạn thẳng nằm ngang tại y = 1.1
- **Màu sắc**: Đỏ
- **Độ dày**: 4 pixels
- **Độ dài tối thiểu**: 1 năm
- **Nhãn**: Hiển thị ở giữa đoạn thẳng

#### 🔵 Suy thoái (Recession)
- **Vị trí**: Đoạn thẳng nằm ngang tại y = 1.2
- **Màu sắc**: Xanh dương
- **Độ dày**: 4 pixels
- **Độ dài tối thiểu**: 1 năm
- **Nhãn**: Hiển thị ở giữa đoạn thẳng

### Biểu Đồ 2: Chu Kỳ Phụ + Sự Kiện Toàn Cầu

#### ⚫ Sự Kiện Chiến Tranh/Thiên Tai
- **Vị trí**: Đường thẳng đứng
- **Màu sắc**: Đen
- **Độ dày**: 0.9 pixels
- **Nhãn**: Xoay 90° theo đường thẳng

## 📈 Dữ liệu Đầu Vào

### 1. Chu Kỳ Kinh Tế (`du_lieu_chu_ky_kinh_te.csv`)

Dữ liệu mô phỏng các chu kỳ kinh tế từ 2020-2035 với giá trị chuẩn hóa:

| Năm | Chu_Ky_Tin_Dung | Chu_Ky_Bat_Dong_San | Chu_Ky_Chung_Khoan | Chu_Ky_Chien_Tranh | Chu_Ky_Nang_Luong | Chu_Ky_Thien_Tai |
|-----|------------------|---------------------|---------------------|---------------------|-------------------|------------------|
| 2020 | -0.85 | 0.45 | -0.92 | -0.15 | 0.35 | -0.75 |
| 2021 | -0.42 | 0.78 | -0.31 | 0.25 | 0.67 | -0.12 |
| 2022 | 0.23 | 0.89 | 0.45 | 0.78 | 0.95 | 0.34 |
| 2023 | 0.71 | 0.34 | 0.87 | 0.12 | 0.23 | 0.89 |
| 2024 | 0.95 | -0.12 | 0.65 | -0.45 | -0.34 | 0.45 |

**📊 Giải thích các giá trị:**
- **Phạm vi**: -1.0 đến +1.0 (chuẩn hóa)
- **Giá trị âm**: Giai đoạn suy giảm/khủng hoảng
- **Giá trị dương**: Giai đoạn tăng trưởng/phục hồi
- **Giá trị gần 0**: Giai đoạn ổn định

### 2. Dữ Liệu Suy Thoái (NBER, Mỹ)

**Các giai đoạn suy thoái được mã hóa trong `generate_graph.py`:**

| Thời Gian | Tên Suy Thoái |
|-----------|---------------|
| 1929-08 → 1933-03 | Đại Suy thoái 1929–33 |
| 1937-05 → 1938-06 | Suy thoái 1937–38 |
| 1945-02 → 1945-10 | Suy thoái 1945 (hậu chiến) |
| 1948-11 → 1949-10 | Suy thoái 1948–49 |
| 1953-07 → 1954-05 | Suy thoái 1953–54 |
| 1957-08 → 1958-04 | Suy thoái 1957–58 |
| 1960-04 → 1961-02 | Suy thoái 1960–61 |
| 1969-12 → 1970-11 | Suy thoái 1969–70 |
| 1973-11 → 1975-03 | Suy thoái 1973–75 (dầu mỏ) |
| 1980-01 → 1980-07 | Suy thoái 1980 |
| 1981-07 → 1982-11 | Suy thoái 1981–82 |
| 1990-07 → 1991-03 | Suy thoái 1990–91 |
| 2001-03 → 2001-11 | Suy thoái 2001 (dot-com) |
| 2007-12 → 2009-06 | Khủng hoảng 2007–09 |
| 2020-02 → 2020-04 | COVID-19 2020 |

### 3. Dữ Liệu Khủng Hoảng Lớn

**Các giai đoạn khủng hoảng nghiêm trọng:**

| Thời Gian | Tên Khủng Hoảng |
|-----------|-----------------|
| 1929-10 → 1933-03 | Đại Khủng hoảng 1929–33 |
| 1973-10 → 1975-03 | Khủng hoảng dầu mỏ 1973–75 |
| 1979-01 → 1982-12 | Sốc dầu lần 2 & thắt chặt 1979–82 |
| 1982-08 → 1983-12 | Khủng hoảng nợ Mỹ Latinh 1982–83 |
| 1997-07 → 1998-12 | Khủng hoảng châu Á 1997–98 |
| 2000-03 → 2002-12 | Vỡ bong bóng dot-com 2000–02 |
| 2007-08 → 2009-06 | Khủng hoảng tài chính toàn cầu 2007–09 |
| 2010-01 → 2012-12 | Khủng hoảng nợ Eurozone 2010–12 |
| 2020-02 → 2020-12 | Sốc COVID-19 2020 |
| 2022-01 → 2023-12 | Lạm phát toàn cầu & siết tiền tệ 2022–23 |

### 4. Sự Kiện Toàn Cầu (`SuKien_ChienTranh_ThienTai_ToanCau.csv`)

Dữ liệu 23 sự kiện lớn từ 1939-2022 bao gồm:

**🌍 Sự kiện Chiến tranh/Chính trị:**
- WWII 1939–45, Korean War 1950–53, Vietnam War
- Oil embargo 1973–74, Nixon Shock 1971–73
- Gulf War 1990–91, 9/11 (2001), Iraq War 2003–11
- Arab Spring 2011–12, Russia–Ukraine 2022–

**🌪️ Sự kiện Thiên tai/Đại dịch:**
- Asian Flu 1957–58, Hong Kong Flu 1968–70
- SARS 2003, Tsunami 2004, Iceland ash 2010
- Tohoku 2011, Thailand floods 2011
- Ebola 2014–16, COVID-19 2020–

## 📈 Kết Quả Đầu Ra

### Biểu Đồ Được Tạo Ra

1. **`BieuDo_1_ChuKyChinh.svg`** - Chu kỳ chính + Đoạn ngang suy thoái (xanh) + Đoạn ngang khủng hoảng (đỏ)
2. **`BieuDo_2_ChuKyPhu.svg`** - Chu kỳ phụ + Đường thẳng đứng sự kiện chiến tranh/thiên tai

### Đặc Điểm Biểu Đồ

- **📏 Định dạng**: SVG (Vector graphics) có thể phóng to vô hạn
- **🎨 Màu sắc**: Phân biệt rõ ràng từng loại sự kiện
- **📊 Thang đo**: Y-axis từ -1.1 đến 1.4 để hiển thị đầy đủ
- **📅 Thời gian**: X-axis từ 1925 đến 2035
- **🏷️ Nhãn**: Tự động gắn nhãn cho mỗi sự kiện

## 🔬 Phương Pháp Luận

### Mô Hình Toán Học

Công cụ sử dụng mô hình sóng sin để mô phỏng các chu kỳ:

```python
# Công thức cơ bản cho mỗi chu kỳ
series = sin(2π × (t / period) + phase)

# Tổng hợp các chu kỳ
composite = Σ(weight × series)

# Chuẩn hóa kết quả
normalized = composite / max(|composite|)
```

**Trong đó:**
- `t`: Thời gian (năm)
- `period`: Chu kỳ của từng yếu tố (năm)
- `phase`: Độ lệch pha (radians)
- `weight`: Trọng số ảnh hưởng (0-1)

### Thuật Toán Phát Hiện Đỉnh

```python
# Điều kiện phát hiện đỉnh khủng hoảng
if (composite[i-1] < composite[i] > composite[i+1]) and \
   (composite[i] >= threshold_85_percentile):
    peak_detected = True
```

### Xử Lý Khoảng Thời Gian

```python
# Đảm bảo độ dài tối thiểu 1 năm
if (end_date - start_date).days < 365:
    end_date = start_date + DateOffset(years=1)
```

## 🎯 Ứng Dụng Thực Tế

### 📊 Phân Tích Tài Chính
- **Đánh giá rủi ro**: Xác suất khủng hoảng trong tương lai
- **Timing đầu tư**: Xác định thời điểm tối ưu cho quyết định đầu tư
- **Quản lý danh mục**: Điều chỉnh tài sản theo chu kỳ

### 🏛️ Hoạch Định Chính Sách
- **Chính sách vĩ mô**: Hỗ trợ ngân hàng trung ương
- **Dự báo**: Chuẩn bị cho các kịch bản khủng hoảng
- **Phản ứng**: Thiết kế biện pháp ứng phó kịp thời

### 🎓 Giáo Dục và Nghiên Cứu
- **Giảng dạy**: Minh họa chu kỳ kinh tế cho sinh viên
- **Nghiên cứu**: Phân tích mối quan hệ giữa các yếu tố
- **Xuất bản**: Tạo biểu đồ cho báo cáo và bài viết

## ⚠️ Lưu Ý Quan Trọng

> **🚨 Disclaimer**: Đây là công cụ mô phỏng dựa trên dữ liệu lịch sử và mô hình toán học. Kết quả chỉ mang tính chất tham khảo và **KHÔNG NÊN** được sử dụng làm cơ sở duy nhất cho các quyết định đầu tư hoặc chính sách quan trọng.

### Giới Hạn của Mô Hình
- **Dữ liệu lịch sử**: Quá khứ không đảm bảo tương lai
- **Mô hình đơn giản**: Thực tế phức tạp hơn nhiều
- **Yếu tố ngẫu nhiên**: Không thể dự đoán sự kiện bất ngờ
- **Bối cảnh thay đổi**: Kinh tế toàn cầu liên tục biến đổi

## 📄 Giấy Phép

Dự án này được phát hành dưới **Giấy phép MIT** cho mục đích giáo dục, nghiên cứu và phi lợi nhuận.
