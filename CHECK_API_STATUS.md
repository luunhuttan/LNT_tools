# ✅ Checklist: Kích hoạt API cho tất cả keys

## Những gì bạn đang thấy:
- ✅ Custom Search API: **Enabled**
- ✅ Tab "Metrics" showing credentials filter
- ℹ️ Có thể thấy "API key 1, API key 2..." trong dropdown

## Cần kiểm tra:

### 1. Check tab "Quotas & System Limits"
Click vào tab này để xem:
- Daily quota: 100 requests/day per key
- Check xem có limit nào không

### 2. Check tab "Credentials"  
Click vào tab "Credentials" để:
- Xem tất cả API keys
- Enable API cho từng key mới
- Nếu thấy keys 2-5 chưa enable → Enable ngay

### 3. Check Metrics
Trong tab "Metrics":
- Nếu có traffic từ keys 2-5 → Good!
- Nếu chỉ có traffic từ key 1 → Cần enable keys khác

## Hướng dẫn Enable cho keys mới:

1. **Vào tab "Credentials"**
2. Click vào mỗi API key mới (keys 2-5)
3. Click "Restrictions" hoặc "Edit"
4. Trong "API restrictions" section:
   - Chọn "Restrict key"
   - Tìm và check "Custom Search API"
   - Click "Save"

Hoặc dùng cách này:
1. Vào: https://console.cloud.google.com/apis/library/customsearch.googleapis.com
2. Click "Enable" cho project của bạn
3. Làm lại cho mỗi API key

---

**Sau khi enable xong, test lại với multi-keys mode!**

