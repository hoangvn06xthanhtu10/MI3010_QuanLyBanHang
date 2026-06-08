"""
=============================================================
  DATA GENERATOR - Hệ Thống Quản Lý Bán Hàng
  Sinh dữ liệu giả lập: Khách hàng, Sản phẩm, Nhân viên,
  Hóa đơn & Chi tiết hóa đơn
=============================================================
"""

import random
import json
import csv
import os
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
#  CÀI ĐẶT
# ─────────────────────────────────────────────
NUM_CUSTOMERS   = 200
NUM_PRODUCTS    = 60
NUM_EMPLOYEES   = 15
NUM_INVOICES    = 500
OUTPUT_DIR      = "generated_data"

# ─────────────────────────────────────────────
#  DỮ LIỆU GỐC TIẾNG VIỆT
# ─────────────────────────────────────────────
HO = [
    "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan",
    "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương",
    "Lý", "Đinh", "Tô", "Tống", "Trịnh",
]
TEN_DEM_NAM  = ["Văn", "Hữu", "Đức", "Minh", "Quốc", "Anh", "Trung", "Bảo"]
TEN_DEM_NU   = ["Thị", "Thu", "Thùy", "Ngọc", "Kim", "Bích", "Hồng", "Lan"]
TEN_CHINH_NAM = [
    "An", "Bình", "Cường", "Dũng", "Hùng", "Khang", "Long",
    "Minh", "Nam", "Phúc", "Quân", "Sơn", "Tài", "Tuấn",
    "Vinh", "Khoa", "Đạt", "Hải", "Lâm", "Quang",
]
TEN_CHINH_NU = [
    "Anh", "Châu", "Diệu", "Giang", "Hương", "Lan", "Linh",
    "Mai", "Ngân", "Nhung", "Phương", "Thảo", "Trang", "Uyên",
    "Vi", "Yến", "Hà", "Ly", "Nhi", "Quỳnh",
]

TINH_THANH = [
    "Hà Nội", "TP. Hồ Chí Minh", "Đà Nẵng", "Hải Phòng",
    "Cần Thơ", "Bình Dương", "Đồng Nai", "Khánh Hòa",
    "Nghệ An", "Thanh Hóa", "Bắc Ninh", "Hải Dương",
    "Thừa Thiên Huế", "Quảng Ninh", "Long An",
]

LOAI_DUONG = ["Đường", "Phố", "Ngõ", "Hẻm", "Ngách"]
TEN_DUONG  = [
    "Lê Lợi", "Nguyễn Huệ", "Trần Phú", "Đinh Tiên Hoàng",
    "Lý Thường Kiệt", "Hoàng Diệu", "Võ Thị Sáu", "Bà Triệu",
    "Phan Chu Trinh", "Ngô Quyền", "Hai Bà Trưng", "Đinh Bộ Lĩnh",
]

HANG_SAN_PHAM = {
    "Đồ uống":    ["Cà phê đen", "Cà phê sữa", "Trà đào", "Nước cam", "Sinh tố bơ",
                   "Trà sữa trân châu", "Nước chanh", "Soda chanh leo"],
    "Thực phẩm":  ["Bánh mì thịt", "Xôi gà", "Phở bò", "Bún bò", "Cơm gà",
                   "Bánh cuốn", "Cháo sườn", "Mì Quảng"],
    "Đồ ăn vặt":  ["Khoai tây chiên", "Bánh tráng trộn", "Chả giò", "Nem chua",
                   "Bánh flan", "Chè đậu đỏ", "Kem que"],
    "Điện thoại": ["iPhone 15", "Samsung Galaxy A55", "Xiaomi 14T", "OPPO Reno12",
                   "Vivo V30", "Realme 12 Pro"],
    "Phụ kiện":   ["Ốp lưng điện thoại", "Tai nghe không dây", "Cáp sạc USB-C",
                   "Pin dự phòng 10000mAh", "Giá đỡ điện thoại", "Kính cường lực"],
}

CHUC_VU = ["Thu ngân", "Quản lý", "Nhân viên kho", "Trưởng ca"]
PHUONG_THUC_TT = ["Tiền mặt", "Chuyển khoản", "Thẻ tín dụng", "Ví điện tử"]
TRANG_THAI_HD  = ["Hoàn thành", "Đã hủy", "Đang xử lý"]


