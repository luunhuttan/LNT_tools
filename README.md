# 🚀 CV Collector - Thu thập CV/Profile từ LinkedIn

Tool tự động thu thập thông tin CV/Profile từ LinkedIn của các chuyên gia **tại Việt Nam** theo ngành nghề, lưu dưới dạng CSV.

---

## ✨ Tính năng

- ✅ Thu thập profiles từ LinkedIn công khai
- ✅ Tự động filter theo ngành nghề và vị trí địa lý
- ✅ Tự động normalize URLs (vn.linkedin.com → www.linkedin.com)
- ✅ Append mode để collect nhiều ngày
- ✅ Tự động loại trùng dựa trên URL
- ✅ Export CSV với UTF-8-SIG encoding (mở được Excel)

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run tool
```bash
python main.py --industry "Data Engineer" --count 50 --api_key "YOUR_API_KEY" --cx "YOUR_CX"
```

### 3. Output
```
data_collected/Data Engineer/profiles.csv
```

---

## 📋 Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--industry` | ✅ | - | Industry name (e.g., "Data Engineer") |
| `--count` | ❌ | 20 | Number of profiles to collect |
| `--api_key` | ⚠️ | - | Google Custom Search API key (optional if using `--use_multi_keys`) |
| `--cx` | ⚠️ | - | Search Engine ID (CX). Optional when `CX_n` pairs exist in `.api_keys_multi.txt` |
| `--delay` | ❌ | 2.0 | Delay between requests (seconds) |
| `--overwrite` | ❌ | False | Overwrite existing CSV instead of appending (default is append) |
| `--use_multi_keys` | ❌ | False | Use multi key/CX rotation from `.api_keys_multi.txt` |

---

## 📖 Documentation

- **Full guide:** See `HUONG_DAN.md`
- **Setup API:** Follow instructions in `HUONG_DAN.md`

---

## 📊 Output Format

CSV file contains:
- Name
- Title
- Location
- About
- Experience
- Education
- Skills
- URL

---

## ⚠️ Limitations

- Free tier: 100 queries/day
- To collect more: Run multiple times (default appends new profiles). Use `--overwrite` to start fresh
- Data from public LinkedIn profiles only

---

## 🎯 Examples

```bash
# Collect Data Engineer profiles
python main.py --industry "Data Engineer" --count 100 --api_key "..." --cx "..."

# Collect Frontend Developer profiles
python main.py --industry "Frontend Developer" --count 50 --api_key "..." --cx "..."
```

### Multi-keys with paired CX (recommended)

```bash
python main.py --industry "Data Engineer" --count 200 --use_multi_keys --delay 3
```

Ensure `.api_keys_multi.txt` contains pairs:
```
API_KEY_1=your_key_1
CX_1=your_cx_1
API_KEY_2=your_key_2
CX_2=your_cx_2
```

---

## 📝 Notes

- URLs are automatically normalized (vn.linkedin.com → www.linkedin.com)
- Duplicate profiles are automatically removed
- All data is from public sources only
- Complies with LinkedIn ToS

---

**Happy collecting! 🎉**

