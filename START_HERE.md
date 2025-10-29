# 🎯 Hướng dẫn thu thập 2000 IT profiles

## Quick Start

### Cách 1: Chạy thử với count lớn (Recommended)
```bash
# Thu thập 300 profiles Data Engineer (toàn thế giới)
python main.py --industry "Data Engineer" --count 300 --api_key "YOUR_KEY" --cx "YOUR_CX"
```

### Cách 2: Chạy tất cả IT jobs tự động
```bash
# Đảm bảo API credentials đúng trong collect_it_profiles.py
python collect_it_profiles.py
```

## Chiến lược thu thập

### Phase 1: Data Engineer (Hiện có: 107)
- Chạy với count 300-500 để thu thập global
- Mục tiêu: 500+ profiles

### Phase 2: Các ngành IT khác
- Backend Engineer: 200 profiles
- Frontend Engineer: 200 profiles  
- DevOps Engineer: 200 profiles
- ML Engineer: 200 profiles
- Data Scientist: 200 profiles
- Software Engineer: 200 profiles
- Big Data Engineer: 100 profiles
- Cloud Engineer: 100 profiles
- AI Engineer: 100 profiles

**Tổng: ~2000 profiles IT**

## Lưu ý

1. **Global Search**: Code đã được cấu hình để search toàn thế giới, không chỉ VN
2. **Auto-append**: Mỗi lần chạy sẽ tự động thêm vào file cũ, bỏ qua trùng
3. **Quota API**: 100 queries/ngày → ~200-300 profiles/ngày an toàn

## Timeline

- **Tuần 1-2:** Thu thập Data Engineer (global)
- **Tuần 3-4:** Thu thập các ngành IT khác
- **Tổng thời gian:** 4-6 tuần để đạt 2000 profiles

## Các lệnh hữu ích

```bash
# Kiểm tra số profiles hiện có
Get-Content "data_collected\Data Engineer\profiles.csv" | Measure-Object -Line

# List tất cả các folders đã thu thập
dir data_collected\

# Merge tất cả IT profiles vào 1 file lớn (sẽ làm sau)
```

---

**Bắt đầu thu thập ngay:**

```bash
python main.py --industry "Data Engineer" --count 300 --api_key "AIzaSyA5tjOlmPZxbKXz9uDzvNqPO_Sco7Oq9-k" --cx "d4849e3a9180a4ea6"
```

