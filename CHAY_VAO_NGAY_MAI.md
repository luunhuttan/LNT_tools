# 🚀 Lệnh chạy vào ngày mai

## Khi nào chạy?
**00:00 UTC** (khoảng **7-8h sáng** giờ Việt Nam)
- Quota reset lúc này
- Có thể chạy sớm hơn (6h30-7h) để tránh người khác dùng quota

## Lệnh chạy:

### Lần 1 (Sáng - dùng 500 queries):
```bash
python main.py --industry "Data Engineer" --count 500 --cx "d4849e3a9180a4ea6" --use_multi_keys --delay 5
```

**Kết quả mong đợi:**
- 500 queries → tự động rotate 5 keys
- ~500-700 profiles mới
- Tổng: ~700-900 profiles

### Lần 2 (Chiều - thêm 500 queries):
```bash
python main.py --industry "Data Engineer" --count 500 --cx "d4849e3a9180a4ea6" --use_multi_keys --delay 5
```

**Kết quả mong đợi:**
- ~300-500 profiles mới (một số trùng)
- Tổng: ~1000-1400 profiles

### Ngày kia (Lần 3 - final):
```bash
python main.py --industry "Data Engineer" --count 500 --cx "d4849e3a9180a4ea6" --use_multi_keys --delay 5
```

**Kết quả cuối:**
- **~1500-2000+ profiles** ✨

---

## 💡 Tips:

### Delay nên dùng bao nhiêu?
- **5 giây**: An toàn, ít rate limit
- **3 giây**: Nhanh hơn, có thể bị rate limit đôi chút

### Count nên bao nhiêu?
- **500**: Dùng hết quota 1 ngày
- **300**: An toàn hơn, để dự phòng

### Tại sao chạy nhiều lần?
- Key rotation sẽ tự động
- Mỗi lần chạy thêm được profiles mới
- Tránh trùng lặp nhờ hệ thống lọc duplicate

---

## ✅ Checklist trước khi chạy:

- [ ] Chờ đến ngày mai (7-8h sáng)
- [ ] Quota đã reset
- [ ] File `.api_keys_multi.txt` có đủ 5 keys
- [ ] Sẵn sàng!

**Good luck! 🎉**

