# 🖥️ Hệ Thống Quản Lý Bán Hàng Cửa Hàng Máy Tính

Dự án cuối kỳ môn **Kỹ thuật Lập trình (MI3010)** — Học kỳ 2, Năm học 2025-2026.

Hệ thống quản lý bán hàng dạng Console, xây dựng bằng Python thuần, tự cài đặt mọi thuật toán từ cấp độ nguyên thủy, không phụ thuộc vào thư viện xử lý file hay sắp xếp/tìm kiếm có sẵn.

---

## 📖 Mô Tả Dự Án

Trong bối cảnh một cửa hàng bán lẻ máy tính và linh kiện PC, nhu cầu về một hệ thống quản lý gọn nhẹ, đáng tin cậy và không phụ thuộc vào hạ tầng phức tạp là rất cần thiết. Hệ thống này đáp ứng các nghiệp vụ:

- **Quản lý danh mục sản phẩm**: CPU, GPU, RAM, SSD, Mainboard, PSU, Case, Cooler...
- **Lập hóa đơn bán hàng**: Kiểm tra tồn kho tự động, tính thuế VAT 8%.
- **Thống kê doanh thu**: Theo khoảng thời gian tùy chọn.

### Điểm Nổi Bật Về Mặt Kỹ Thuật

| Đặc điểm | Mô tả |
| :--- | :--- |
| 🧠 **Tự cài đặt thuật toán** | Bubble Sort, Linear Search, Substring Matching — không dùng hàm có sẵn |
| 📄 **Xử lý file thủ công** | Đọc/ghi `.txt` bằng `.split('\|')`, không dùng `json`, `csv` |
| 🔒 **Tính nguyên tử giao dịch** | Cơ chế Check-Then-Act: kiểm tra hết trước khi thực thi |
| 🛡️ **Phòng vệ đầu vào** | Validation toàn diện, bắt lỗi số âm, ký tự lạ, sai định dạng ngày |
| 🚀 **Không phụ thuộc** | Chỉ cần Python 3.7+, không cần cài thêm bất kỳ thư viện nào |

---

## 🏛 Kiến Trúc Hệ Thống

Hệ thống thiết kế theo mô hình **lập trình hướng cấu trúc (Procedural Programming)**, chia 4 module:

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                           TERMINAL CONSOLE                               │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                        TẦNG GIAO DIỆN (UI)                       │   │
│  │   main.py                 menu.py                                │   │
│  │   ┌────────────┐          ┌──────────────────────────────────┐   │   │
│  │   │ Khởi tạo   │─────────►│ Menu Chính                       │   │   │
│  │   │ Kiểm tra   │          │  ├─ Quản lý sản phẩm             │   │   │
│  │   │ file dữ liệu│         │  ├─ Quản lý bán hàng             │   │   │
│  │   └────────────┘          │  └─ Thống kê doanh thu           │   │   │
│  │                           │  + Validation (bẫy lỗi)          │   │   │
│  │                           │  + Tabular Display (dạng bảng)   │   │   │
│  │                           └──────────────┬───────────────────┘   │   │
│  └──────────────────────────────────────────┼───────────────────────┘   │
│                                             │                           │
│  ┌──────────────────────────────────────────┼───────────────────────┐   │
│  │                    TẦNG NGHIỆP VỤ (BUSINESS)                      │   │
│  │                         business.py                              │   │
│  │   ┌──────────────────────────────────────────────────────────┐   │   │
│  │   │  Thuật toán tự cài đặt:                                  │   │   │
│  │   │  • Bubble Sort (sắp xếp theo giá/tồn kho)                │   │   │
│  │   │  • Linear Search (tìm kiếm sản phẩm)                     │   │   │
│  │   │  • Substring Matching (so khớp chuỗi con thủ công)       │   │   │
│  │   │  • Check-Then-Act (lập hóa đơn an toàn)                  │   │   │
│  │   │  • Tính thuế VAT 8%                                      │   │   │
│  │   │  • Sinh mã tự động (SP001, HD001...)                     │   │   │
│  │   └──────────────────────────┬───────────────────────────────┘   │   │
│  └──────────────────────────────┼───────────────────────────────────┘   │
│                                 │                                       │
│  ┌──────────────────────────────┼───────────────────────────────────┐   │
│  │              TẦNG TRUY XUẤT DỮ LIỆU (DATA ACCESS)                │   │
│  │   models.py               file_handler.py                        │   │
│  │   ┌────────────┐        ┌───────────────────────────────────┐    │   │
│  │   │ SanPham    │        │  Đọc: .readlines() → .split('|')  │    │   │
│  │   │ HoaDon     │◄───────┤  Ghi: nối chuỗi + '|' + '\n'      │    │   │
│  │   │ (Entities) │        │  Lỗi: FileNotFoundError → seed    │    │   │
│  │   └────────────┘        └──────────────┬────────────────────┘    │   │
│  └────────────────────────────────────────┼─────────────────────────┘   │
│                                           │                             │
└───────────────────────────────────────────┼─────────────────────────────┘
                                            │
        ┌───────────────────────────────────┼───────────────────────────┐
        │                       TẦNG LƯU TRỮ BỀN VỮNG                   │
        │                                                               │
        │   ┌──────────────────────┐    ┌──────────────────────┐        │
        │   │    products.txt      │    │    invoices.txt      │        │
        │   │    SP001|Intel...    │    │    HD001|KH001|...    │        │
        │   │    SP002|AMD...      │    │    HD002|KH002|...    │        │
        │   └──────────────────────┘    └──────────────────────┘        │
        │   Định dạng: mỗi dòng 1 bản ghi, phân tách trường bằng '|'   │
        └───────────────────────────────────────────────────────────────┘


Luồng Xử Lý Một Yêu Cầu:
Người dùng chọn "Lập hóa đơn"
        │
        ▼
menu.py ──► Hiển thị danh sách sản phẩm, nhập thông tin đơn hàng
        │
        ▼
business.py ──► Kiểm tra tồn kho → Trừ kho → Tính tiền + VAT → Tạo HĐ
        │
        ▼
file_handler.py ──► Ghi đè file .txt với dữ liệu mới
        │
        ▼
menu.py ──► Hiển thị kết quả hóa đơn ra Console4

