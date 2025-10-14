# 📖 HƯỚNG DẪN SỬ DỤNG CHI TIẾT

## 🎯 Mục đích

Tài liệu này hướng dẫn chi tiết cách sử dụng chương trình giải bài toán Người du lịch (TSP) với giao diện web HTML/CSS/JS.

## 📁 Cấu trúc dự án

\`\`\`
tsp-solver/
├── index.html              # Giao diện HTML chính
├── styles.css              # File CSS riêng biệt
├── script.js               # File JavaScript riêng biệt
├── requirements.txt        # Thư viện Python cần thiết
├── README.md              # Tài liệu tổng quan
├── HUONG_DAN_SU_DUNG.md   # Hướng dẫn chi tiết (file này)
└── scripts/
    ├── server.py          # HTTP Server
    ├── tsp_backtracking.py # Thuật toán Backtracking
    └── tsp_aco.py         # Thuật toán ACO
\`\`\`

## 🚀 Bắt đầu nhanh

### 1. Cài đặt môi trường

\`\`\`bash
# Kiểm tra phiên bản Python
python --version  # Cần Python 3.8+

# Cài đặt thư viện
pip install -r requirements.txt
\`\`\`

### 2. Chạy server

\`\`\`bash
# Chạy server từ thư mục gốc
python scripts/server.py

# Hoặc chỉ định port khác (mặc định: 8000)
python scripts/server.py 3000
\`\`\`

### 3. Mở trình duyệt

Truy cập: **http://localhost:8000**

## 🖥️ Giao diện web

### Panel bên trái - Điều khiển

#### 1. Tab "Mặc định"
- Hiển thị 8 thành phố Việt Nam được sử dụng trong bài toán
- Dữ liệu mặc định: Hà Nội, Hải Phòng, Đà Nẵng, Huế, TP.HCM, Cần Thơ, Nha Trang, Đà Lạt
- Mỗi thành phố có tọa độ GPS (kinh độ, vĩ độ)

#### 2. Tab "Nhập tay"
- Cho phép thêm/sửa/xóa thành phố
- Nhập tên thành phố, kinh độ (longitude), vĩ độ (latitude)
- Nút "➕ Thêm thành phố" để thêm thành phố mới
- Nút "🗑️" để xóa thành phố (tối thiểu 3 thành phố)
- Thay đổi tự động cập nhật trực quan hóa

#### 3. Tab "File CSV"
- Upload file CSV với định dạng: `name,longitude,latitude`
- Ví dụ:
  \`\`\`
  name,longitude,latitude
  Hà Nội,105.8,21.0
  Hải Phòng,106.7,20.8
  Đà Nẵng,108.2,16.0
  \`\`\`
- Kéo thả hoặc click để chọn file
- Hiển thị thông tin file sau khi upload thành công

#### 4. Tham số thuật toán ACO

**Số lượng kiến (n_ants):**
- Mặc định: 30
- Khuyến nghị: 20-50
- Càng nhiều kiến → kết quả tốt hơn nhưng chậm hơn

**Số iterations:**
- Mặc định: 100
- Khuyến nghị: 50-200
- Càng nhiều vòng lặp → thuật toán hội tụ tốt hơn

**Alpha (α):**
- Mặc định: 1.0
- Khuyến nghị: 0.5-2.0
- Ảnh hưởng của pheromone trong quyết định

**Beta (β):**
- Mặc định: 2.0
- Khuyến nghị: 1.0-5.0
- Ảnh hưởng của khoảng cách trong quyết định

**Evaporation (ρ):**
- Mặc định: 0.5
- Khuyến nghị: 0.1-0.9
- Tốc độ bay hơi pheromone

**Q (hằng số):**
- Mặc định: 100
- Khuyến nghị: 10-1000
- Lượng pheromone được thêm vào

#### 5. Nút điều khiển

**🚀 Giải bài toán:**
- Gửi request đến server Python
- Chạy cả hai thuật toán (Backtracking và ACO)
- Hiển thị kết quả và trực quan hóa
- Thời gian chạy: 5-30 giây tùy tham số

**📊 So sánh kết quả:**
- Mở modal so sánh chi tiết
- Hiển thị bảng so sánh các tiêu chí
- Đưa ra kết luận tự động

#### 6. Kết quả

Hiển thị trong hộp kết quả:
- Tiến trình thực thi của cả hai thuật toán
- Tuyến đường tìm được
- Tổng khoảng cách (km)
- Thời gian thực thi (giây)

### Panel bên phải - Trực quan hóa

#### 1. Vị trí các thành phố (Trên trái)
- Hiển thị vị trí địa lý của các thành phố
- Tọa độ dựa trên kinh độ và vĩ độ thực tế
- Vẽ bằng HTML5 Canvas
- Cập nhật tự động khi thay đổi dữ liệu

#### 2. Kết quả Backtracking (Trên phải)
- Tuyến đường tìm được bởi Backtracking
- Màu xanh dương (#4a9eff)
- Hiển thị số thứ tự các thành phố
- Đường nối tạo thành chu trình

#### 3. Kết quả ACO (Dưới trái)
- Tuyến đường tìm được bởi ACO
- Màu đỏ (#ff6b6b)
- Hiển thị số thứ tự các thành phố
- Đường nối tạo thành chu trình

#### 4. Biểu đồ hội tụ ACO (Dưới phải)
- Theo dõi quá trình cải thiện giải pháp
- Trục X: Số iteration
- Trục Y: Khoảng cách tốt nhất tìm được
- Màu vàng (#f7d046)

## 🎮 Hướng dẫn sử dụng từng bước

### Bước 1: Khởi động server

\`\`\`bash
python scripts/server.py
\`\`\`

**Kết quả:**
\`\`\`
============================================================
🚀 TSP SOLVER SERVER
============================================================
📂 Thư mục: /path/to/project
🌐 Server đang chạy tại: http://localhost:8000
🔗 Mở trình duyệt và truy cập: http://localhost:8000
============================================================
Nhấn Ctrl+C để dừng server
\`\`\`

### Bước 2: Mở trình duyệt

1. Mở trình duyệt web (Chrome, Firefox, Safari, Edge)
2. Truy cập: **http://localhost:8000**
3. Giao diện web sẽ hiển thị với:
   - Header với tiêu đề màu vàng
   - Panel điều khiển bên trái
   - Panel trực quan hóa bên phải
   - Vị trí các thành phố đã được vẽ sẵn

### Bước 3: Điều chỉnh tham số (Tùy chọn)

Nếu muốn thử nghiệm với các tham số khác:

**Để có kết quả nhanh:**
- Số kiến: 20
- Iterations: 50

**Để có kết quả tốt nhất:**
- Số kiến: 50
- Iterations: 200
- Alpha: 1.0
- Beta: 3.0

### Bước 4: Giải bài toán

1. Nhấn nút **"🚀 Giải bài toán"**
2. Chờ indicator "Đang xử lý..." (5-30 giây)
3. Quan sát kết quả trong hộp kết quả

**Kết quả hiển thị:**
\`\`\`
==================================================
THUẬT TOÁN BACKTRACKING (simpleAI)
==================================================

Tuyến đường: Hà Nội → Hải Phòng → ... → Đà Lạt → Hà Nội
Tổng khoảng cách: 3456.78 km
Thời gian: 2.3456 giây

==================================================
THUẬT TOÁN ACO (Ant Colony Optimization)
==================================================

Iteration 10/100: Khoảng cách tốt nhất = 3500.00 km
Iteration 20/100: Khoảng cách tốt nhất = 3450.00 km
...
Tuyến đường: Hà Nội → Huế → ... → Cần Thơ → Hà Nội
Tổng khoảng cách: 3423.45 km
Thời gian: 5.6789 giây

==================================================
✅ Hoàn thành! Nhấn "So sánh kết quả" để xem chi tiết.
==================================================
\`\`\`

**Trong console server (terminal):**
\`\`\`
============================================================
Nhận được yêu cầu giải bài toán TSP
============================================================
Tham số ACO: {'n_ants': 30, 'n_iterations': 100, ...}

Đang giải bằng Backtracking...
✓ Backtracking hoàn thành: 3456.78 km trong 2.3456s

Đang giải bằng ACO...
✓ ACO hoàn thành: 3423.45 km trong 5.6789s

✅ Đã gửi kết quả về client
============================================================
\`\`\`

### Bước 5: Xem trực quan hóa

Sau khi giải xong, panel bên phải tự động cập nhật:

1. **Tuyến đường Backtracking** (màu xanh)
   - Các thành phố được đánh số theo thứ tự
   - Đường nối giữa các thành phố
   - Quay về điểm xuất phát

2. **Tuyến đường ACO** (màu đỏ)
   - Tương tự như Backtracking
   - Có thể khác hoặc giống tùy kết quả

3. **Biểu đồ hội tụ**
   - Cho thấy ACO cải thiện giải pháp qua các iteration
   - Đường đi xuống = thuật toán đang tìm được đường ngắn hơn
   - Đường ngang = thuật toán đã hội tụ

### Bước 6: So sánh kết quả

1. Nhấn nút **"📊 So sánh kết quả"**
2. Modal popup hiển thị bảng so sánh:

\`\`\`
┌─────────────────┬──────────────┬──────────┬──────────────┐
│ Tiêu chí        │ Backtracking │ ACO      │ Tốt hơn      │
├─────────────────┼──────────────┼──────────┼──────────────┤
│ Khoảng cách(km) │ 3456.78      │ 3423.45  │ ACO          │
│ Thời gian (s)   │ 2.3456       │ 5.6789   │ Backtracking │
│ Số thành phố    │ 8            │ 8        │ Bằng nhau    │
└─────────────────┴──────────────┴──────────┴──────────────┘
\`\`\`

3. Đọc kết luận tự động
4. Nhấn "Đóng" hoặc click bên ngoài để đóng modal

## 🔧 Chạy riêng từng thuật toán

### Chỉ chạy Backtracking

\`\`\`bash
python scripts/tsp_backtracking.py
\`\`\`

**Kết quả:**
\`\`\`
Thuật toán: Backtracking (simpleAI)
Tuyến đường tốt nhất: Hà Nội -> Hải Phòng -> ... -> Hà Nội
Tổng khoảng cách: 3456.78 km
Thời gian thực thi: 2.3456 giây
\`\`\`

### Chỉ chạy ACO

\`\`\`bash
python scripts/tsp_aco.py
\`\`\`

**Kết quả:**
\`\`\`
============================================================
Bắt đầu thuật toán ACO với 20 kiến, 100 iterations
============================================================

Iteration 10/100: Khoảng cách tốt nhất = 3500.00 km
Iteration 20/100: Khoảng cách tốt nhất = 3450.00 km
...

============================================================
Hoàn thành! Thời gian: 5.6789 giây
============================================================

Thuật toán: ACO (Ant Colony Optimization)
Tuyến đường tốt nhất: Hà Nội -> Huế -> ... -> Hà Nội
Tổng khoảng cách: 3423.45 km
Thời gian thực thi: 5.6789 giây
\`\`\`

## 💡 Mẹo sử dụng

### 1. Sử dụng các tab nhập liệu

**Tab "Mặc định":**
- Dùng cho demo nhanh với dữ liệu có sẵn
- Phù hợp cho bài thuyết trình

**Tab "Nhập tay":**
- Tùy chỉnh từng thành phố
- Thử nghiệm với các tọa độ khác nhau
- Thêm/bớt thành phố linh hoạt

**Tab "File CSV":**
- Nhập nhiều thành phố cùng lúc
- Dễ dàng chia sẻ dữ liệu
- Phù hợp cho bài toán lớn

### 2. Tối ưu hóa tham số ACO

**Bài toán nhỏ (n < 10):**
- Số kiến: 20
- Iterations: 50
- Alpha: 1.0, Beta: 2.0

**Bài toán trung bình (10 ≤ n ≤ 20):**
- Số kiến: 30
- Iterations: 100
- Alpha: 1.0, Beta: 3.0

**Bài toán lớn (n > 20):**
- Số kiến: 50
- Iterations: 200
- Alpha: 1.5, Beta: 2.5

### 3. Hiểu biểu đồ hội tụ

- **Giảm nhanh ban đầu:** Thuật toán đang khám phá
- **Giảm chậm dần:** Đang tinh chỉnh giải pháp
- **Nằm ngang:** Đã hội tụ (có thể tăng iterations)

### 4. So sánh thuật toán

**Backtracking tốt hơn khi:**
- Bài toán nhỏ (n < 12)
- Cần giải pháp tối ưu chắc chắn
- Có đủ thời gian chờ

**ACO tốt hơn khi:**
- Bài toán lớn (n > 15)
- Cần kết quả nhanh
- Chấp nhận giải pháp gần tối ưu

### 5. Sử dụng giao diện web

- **Responsive:** Giao diện tự động điều chỉnh theo kích thước màn hình
- **Real-time:** Kết quả cập nhật ngay khi server trả về
- **Interactive:** Click vào modal để xem chi tiết so sánh
- **Visual:** Canvas vẽ tuyến đường trực quan, dễ hiểu

## ❓ Xử lý lỗi thường gặp

### Lỗi: "No module named 'simpleai'"

**Nguyên nhân:** Chưa cài đặt thư viện simpleAI

**Giải pháp:**
\`\`\`bash
pip install simpleai==0.8.3
\`\`\`

### Lỗi: "Address already in use"

**Nguyên nhân:** Port 8000 đã được sử dụng

**Giải pháp:**
\`\`\`bash
# Sử dụng port khác
python scripts/server.py 3000

# Hoặc tìm và dừng process đang dùng port 8000
# Linux/Mac:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
\`\`\`

### Lỗi: "Connection refused" trong trình duyệt

**Nguyên nhân:** Server chưa chạy hoặc đã dừng

**Giải pháp:**
1. Kiểm tra terminal xem server có đang chạy không
2. Khởi động lại server: `python scripts/server.py`
3. Refresh trình duyệt

### Lỗi: "Internal Server Error" khi giải bài toán

**Nguyên nhân:** Lỗi trong thuật toán hoặc tham số không hợp lệ

**Giải pháp:**
1. Kiểm tra console server để xem lỗi chi tiết
2. Đảm bảo tham số hợp lệ (số dương, không quá lớn)
3. Thử với tham số mặc định

### Trình duyệt không hiển thị giao diện

**Nguyên nhân:** File index.html không tìm thấy

**Giải pháp:**
1. Đảm bảo file `index.html` ở thư mục gốc project
2. Chạy server từ thư mục gốc, không phải từ thư mục scripts
3. Kiểm tra console server xem có lỗi không

### Chương trình chạy quá lâu

**Nguyên nhân:** Tham số quá lớn hoặc bài toán phức tạp

**Giải pháp:**
- Giảm số kiến xuống 20
- Giảm iterations xuống 50
- Đợi thêm thời gian (có thể mất vài phút)
- Kiểm tra console server để xem tiến trình

### Canvas không vẽ được

**Nguyên nhân:** Trình duyệt không hỗ trợ Canvas hoặc JavaScript bị tắt

**Giải pháp:**
- Sử dụng trình duyệt hiện đại (Chrome, Firefox, Safari, Edge)
- Bật JavaScript trong trình duyệt
- Xóa cache và refresh lại trang

## 📊 Đánh giá kết quả

### Khoảng cách tốt (cho 8 thành phố mẫu)

- **Xuất sắc:** < 3400 km
- **Tốt:** 3400-3500 km
- **Trung bình:** 3500-3700 km
- **Cần cải thiện:** > 3700 km

### Thời gian chạy bình thường

- **Backtracking:** 1-5 giây
- **ACO (50 iterations):** 3-8 giây
- **ACO (100 iterations):** 5-15 giây
- **ACO (200 iterations):** 10-30 giây

## 🎓 Sử dụng cho đồ án

### Nội dung cần trình bày

1. **Giới thiệu bài toán TSP**
   - Định nghĩa
   - Ứng dụng thực tế
   - Độ phức tạp

2. **Thuật toán Backtracking**
   - Nguyên lý
   - Cài đặt với simpleAI
   - Ưu nhược điểm

3. **Thuật toán ACO**
   - Nguyên lý đàn kiến
   - Các tham số
   - Ưu nhược điểm

4. **Kiến trúc hệ thống**
   - Frontend: HTML/CSS/JS (tách riêng 3 file)
   - Backend: Python HTTP Server
   - Giao tiếp: REST API (JSON)
   - Tính toán khoảng cách: Haversine formula

5. **Tính năng nổi bật**
   - 3 phương thức nhập liệu (Mặc định, Nhập tay, CSV)
   - Trực quan hóa real-time với Canvas
   - So sánh chi tiết hai thuật toán
   - Responsive design

6. **Kết quả thực nghiệm**
   - Chạy với dữ liệu mẫu
   - Thử nghiệm với dữ liệu tùy chỉnh
   - So sánh hai thuật toán
   - Phân tích kết quả
   - Screenshot giao diện

7. **Kết luận**
   - Đánh giá
   - Hướng phát triển

### Demo trong buổi bảo vệ

1. Khởi động server
2. Mở trình duyệt và giải thích giao diện
3. Demo tab "Mặc định" với dữ liệu có sẵn
4. Giải thích các tham số ACO
5. Chạy với tham số mặc định
6. Giải thích kết quả và trực quan hóa
7. Demo tab "Nhập tay" - thêm/sửa/xóa thành phố
8. Demo tab "File CSV" - upload file
9. Thay đổi tham số và chạy lại
10. So sánh kết quả chi tiết
11. Trả lời câu hỏi

### Điểm cộng

- ✅ Giao diện web đẹp, chuyên nghiệp
- ✅ Code tách riêng HTML/CSS/JS (best practice)
- ✅ 3 phương thức nhập liệu linh hoạt
- ✅ Trực quan hóa bằng Canvas
- ✅ Không dùng framework (thuần HTML/CSS/JS + Python standard library)
- ✅ Sử dụng đúng thư viện simpleAI cho Backtracking
- ✅ Cài đặt đầy đủ ACO với 6 tham số điều chỉnh được
- ✅ So sánh chi tiết hai thuật toán
- ✅ Responsive design
- ✅ Code sạch, có comment tiếng Việt
- ✅ Tài liệu đầy đủ

## 🌐 Kiến trúc hệ thống

### Frontend

**index.html:**
- Cấu trúc HTML5 semantic
- 3 tab cho các phương thức nhập liệu khác nhau
- Form controls cho tham số thuật toán
- Canvas elements cho trực quan hóa

**styles.css:**
- Theme tối với gradient background
- Màu accent vàng (#f7d046)
- Responsive design với CSS Grid và Flexbox
- Custom scrollbar và animations
- Hover effects và transitions

**script.js:**
- Quản lý state (cities, cityCoords, results)
- Xử lý tab switching
- CRUD operations cho thành phố
- CSV file parsing
- Fetch API để gọi backend
- Canvas drawing functions
- Modal comparison display

### Backend (server.py)
- **http.server:** Server HTTP chuẩn của Python
- **JSON API:** Endpoint `/solve` nhận POST request
- **Haversine formula:** Tính khoảng cách GPS
- **Algorithm Integration:** Gọi tsp_backtracking.py và tsp_aco.py
- **CORS support:** Cho phép cross-origin requests

### Communication Flow
\`\`\`
Browser → POST /solve → Server → Run Algorithms → JSON Response → Browser
                                      ↓
                              tsp_backtracking.py
                              tsp_aco.py
\`\`\`

### Data Flow
\`\`\`
User Input (Tab) → JavaScript → JSON → Server → Distance Matrix
                                                      ↓
                                              Backtracking + ACO
                                                      ↓
                                              JSON Response
                                                      ↓
                                          Update UI + Canvas
\`\`\`

---

**Chúc bạn thành công với đồ án! 🎉**