# ─────────────────────────────────────────────
#  HÀM TIỆN ÍCH
# ─────────────────────────────────────────────
def random_phone() -> str:
    prefixes = ["032", "033", "034", "035", "036", "037", "038", "039",
                "086", "096", "097", "098", "070", "076", "077", "078", "079"]
    return random.choice(prefixes) + "".join(str(random.randint(0, 9)) for _ in range(7))


def random_email(ho: str, ten: str, idx: int) -> str:
    import unicodedata, re
    def remove_accent(text):
        text = unicodedata.normalize("NFD", text)
        text = "".join(c for c in text if unicodedata.category(c) != "Mn")
        return re.sub(r"[^a-zA-Z0-9]", "", text).lower()
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
    return f"{remove_accent(ten)}.{remove_accent(ho)}{idx}@{random.choice(domains)}"


def random_address() -> str:
    so_nha = random.randint(1, 999)
    return f"{so_nha} {random.choice(LOAI_DUONG)} {random.choice(TEN_DUONG)}, {random.choice(TINH_THANH)}"


def random_name(gender: str = None) -> tuple[str, str]:
    """Trả về (ho_ten_dem, ten_chinh)"""
    if gender is None:
        gender = random.choice(["nam", "nu"])
    ho = random.choice(HO)
    if gender == "nam":
        dem  = random.choice(TEN_DEM_NAM)
        ten  = random.choice(TEN_CHINH_NAM)
    else:
        dem  = random.choice(TEN_DEM_NU)
        ten  = random.choice(TEN_CHINH_NU)
    return f"{ho} {dem}", ten


