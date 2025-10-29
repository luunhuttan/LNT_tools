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
| `--api_key` | ✅ | Google API Key |
| `--cx` | ✅ | Search Engine ID (CX) |
| `--delay` | ❌ | Delay giữa requests (mặc định: 2s) |
| `--overwrite` | ❌ | Ghi đè file CSV cũ (mặc định: append và lọc trùng) |

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

- **Free tier:** 100 queries/ngày
- **Mỗi query:** Tối đa 10 results
- **Tổng:** ~100 profiles/ngày

### Phạm vi tìm kiếm

- Tool chỉ tìm profiles **tại Việt Nam**
- Sử dụng từ khóa "Vietnam" hoặc "Viet Nam"
- Nguồn: LinkedIn profiles công khai

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

