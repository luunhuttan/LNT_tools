# 🎯 Hướng dẫn thu thập 2000 profiles Data Engineer

## Chiến lược thu thập

### Bước 1: Chạy nhiều lần với count lớn
```bash
# Lần 1: Thu thập 100 profiles đầu tiên
python main.py --industry "Data Engineer" --count 100 --api_key "..." --cx "..."

# Lần 2: Thu thập thêm 100 profiles (tự động skip trùng)
python main.py --industry "Data Engineer" --count 100 --api_key "..." --cx "..."

# Lần 3-10: Tiếp tục chạy cho đến khi có đủ 2000 profiles
python main.py --industry "Data Engineer" --count 100 --api_key "..." --cx "..."
```

### Bước 2: Kiểm tra số lượng profiles
```bash
# Đếm số profiles hiện có
Get-Content "data_collected\Data Engineer\profiles.csv" | Measure-Object -Line
```

### Bước 3: Tiếp tục chạy cho đến khi đạt mục tiêu
- Mỗi lần chạy sẽ thu thập thêm ~50-80 profiles mới (tùy độ trùng)
- Chạy ~20-40 lần để đạt 2000 profiles
- Tự động skip trùng, không lo duplicate

## Lưu ý

### Giới hạn API:
- **100 queries/ngày** (free tier)
- **~1000 profiles/ngày** (lý thuyết tối đa)
- **Thực tế:** ~200-300 profiles/ngày (an toàn)

### Timeline ước tính:
- **Ngày 1:** 100-300 profiles
- **Ngày 2-7:** 300-700 profiles
- **Ngày 8-14:** 700-1500 profiles
- **Ngày 15+:** 1500-2000 profiles

Tổng thời gian: **~2-3 tuần** để thu thập đủ 2000 profiles

## Code mới làm gì?

Code mới sử dụng **42 query variations** thay vì 1 query:
- Search theo nhiều từ khóa: Data Engineer, Senior Data Engineer, Junior Data Engineer...
- Search theo nhiều thành phố: HCMC, Hanoi, Da Nang...
- Tự động chuyển query khi không còn kết quả mới
- Lọc trùng ngay trong quá trình search

➡️ **Kết quả:** Thu thập được nhiều profiles unique hơn, không bị giới hạn bởi Google ranking!
