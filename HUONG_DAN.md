# 📖 HƯỚNG DẪN SỬ DỤNG CV COLLECTOR

## 🎯 Mục đích

Tool tự động thu thập thông tin CV/Profile từ LinkedIn của các chuyên gia **tại Việt Nam** theo ngành nghề, lưu dưới dạng CSV.

---

## ⚙️ Yêu cầu

1. **Python 3.11+**
2. **Google API Credentials:**
   - API Key từ Google Cloud Console
   - Search Engine ID (CX) từ Custom Search Engine

---

## 📦 Cài đặt

### 1. Cài dependencies
```bash
pip install -r requirements.txt
```

### 2. Lấy Google API Credentials

#### A. API Key (từ Google Cloud Console)

1. Truy cập: https://console.cloud.google.com/
2. Tạo project mới (nếu chưa có)
3. Bật **Custom Search API**
4. Tạo **API Key**:
   - Vào **APIs & Services** → **Credentials**
   - Click **"CREATE CREDENTIALS"** → **"API Key"**
   - Copy API Key (chỉ hiện 1 lần!)

#### B. Search Engine ID / CX

1. Truy cập: https://programmablesearchengine.google.com/
2. Tạo Search Engine mới:
   - Sites to search: **Để trống**
   - Name: "CV Collector"
   - Click **"CREATE"**
3. Lấy **Search Engine ID (CX)** từ trang setup

---

## 🚀 Cách sử dụng

### ⚡ Cách chạy đơn giản

**Lệnh chạy bình thường (tự động lưu vào file cũ):**
```bash
python main.py --industry "Data Engineer" --count 50 --api_key "YOUR_API_KEY" --cx "YOUR_CX"
```

**Lần 1:** Tạo file mới → `data_collected/Data Engineer/profiles.csv` (50 profiles)  
**Lần 2:** Chạy lại cùng lệnh → Tự động thêm profiles mới vào file cũ (bỏ qua trùng lặp)  
**Lần 3+:** Chạy thêm nhiều lần → Data tích lũy thêm, không bị trùng

📌 **Quan trọng:** Mặc định chương trình tự động lưu vào file cũ, không cần thêm flag gì!

**Chỉ dùng flag `--overwrite` khi muốn xóa file cũ và tạo lại:**
```bash
python main.py --industry "Data Engineer" --count 50 --api_key "..." --cx "..." --overwrite
```

---

### 📋 Lệnh cơ bản

```bash
python main.py --industry "TÊN_NGÀNH" --count SỐ_LƯỢNG --api_key "API_KEY" --cx "CX"
```

### 📝 Ví dụ nhanh

```bash
# Thu thập 50 profiles Data Engineer tại Việt Nam
python main.py --industry "Data Engineer" --count 50 --api_key "AIzaSy..." --cx "d4849e3a9180a4ea6"
```

### 📊 Tham số

| Tham số | Bắt buộc | Mô tả |
|---------|----------|-------|
| `--industry` | ✅ | Tên ngành nghề (VD: "Data Engineer", "Frontend Developer") |
| `--count` | ❌ | Số lượng profiles (mặc định: 20) |
| `--api_key` | ⚠️ | Google API Key (bắt buộc nếu không dùng `--use_multi_keys`) |
| `--cx` | ✅ | Search Engine ID (CX) |
| `--delay` | ❌ | Delay giữa requests (mặc định: 2s) |
| `--overwrite` | ❌ | Ghi đè file CSV cũ (mặc định: append và lọc trùng) |
| `--use_multi_keys` | ❌ | Dùng nhiều API keys từ file `.api_keys_multi.txt` (khuyến nghị) |

### 🔑 Chế độ Multi-API Keys (Khuyến nghị)

**Ưu điểm:**
- Tăng quota: 5 keys = 500 queries/ngày
- Tự động rotate khi bị rate limit
- Thu thập nhanh hơn: 500-1000 profiles/ngày

