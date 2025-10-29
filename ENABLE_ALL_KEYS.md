# ✅ Enable Custom Search API cho Keys 2-5

## Vấn đề:
- ✅ Key 1: Đang hoạt động
- ❌ Keys 2-5: Chưa enable Custom Search API → 403 error

## Giải pháp nhanh:

### Cách 1: Check trong Google Cloud Console
1. Vào: https://console.cloud.google.com/apis/credentials
2. Click vào **API key 2**
3. Check:
   - "API restrictions" → "Restrict key" được check chưa?
   - "Selected APIs" có "Custom Search API" chưa?
4. Nếu chưa → làm như hướng dẫn trước

### Cách 2: Check thông qua Metrics tab
1. Vào: https://console.cloud.google.com/apis/api/customsearch.googleapis.com/metrics
2. Filter by "Credentials" 
3. Xem keys nào có traffic:
   - Có traffic → OK
   - Không có traffic → Chưa enable

### Cách 3: Test từng key riêng lẻ
```bash
# Test key 1
python main.py --industry "Data Engineer" --count 50 --api_key "AIzaSyA5tjOlmPZxbKXz9uDzvNqPO_Sco7Oq9-k" --cx "d4849e3a9180a4ea6"

# Test key 2  
python main.py --industry "Data Engineer" --count 50 --api_key "AIzaSyDwGdCTCPx2N03PoBYCGBPoPdMuBLNXGhU" --cx "d4849e3a9180a4ea6"
```

---

## Khuyến nghị:
**Check lại Google Cloud Console xem Keys 2-5 đã enable Custom Search API chưa!**

Sau khi enable → script sẽ tự động rotate và hoạt động tốt!

