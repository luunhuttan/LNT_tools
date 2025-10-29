# ✅ Final Steps: Complete API Setup

## Current Status:
✅ API Key 2: Custom Search API enabled and ready to save

## Next Actions:

### 1. Click "Save" button
- Blue button at bottom left
- Wait for confirmation message

### 2. Enable for Keys 3, 4, 5
- Navigate to each key (use menu/back button)
- Repeat same steps:
  - Click "Edit" 
  - Select "Restrict key"
  - Click "Select APIs" dropdown
  - Check "Custom Search API"
  - Click "Save"

### 3. Verify All Keys
After saving all keys, you should have:
- ✅ API Key 1 (already had quota)
- ✅ API Key 2 (just enabled)  
- ✅ API Key 3 (to enable)
- ✅ API Key 4 (to enable)
- ✅ API Key 5 (to enable)

**Total quota: 5 × 100 = 500 queries/day!**

---

## After All Keys Enabled:

Test with count 50 to verify:
```bash
python main.py --industry "Data Engineer" --count 50 --cx "d4849e3a9180a4ea6" --use_multi_keys --delay 5
```

Then run full collection:
```bash
python main.py --industry "Data Engineer" --count 500 --cx "d4849e3a9180a4ea6" --use_multi_keys --delay 5
```

Expected result: **500+ new profiles in a single run!**