**Cách setup:**

1) Tạo file `.api_keys_multi.txt` tại thư mục gốc project theo 1 trong 2 chế độ sau:

- Chế độ ghép cặp API Key ↔ CX (khuyến nghị, không cần truyền `--cx` khi chạy):
  ```
  API_KEY_1=your_api_key_1
  CX_1=your_cx_1
  API_KEY_2=your_api_key_2
  CX_2=your_cx_2
  # (tiếp tục API_KEY_3/CX_3 nếu có)
  ```

- Chế độ nhiều API Key dùng chung 1 CX (cần truyền `--cx` khi chạy):
  ```
  API_KEY_1=your_api_key_1
  API_KEY_2=your_api_key_2
  # (tiếp tục API_KEY_3 nếu có)
  ```

2) Enable Custom Search API cho tất cả API Keys trong Google Cloud Console.

3) Cách chạy với multi-keys:

- Nếu dùng GHÉP CẶP key↔CX trong file (không cần `--cx`):
  ```bash
  python main.py --industry "Data Engineer" --count 500 --use_multi_keys --delay 5
  ```

- Nếu dùng nhiều API Key CHUNG 1 CX (truyền `--cx`):
  ```bash
  python main.py --industry "Data Engineer" --count 500 --cx "YOUR_CX" --use_multi_keys --delay 5
  ```

4) (Tuỳ chọn) Tạo file mẫu nhanh:
   ```bash
   python -c "from utils.multi_api_key import *; create_api_keys_file()"
   # Điền API keys (và CX nếu muốn ghép cặp), sau đó lưu thành .api_keys_multi.txt
   ```

**So sánh:**

| Mode | Single Key | Multi-keys (5 keys) |
|------|------------|---------------------|
| Quota/ngày | 100 queries | 500 queries |
| Profiles/ngày | ~100-200 | ~500-1000 |
| Rotation | ❌ | ✅ Auto |
| Time to 2000 profiles | 10-15 ngày | 2-3 ngày |

---

## 📊 Output

### File CSV được lưu tại:

```
data_collected/{Tên ngành}/profiles.csv
```

### Cấu trúc CSV:

| Cột | Mô tả |
|-----|-------|
| Name | Tên người |
| Title | Chức danh |
| Location | Vị trí địa lý |
| About | Mô tả |
| Experience | Kinh nghiệm |
| Education | Học vấn |
| Skills | Kỹ năng |
| URL | Link LinkedIn profile |

---

## ⚠️ Lưu ý

### 🆕 Tính năng mới: Tự động lọc trùng Profile

- ✅ **Mặc định:** Append mode - tự động thêm profiles mới vào file CSV cũ
- ✅ **Tự động lọc trùng** dựa trên URL (không bị duplicate)
- ✅ **An toàn:** Chạy nhiều lần sẽ tích lũy data, không gây trùng lặp
- ✅ **Thông minh:** Tự động skip profiles đã có trong file

**Ví dụ:**
```bash
# Lần 1: Thu thập 50 profiles
python main.py --industry "Data Engineer" --count 50 ...

# Lần 2: Thu thập thêm 50 profiles nữa
# → Tự động merge vào file cũ, bỏ qua trùng lặp
# → File có ~80-100 profiles (không phải 100 vì có 10-20 profiles trùng)
python main.py --industry "Data Engineer" --count 50 ...
```

### Giới hạn API

📊 **Free Tier (mặc định):**
- **100 queries/ngày**
- **Mỗi query:** Tối đa 10 results
- **Tổng lý thuyết:** ~1000 profiles/ngày (100 queries × 10 results)
- **Thời gian chạy:** ~200 giây (3-4 phút) cho 100 queries (với delay 2s)

