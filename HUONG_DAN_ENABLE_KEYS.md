# 🔧 Hướng dẫn Enable API Keys 2-5

## Bước 1: Vào Google Cloud Console

1. Truy cập: https://console.cloud.google.com/apis/credentials
2. Đăng nhập nếu chưa

## Bước 2: Enable cho API Key 2

### 2.1. Click vào "API key 2"
- Trong danh sách API keys
- Click vào dòng "API key 2" (hoặc tên khác bạn đặt)

### 2.2. Tìm phần "API restrictions"
- Scroll xuống phần "API restrictions"
- Sẽ thấy 2 options:
  - ⚪ "Don't restrict key" (hiện đang check)
  - ⚫ **"Restrict key"** ← Chọn cái này!

### 2.3. Enable "Restrict key"
- Click vào radio button **"Restrict key"**
- Sẽ hiện dropdown "Select APIs"

### 2.4. Chọn Custom Search API
- Click vào dropdown **"Select APIs"**
- Scroll hoặc search "custom" hoặc "search"
- Tìm **"Custom Search API"** trong danh sách
- ✅ Click checkbox để chọn
- Click **"OK"** hoặc **"Add"**

### 2.5. Save
- Scroll xuống dưới
- Click nút **"Save"** màu xanh
- Đợi message "Saved successfully"

## Bước 3: Làm tương tự cho Key 3

### 3.1. Back về list keys
- Click **"← Back"** hoặc menu trên cùng
- Về danh sách credentials

### 3.2. Click vào "API key 3"
### 3.3. Repeat bước 2.2 - 2.5
- Enable "Restrict key"
- Chọn "Custom Search API"
- Save

## Bước 4: Làm tương tự cho Key 4

- Back về list
- Click "API key 4"
- Enable "Restrict key"
- Chọn "Custom Search API"
- Save

## Bước 5: Làm tương tự cho Key 5

- Back về list
- Click "API key 5"
- Enable "Restrict key"
- Chọn "Custom Search API"
- Save

---

## Checklist cuối:

Sau khi xong, check lại:

1. Vào: https://console.cloud.google.com/apis/api/customsearch.googleapis.com/metrics
2. Click tab "Credentials"
3. Xem tất cả 5 keys đều có trong danh sách
4. Hoặc filter "Credentials" trong Metrics tab
5. Xem keys nào có traffic (có traffic = enable thành công)

---

## Sau khi enable xong:

**Test ngay:**
```bash
python main.py --industry "Data Engineer" --count 50 --cx "d4849e3a9180a4ea6" --use_multi_keys --delay 5
```

**Nếu OK → Chạy full:**
```bash
python main.py --industry "Data Engineer" --count 500 --cx "d4849e3a9180a4ea6" --use_multi_keys --delay 5
```

---

## ⚠️ Lưu ý:

### Key 1 (API key 1):
- Hiện là "Don't restrict key" 
- Vẫn hoạt động tốt
- Có thể giữ nguyên hoặc restrict (tùy bạn)

### Thời gian apply:
- Sau khi Save → Wait 5 phút
- Settings mới có hiệu lực

### Verify:
- Enable xong → check lại Metrics
- Nếu có traffic = enable thành công!

