# 🚀 Hướng dẫn trình tự push code lên GitHub

Tài liệu này hướng dẫn thứ tự lệnh chuẩn để đẩy (push) code lên GitHub, kèm mẹo xử lý khi lỡ thao tác sai thứ tự.

---

## ✅ Thứ tự chuẩn (đúng)

1) Kiểm tra thay đổi
```bash
git status
```

2) Chọn file cần đẩy (stage)
```bash
git add -A          # hoặc: git add <file1> <file2>
```

3) Tạo commit với thông điệp rõ ràng
```bash
git commit -m "mo ta ngan gon, ro rang ve thay doi"
```

4) Push lên GitHub
- Lần đầu với nhánh hiện tại (thiết lập upstream):
```bash
git push --set-upstream origin main
```
- Các lần sau (cùng nhánh):
```bash
git push
```

---

## ❓ Nếu lỡ gõ sai thứ tự (ví dụ: push → add → commit)

- Gõ `git push` trước khi `add/commit` sẽ không đẩy gì cả vì chưa có commit mới. Chỉ cần làm tiếp:
```bash
git add -A
git commit -m "them/thay doi ..."
git push
```

- Nếu Git báo "no upstream branch": dùng lệnh thiết lập upstream lần đầu:
```bash
git push --set-upstream origin <ten-nhanh>
```

---

## 🌿 Làm việc với branch (khuyến nghị theo tính năng)

- Tạo và chuyển sang nhánh mới:
```bash
git checkout -b feature/<ten-tinh-nang>
```
- Push nhánh mới lần đầu:
```bash
git push --set-upstream origin feature/<ten-tinh-nang>
```

---

## 🧩 Một số lệnh hữu ích

- Lưu tạm thay đổi, kéo code mới, rồi khôi phục thay đổi:
```bash
git stash
git pull
git stash pop
```

- Xem lịch sử commit ngắn gọn:
```bash
git log --oneline --graph --decorate --all
```

---

Mẹo: Viết thông điệp commit ngắn gọn nhưng có ý nghĩa (prefix gợi ý: `feat:`, `fix:`, `docs:`, `chore:`).


