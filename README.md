# 🛒 Hệ Thống Quản Lý Bán Hàng (Sales Management System)

Dự án cuối kỳ môn **Kỹ thuật Lập trình**. Đây là một giải pháp phần mềm quản lý bán hàng toàn diện, được thiết kế với sự chú trọng đặc biệt vào tốc độ thao tác tại quầy và tính toàn vẹn của dữ liệu giao dịch.

## 📖 Mô Tả Dự Án

Trong môi trường bán lẻ nhịp độ cao, một hệ thống chậm trễ hoặc sai sót dữ liệu có thể dẫn đến thiệt hại về doanh thu và trải nghiệm khách hàng. Nhận thức được bài toán nghiệp vụ đó, dự án này được xây dựng nhằm giải quyết hai mục tiêu cốt lõi: **Hiệu năng giao diện** và **Độ tin cậy của dữ liệu**. 

Hệ thống áp dụng triệt để mô hình kiến trúc **Client - Server**, chia tách rõ ràng giữa lớp hiển thị và lớp xử lý logic:

* **Tối ưu trải nghiệm thu ngân:** Sử dụng công nghệ Single Page Application (SPA) cho Frontend, giúp nhân viên có thể thêm món, tính tiền và chốt đơn liên tục mà không phải chờ tải lại trang.
* **Xử lý nghiệp vụ tập trung:** Backend đóng vai trò như một "bộ não" độc lập, kiểm soát chặt chẽ các logic về phân quyền (Quản lý vs. Thu ngân) và theo dõi tồn kho theo thời gian thực.
* **Bảo toàn giao dịch tài chính:** Sử dụng Hệ quản trị Cơ sở dữ liệu Quan hệ (RDBMS) tuân thủ nghiêm ngặt tiêu chuẩn ACID, đảm bảo mọi hóa đơn và dòng tiền đều được ghi nhận chính xác tuyệt đối, loại bỏ rủi ro mất mát dữ liệu khi hệ thống gặp sự cố.

---

## 🏛 Kiến Trúc Hệ Thống

```text
 ┌─────────────────────────┐         HTTP/REST (JSON)          ┌─────────────────────────┐
 │       TẦNG CLIENT       │ ◄───────────────────────────────► │       TẦNG SERVER       │
 │   (Giao diện người dùng)│                                   │    (Xử lý nghiệp vụ)    │
 │                         │                                   │                         │
 │  - Trình duyệt Web      │         1. Gửi Request API        │  - API Server           │
 │  - Quầy Thu ngân / POS  │ ─────────────────────────────────►│  - Middleware (Auth)    │
 │                         │                                   │  - Controllers          │
 │  [Công nghệ: React/Vue] │ ◄─────────────────────────────────│                         │
 └─────────────────────────┘         4. Trả về Response        └────────────┬────────────┘
                                                                            │   ▲
                                                                  2. Query  │   │ 3. Trả kết
                                                                     (SQL)  │   │    quả
                                                                            ▼   │
                                                               ┌─────────────────────────┐
                                                               │      TẦNG DATABASE      │
                                                               │      (Cơ sở dữ liệu)    │
                                                               │                         │
                                                               │  - Quản lý Hóa đơn      │
                                                               │  - Quản lý Tồn kho      │
                                                               │  - Quản lý Nhân viên    │
                                                               │                         │
                                                               │  [Công nghệ: MySQL]     │
                                                               └─────────────────────────┘

💻 Công Nghệ Sử Dụng (Tech Stack)
Dựa trên phân tích kỹ thuật, hệ thống sử dụng bộ công cụ sau:

* Frontend: TBD (ReactJS / VueJS)

* Backend: TBD (Node.js Express / Spring Boot)

* Database: RDBMS (MySQL / PostgreSQL)

Khác: JWT (Xác thực người dùng), RESTful API.
