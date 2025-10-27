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
| `--api_key` | ✅ | - | Google Custom Search API key |
| `--cx` | ✅ | - | Search Engine ID (CX) |
| `--delay` | ❌ | 2.0 | Delay between requests (seconds) |
| `--append` | ❌ | False | Append to existing CSV file |

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
- To collect more: Use `--append` flag daily
- Data from public LinkedIn profiles only

---

## 🎯 Examples

```bash
# Collect Data Engineer profiles
python main.py --industry "Data Engineer" --count 100 --api_key "..." --cx "..." --append

# Collect Frontend Developer profiles
python main.py --industry "Frontend Developer" --count 50 --api_key "..." --cx "..."
```

---

## 📝 Notes

- URLs are automatically normalized (vn.linkedin.com → www.linkedin.com)
- Duplicate profiles are automatically removed
- All data is from public sources only
- Complies with LinkedIn ToS

---

**Happy collecting! 🎉**

