# Checkpoint: Stable MPV Freeze (2026-01-18)

## 📋 Trạng thái hệ thống
- **Tình trạng:** Hoàn toàn ổn định (FROZEN).
- **Core:** Quantix AI Core v1.1.
- **Frontend:** GitHub Pages (Signal Genius AI Dashboard).
- **Backend:** Railway (FastAPI).

## 🗂️ Cấu trúc File (Locked)
Hệ thống đã được đóng gói theo kiến trúc Modular Bất di bất dịch:
1. `main.py`: Entry point với 5 endpoints chuẩn (/health, /signal/latest, /signal/history, /signal/stats, /telegram/webhook).
2. `external_client.py`: Quản lý kết nối TwelveData (Crash-safe).
3. `signal_engine.py`: Logic tạo tín hiệu và fallback Stabilizer.
4. `signal_ledger.py`: Quản lý lịch sử giao dịch (In-memory).
5. `telegram_formatter.py`: Định dạng bản tin Telegram.
6. `rate_limit.py`: Chặn request > 1 lần/phút.
7. `outcome_checker.py`: Kiểm tra kết quả lệnh (Win/Loss).
8. `index.html` & `style.css`: Giao diện Glassmorphism (đã loại bỏ icon theo yêu cầu).
9. `payload.js`: Orchestration lớp Web.

## 🚀 Docker & Deployment
- **Dockerfile:** Đã tối ưu cho Railway, sử dụng `python -m uvicorn`.
- **Health Check:** `https://signalgeniusai-production.up.railway.app/health` -> OK.

## 🔒 Git Metadata
- **Commit:** `ui: remove brand logo as requested`
- **Tag:** `mpv-freeze-v1`
- **Branch:** `main`

## 🧠 Triết lý MPV (Ghi nhớ)
- MPV **KHÔNG** dùng để training hay backtest.
- MPV **CHỈ** dùng để Tracker tín hiệu Live và chứng minh thực thi (Stability).

---
*Checkpoint ghi nhận vào lúc 12:12 ngày 18-01-2026.*