💡 **Thực tế sử dụng:**
- **Thu thập 50 profiles:** ~10 queries, ~20 giây
- **Thu thập 100 profiles:** ~10-20 queries, ~40 giây  
- **Tối đa 1 ngày:** 100-150 profiles (an toàn, tránh hết quota)
- **Nếu dùng hết quota:** ~1000 profiles/ngày (nhưng không nên dùng hết!)

⚠️ **Lưu ý:** 
- Nên chạy nhiều lần trong ngày với số lượng nhỏ (20-50 profiles/lần)
- Chạy vài lần trong tuần để tích lũy data dần dần
- Không nên chạy quá nhiều cùng lúc để tránh hết quota

### Phạm vi tìm kiếm

- Tool chỉ tìm profiles **tại Việt Nam**
- Sử dụng từ khóa "Vietnam" hoặc "Viet Nam"
- Nguồn: LinkedIn profiles công khai

### ⚠️ Tại sao không có profile mới khi chạy nhiều lần?

**Đây là hành vi ĐÚNG của hệ thống:**
1. Google Search trả về kết quả theo **relevance** (độ liên quan), không random
2. Mỗi lần chạy cùng industry → Google trả về **cùng các profiles**
3. Tính năng lọc trùng tự động **skip profiles đã có** → Số lượng không tăng
4. Đây là điều **tốt** - đảm bảo không bị trùng dữ liệu!

**💡 Giải pháp để thu thập thêm profiles:**

1. **Chạy với industry/từ khóa khác:**
   ```bash
   python main.py --industry "Big Data Engineer" --count 50 ...
   python main.py --industry "Cloud Data Engineer" --count 50 ...
   python main.py --industry "Senior Data Engineer" --count 50 ...
   ```

2. **Chạy với ngành nghề khác hoàn toàn:**
   ```bash
   python main.py --industry "Frontend Developer" --count 50 ...
   python main.py --industry "Backend Developer" --count 50 ...
   ```

3. **Chấp nhận rằng đã thu thập đủ profiles cho ngành đó ở Việt Nam**
   - Thị trường VN có hạn → không thể thu thập vô hạn
   - 100 profiles cho "Data Engineer" ở VN là khá đủ

### Privacy & Ethics

- ✅ Chỉ thu thập data công khai
- ✅ Từ Google Search snippets
- ✅ Không scrape trực tiếp từ LinkedIn
- ✅ Tuân thủ LinkedIn ToS

---

## 🔍 Ví dụ sử dụng

### ✅ Ví dụ 1: Thu thập Data Engineer (chạy 1 lần)
```bash
python main.py --industry "Data Engineer" --count 50 --api_key "YOUR_KEY" --cx "YOUR_CX"
```
➡️ **Kết quả:** Tạo file mới với 50 profiles

### ✅ Ví dụ 2: Thu thập nhiều lần (data tích lũy)
```bash
# Lần 1: Tạo file mới
python main.py --industry "Data Engineer" --count 50 --api_key "..." --cx "..."

# Lần 2: Thêm vào file cũ (không cần flag gì!)
python main.py --industry "Data Engineer" --count 50 --api_key "..." --cx "..."

# Lần 3: Thêm vào file cũ
python main.py --industry "Data Engineer" --count 50 --api_key "..." --cx "..."
```
➡️ **Kết quả:** File có ~120-140 profiles (tùy số trùng)

💡 **Giải thích:** 
- Mỗi lần chạy sẽ thêm profiles mới vào file cũ
- Tự động lọc trùng dựa trên URL
- Có thể chạy nhiều lần để thu thập nhiều data hơn

### ✅ Ví dụ 3: Thu thập ngành khác

**Frontend Developer:**
```bash
python main.py --industry "Frontend Developer" --count 30 --api_key "YOUR_KEY" --cx "YOUR_CX"
```

**Marketing Manager:**
```bash
python main.py --industry "Marketing Manager" --count 50 --api_key "YOUR_KEY" --cx "YOUR_CX"
```

### ⚠️ Ví dụ 4: Ghi đè file cũ (dùng khi muốn bắt đầu lại)