def random_dob(min_age=18, max_age=65) -> str:
    days_back = random.randint(min_age * 365, max_age * 365)
    return (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")


def random_date_in_range(start_year=2023) -> str:
    start = datetime(start_year, 1, 1)
    delta = datetime.now() - start
    rand_days = random.randint(0, delta.days)
    return (start + timedelta(days=rand_days)).strftime("%Y-%m-%d %H:%M:%S")


# ─────────────────────────────────────────────
#  SINH DỮ LIỆU
# ─────────────────────────────────────────────
def generate_customers(n: int) -> list[dict]:
    customers = []
    for i in range(1, n + 1):
        gender = random.choice(["nam", "nu"])
        ho_dem, ten = random_name(gender)
        ho_ten = f"{ho_dem} {ten}"
        customers.append({
            "customer_id":   i,
            "ho_ten":        ho_ten,
            "gioi_tinh":     "Nam" if gender == "nam" else "Nữ",
            "ngay_sinh":     random_dob(),
            "so_dien_thoai": random_phone(),
            "email":         random_email(ho_dem.split()[0], ten, i),
            "dia_chi":       random_address(),
            "ngay_tao":      random_date_in_range(2022),
            "hang_thanh_vien": random.choice(["Thường", "Bạc", "Vàng", "Kim cương"]),
            "diem_tich_luy": random.randint(0, 5000),
        })
    return customers


def generate_products(n: int) -> list[dict]:
    products = []
    pid = 1
    categories = list(HANG_SAN_PHAM.keys())
    # Đảm bảo ít nhất 1 sản phẩm mỗi loại
    for cat, items in HANG_SAN_PHAM.items():
        for item in items:
            gia_nhap = round(random.uniform(5_000, 500_000), -3)
            he_so_lai = random.uniform(1.2, 2.5)
            products.append({
                "product_id":    pid,
                "ten_san_pham":  item,
                "danh_muc":      cat,
                "gia_nhap":      int(gia_nhap),
                "gia_ban":       int(gia_nhap * he_so_lai / 1000) * 1000,
                "don_vi":        "cái" if cat in ["Điện thoại", "Phụ kiện"] else "phần",
                "ton_kho":       random.randint(0, 500),
                "mo_ta":         f"Sản phẩm {item} chất lượng cao",
                "trang_thai":    random.choice(["Đang bán", "Đang bán", "Ngừng bán"]),
                "ngay_nhap":     random_date_in_range(2022),
            })
            pid += 1
            if pid > n:
                break
        if pid > n:
            break
    # Bổ sung nếu chưa đủ
    while pid <= n:
        cat  = random.choice(categories)
        items = HANG_SAN_PHAM[cat]
        item = random.choice(items) + f" #{pid}"
        gia_nhap = round(random.uniform(5_000, 500_000), -3)
        he_so_lai = random.uniform(1.2, 2.5)
        products.append({
            "product_id":    pid,
            "ten_san_pham":  item,
            "danh_muc":      cat,
            "gia_nhap":      int(gia_nhap),
            "gia_ban":       int(gia_nhap * he_so_lai / 1000) * 1000,
            "don_vi":        "cái" if cat in ["Điện thoại", "Phụ kiện"] else "phần",
            "ton_kho":       random.randint(0, 500),
            "mo_ta":         f"Sản phẩm {item} chất lượng cao",
            "trang_thai":    random.choice(["Đang bán", "Đang bán", "Ngừng bán"]),
            "ngay_nhap":     random_date_in_range(2022),
        })
        pid += 1
    return products


def generate_employees(n: int) -> list[dict]:
    employees = []
    chuc_vu_list = ["Quản lý"] + [random.choice(["Thu ngân", "Nhân viên kho", "Trưởng ca"]) for _ in range(n - 1)]
    random.shuffle(chuc_vu_list)
    for i in range(1, n + 1):
        gender = random.choice(["nam", "nu"])
        ho_dem, ten = random_name(gender)
        ho_ten = f"{ho_dem} {ten}"
        luong_base = {
            "Quản lý": random.randint(12_000_000, 20_000_000),
            "Trưởng ca": random.randint(8_000_000, 12_000_000),
            "Thu ngân": random.randint(6_000_000, 9_000_000),
            "Nhân viên kho": random.randint(6_000_000, 8_000_000),
        }
        cv = chuc_vu_list[i - 1]
        employees.append({
            "employee_id":   i,
            "ho_ten":        ho_ten,
            "gioi_tinh":     "Nam" if gender == "nam" else "Nữ",
            "ngay_sinh":     random_dob(22, 50),
            "so_dien_thoai": random_phone(),
            "email":         random_email(ho_dem.split()[0], ten, 1000 + i),
            "dia_chi":       random_address(),
            "chuc_vu":       cv,
            "luong":         luong_base[cv],
            "ngay_vao_lam":  random_date_in_range(2020),
            "trang_thai":    random.choice(["Đang làm", "Đang làm", "Đang làm", "Nghỉ việc"]),
        })
    return employees


def generate_invoices_and_details(
    customers: list[dict],
    products: list[dict],
    employees: list[dict],
    n: int,
) -> tuple[list[dict], list[dict]]:
    invoices = []
    details  = []
    detail_id = 1
    active_emp = [e for e in employees if e["trang_thai"] == "Đang làm"]
    active_pro = [p for p in products if p["trang_thai"] == "Đang bán"]

    for i in range(1, n + 1):
        khach = random.choice(customers)
        nv    = random.choice(active_emp)
        ngay  = random_date_in_range(2023)
        status = random.choices(
            TRANG_THAI_HD,
            weights=[75, 15, 10],
        )[0]

        # Chi tiết hóa đơn: 1–6 dòng
        so_dong = random.randint(1, 6)
        ds_sp = random.sample(active_pro, min(so_dong, len(active_pro)))
        tong_tien = 0
        invoice_details = []
        for sp in ds_sp:
            so_luong   = random.randint(1, 10)
            don_gia    = sp["gia_ban"]
            thanh_tien = so_luong * don_gia
            giam_gia   = random.choice([0, 0, 0, 5, 10, 15])  # % giảm giá
            thanh_tien_sau_giam = int(thanh_tien * (1 - giam_gia / 100))
            tong_tien += thanh_tien_sau_giam
            invoice_details.append({
                "detail_id":    detail_id,
                "invoice_id":   i,
                "product_id":   sp["product_id"],
                "ten_san_pham": sp["ten_san_pham"],
                "so_luong":     so_luong,
                "don_gia":      don_gia,
                "giam_gia_pct": giam_gia,
                "thanh_tien":   thanh_tien_sau_giam,
            })
            detail_id += 1

        vat     = round(tong_tien * 0.08)
        tong_tt = tong_tien + vat

        invoices.append({
            "invoice_id":       i,
            "customer_id":      khach["customer_id"],
            "ten_khach_hang":   khach["ho_ten"],
            "employee_id":      nv["employee_id"],
            "ten_nhan_vien":    nv["ho_ten"],
            "ngay_lap":         ngay,
            "tong_tien_hang":   tong_tien,
            "thue_vat_8pct":    vat,
            "tong_thanh_toan":  tong_tt,
            "phuong_thuc_tt":   random.choice(PHUONG_THUC_TT),
            "trang_thai":       status,
            "ghi_chu":          random.choice(["", "", "", "Khách VIP", "Giao hàng tận nơi"]),
        })
        details.extend(invoice_details)

    return invoices, details


# ─────────────────────────────────────────────
#  XUẤT FILE
# ─────────────────────────────────────────────
def save_csv(data: list[dict], filename: str):
    if not data:
        return
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"  ✅  {filename:<40} → {len(data):>5} bản ghi")


