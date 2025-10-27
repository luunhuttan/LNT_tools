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

### Lệnh cơ bản

```bash
python main.py --industry "TÊN_NGÀNH" --count SỐ_LƯỢNG --api_key "API_KEY" --cx "CX"
```

### Ví dụ

```bash
# Thu thập 50 profiles Data Engineer tại Việt Nam
python main.py --industry "Data Engineer" --count 50 --api_key "AIzaSy..." --cx "d4849e3a9180a4ea6"
```

### Tham số

| Tham số | Bắt buộc | Mô tả |
|---------|----------|-------|
| `--industry` | ✅ | Tên ngành nghề (VD: "Data Engineer", "Frontend Developer") |
| `--count` | ❌ | Số lượng profiles (mặc định: 20) |
| `--api_key` | ✅ | Google API Key |
| `--cx` | ✅ | Search Engine ID (CX) |
| `--delay` | ❌ | Delay giữa requests (mặc định: 2s) |
| `--append` | ❌ | Thêm vào file CSV có sẵn (không ghi đè) |

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

### Thu thập Data Engineer
```bash
python main.py --industry "Data Engineer" --count 100 --api_key "YOUR_KEY" --cx "YOUR_CX"
```

### Thu thập Frontend Developer
```bash
python main.py --industry "Frontend Developer" --count 30 --api_key "YOUR_KEY" --cx "YOUR_CX"
```

### Thu thập Marketing Manager
```bash
python main.py --industry "Marketing Manager" --count 50 --api_key "YOUR_KEY" --cx "YOUR_CX"
```

### Thu thập nhiều ngày (append vào file có sẵn)
```bash
# Ngày 1: Tạo file mới
python main.py --industry "Data Engineer" --count 100 --api_key "..." --cx "..."

# Ngày 2-10: Thêm vào file
python main.py --industry "Data Engineer" --count 100 --api_key "..." --cx "..." --append
```
**Lưu ý:** Flag `--append` tự động loại trùng profiles dựa trên URL. Có thể chạy nhiều ngày để thu thập nhiều profiles.

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