**Dùng flag `--overwrite` để xóa file cũ và tạo lại:**
```bash
python main.py --industry "Data Engineer" --count 50 --api_key "..." --cx "..." --overwrite
```
➡️ **Kết quả:** Xóa file cũ, tạo file mới với 50 profiles

⛔ **Lưu ý:** Chỉ dùng khi muốn xóa data cũ và bắt đầu lại từ đầu!

---

## 📁 Cấu trúc Project

```
D:\tools\
├── main.py                 # Script chính
├── requirements.txt        # Dependencies
├── .gitignore             # Git ignore
│
├── utils/
│   ├── __init__.py
│   ├── search_google.py  # Google Search API
│   ├── parser.py          # Parse data
│   └── writer.py          # Write CSV
│
└── data_collected/       # Output folder (tự động tạo)
    └── {Industry}/
        └── profiles.csv
```

---

## 🛠️ Troubleshooting

### Lỗi: "Rate limit exceeded"
- **Giải pháp:** Tăng `--delay` (VD: `--delay 5`)

### Lỗi: "No results found"
- **Nguyên nhân:** Có thể không tìm thấy profiles ở Việt Nam cho ngành đó
- **Giải pháp:** Thử ngành khác hoặc bỏ filter "Vietnam"

### Lỗi: "API key invalid"
- **Giải pháp:** Kiểm tra lại API Key và đảm bảo Custom Search API đã enabled

---

## 📞 Support

Nếu gặp vấn đề:
1. Kiểm tra API credentials còn hoạt động
2. Verify Google Cloud Console project
3. Check daily quota (100 queries/ngày)

---

## 📝 Credits

Built with:
- `google-api-python-client` - Google Custom Search API
- `pandas` - Data processing
- `tqdm` - Progress bar
- `beautifulsoup4` - HTML parsing

---

**Happy collecting! 🎯**

## 🧰 Git - Cách sử dụng cơ bản

### 1) Clone dự án về máy
```bash
# HTTPS
git clone https://github.com/<username>/<repo>.git

# Hoặc SSH
git clone git@github.com:<username>/<repo>.git
```

### 2) Cấu hình Git (1 lần trên mỗi máy)
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### 3) Kiểm tra thay đổi, thêm file và commit
```bash
git status
git add -A
git commit -m "your commit message"
```

### 4) Push lần đầu (thiết lập upstream)
```bash
git push --set-upstream origin main
```

### 5) Push các lần sau
```bash
git push
```

### 6) Kéo cập nhật mới nhất về máy
```bash
git pull
```

### 7) Làm việc với branch
```bash
# Tạo và chuyển sang nhánh mới
git checkout -b feature/my-change

# Push nhánh mới lần đầu
git push --set-upstream origin feature/my-change

# Sau đó chỉ cần
git push
```

### 8) Lưu tạm thay đổi (tuỳ chọn)
```bash
git stash           # lưu tạm thời
git pull            # cập nhật code mới
git stash pop       # lấy lại thay đổi
```

Ghi chú:
- Lần đầu push qua HTTPS, Git có thể yêu cầu GitHub Personal Access Token (PAT) thay cho mật khẩu.
- Nếu dùng SSH, hãy cấu hình SSH key trước trong tài khoản GitHub.

### 9) Trình tự chuẩn để push code (nhanh gọn)
```bash
# 1) Kiểm tra thay đổi
git status

# 2) Chọn file để đẩy lên (stage)
git add -A
# 2.1) Nếu add toàn bộ file thì sử dụng
git add .

# 3) Tạo commit
git commit -m "mo ta ngan gon, ro rang ve thay doi"

# 4) Push
# Lần đầu nhánh hiện tại:
git push --set-upstream origin main
# Các lần sau:
git push
```

Nếu lỡ gõ nhầm thứ tự (ví dụ: push → add → commit): chỉ cần tiếp tục `git add -A && git commit -m "..." && git push`.