def save_json(data: list[dict], filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✅  {filename:<40} → {len(data):>5} bản ghi")


def save_sql_insert(data: list[dict], table: str, filename: str):
    """Sinh file SQL INSERT cho từng bảng."""
    if not data:
        return
    path = os.path.join(OUTPUT_DIR, filename)
    cols = list(data[0].keys())
    col_str = ", ".join(f"`{c}`" for c in cols)

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"-- Auto-generated INSERT statements for `{table}`\n")
        f.write(f"-- Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"INSERT INTO `{table}` ({col_str}) VALUES\n")
        rows = []
        for row in data:
            vals = []
            for v in row.values():
                if v is None:
                    vals.append("NULL")
                elif isinstance(v, (int, float)):
                    vals.append(str(v))
                else:
                    safe = str(v).replace("'", "''")
                    vals.append(f"'{safe}'")
            rows.append("  (" + ", ".join(vals) + ")")
        f.write(",\n".join(rows) + ";\n")
    print(f"  ✅  {filename:<40} → {len(data):>5} bản ghi")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    random.seed(42)          # Cố định seed → kết quả tái lập được
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("\n" + "=" * 60)
    print("   DATA GENERATOR — Hệ Thống Quản Lý Bán Hàng")
    print("=" * 60)

    print("\n📦  Đang sinh dữ liệu...")
    customers          = generate_customers(NUM_CUSTOMERS)
    products           = generate_products(NUM_PRODUCTS)
    employees          = generate_employees(NUM_EMPLOYEES)
    invoices, details  = generate_invoices_and_details(
        customers, products, employees, NUM_INVOICES
    )

    print("\n💾  Đang xuất CSV...")
    save_csv(customers, "customers.csv")
    save_csv(products,  "products.csv")
    save_csv(employees, "employees.csv")
    save_csv(invoices,  "invoices.csv")
    save_csv(details,   "invoice_details.csv")

    print("\n🔵  Đang xuất JSON...")
    save_json(customers, "customers.json")
    save_json(products,  "products.json")
    save_json(employees, "employees.json")
    save_json(invoices,  "invoices.json")
    save_json(details,   "invoice_details.json")

    print("\n🗄️   Đang xuất SQL INSERT...")
    save_sql_insert(customers, "customers",       "customers.sql")
    save_sql_insert(products,  "products",        "products.sql")
    save_sql_insert(employees, "employees",       "employees.sql")
    save_sql_insert(invoices,  "invoices",        "invoices.sql")
    save_sql_insert(details,   "invoice_details", "invoice_details.sql")

    # ── Thống kê nhanh ──
    total_revenue = sum(
        inv["tong_thanh_toan"]
        for inv in invoices
        if inv["trang_thai"] == "Hoàn thành"
    )
    print("\n" + "─" * 60)
    print("📊  THỐNG KÊ DỮ LIỆU ĐÃ SINH")
    print("─" * 60)
    print(f"  Khách hàng   : {len(customers):>6}")
    print(f"  Sản phẩm     : {len(products):>6}")
    print(f"  Nhân viên    : {len(employees):>6}")
    print(f"  Hóa đơn      : {len(invoices):>6}")
    print(f"  Chi tiết HD  : {len(details):>6}")
    print(f"  Doanh thu TT : {total_revenue:>15,.0f} VNĐ")
    print("─" * 60)
    print(f"\n✅  Tất cả file đã được lưu tại: ./{OUTPUT_DIR}/\n")


if __name__ == "__main__":
    main()