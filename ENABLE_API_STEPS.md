# 🔧 Hướng dẫn Enable Custom Search API

## Đang xem: API key 2 settings

### Thấy gì?
- ✅ "API restrictions" → **"Restrict key"** (đã check)
- ⚠️ Warning box: "This key is unrestricted"
- 📋 Dropdown: **"Select APIs"** ← Đây là nơi cần click!

### Các bước tiếp theo:

#### Bước 1: Click vào dropdown "Select APIs"
- Dropdown này nằm ngay dưới "Restrict key"
- Hiện đang hiển thị "Select APIs"

#### Bước 2: Tìm và chọn "Custom Search API"
- Sẽ hiện danh sách APIs
- Scroll tìm hoặc search "custom" hoặc "search"
- Check **"Custom Search API"**
- Click **"OK"** hoặc **"Add"**

#### Bước 3: Click nút "Save" màu xanh
- Ở góc dưới bên trái
- Wait 5 phút cho settings apply

### Làm tương tự cho Keys 3, 4, 5:
1. Repeat cho API key 3
2. Repeat cho API key 4  
3. Repeat cho API key 5

**Mẹo:** Sau khi save xong key 2, dùng menu trên để switch sang key 3, 4, 5 và làm lại.

---

## After enabling tất cả keys:

Test lại:
```bash
python main.py --industry "Data Engineer" --count 50 --cx "d4849e3a9180a4ea6" --use_multi_keys --delay 5
```

Nếu OK → Được 5 × 100 = 500 queries/ngày!
