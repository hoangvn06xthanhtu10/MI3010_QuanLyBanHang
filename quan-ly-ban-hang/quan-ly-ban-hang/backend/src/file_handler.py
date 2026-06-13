"""
Module: file_handler.py
Mô tả: Xử lý đọc/ghi file text thủ công, không dùng thư viện json/csv.
Tự động tạo dữ liệu mầm (seed data) nếu file không tồn tại.
"""

import os
from models import SanPham, HoaDon

# Hằng số cấu hình đường dẫn file
THU_MUC_HIEN_TAI = os.path.dirname(os.path.abspath(__file__))

# 2. Lùi ra 2 cấp (từ src -> backend -> quan-ly-ban-hang)
THU_MUC_GOC = os.path.abspath(os.path.join(THU_MUC_HIEN_TAI, "..", ".."))

# 3. Trỏ cứng vào thư mục database
PRODUCTS_FILE = os.path.join(THU_MUC_GOC, "database", "products.txt")
INVOICES_FILE = os.path.join(THU_MUC_GOC, "database", "invoices.txt")
DELIMITER = "|"

def tao_du_lieu_mam_san_pham():
    """Tạo dữ liệu mẫu cho file products.txt nếu chưa tồn tại"""
    # Dữ liệu mầm: ma_sp|ten_san_pham|danh_muc|gia_ban|ton_kho
    du_lieu_mau = [
        "SP001|Intel Core i9-13900K|CPU|12500000|15",
        "SP002|AMD Ryzen 7 7800X3D|CPU|9500000|20",
        "SP003|NVIDIA RTX 4090|GPU|42000000|8",
        "SP004|AMD Radeon RX 7900 XTX|GPU|25000000|12",
        "SP005|Corsair Vengeance DDR5 32GB|RAM|3200000|30",
        "SP006|Samsung 990 Pro 2TB NVMe|SSD|4500000|25",
        "SP007|ASUS ROG MAXIMUS Z790|Mainboard|11000000|10",
        "SP008|Corsair RM1000x 1000W|PSU|4200000|18",
        "SP009|NZXT H7 Flow|Case|2500000|22",
        "SP010|Noctua NH-D15|Cooler|2200000|16"
    ]
    
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        for dong in du_lieu_mau:
            f.write(dong + '\n')
    print(f"[HỆ THỐNG] Đã tạo file {PRODUCTS_FILE} với dữ liệu mẫu.")

def tao_du_lieu_mam_hoa_don():
    """Tạo file invoices.txt rỗng nếu chưa tồn tại"""
    with open(INVOICES_FILE, 'w', encoding='utf-8') as f:
        f.write("")  # Tạo file rỗng
    print(f"[HỆ THỐNG] Đã tạo file {INVOICES_FILE}.")

def doc_danh_sach_san_pham():
    """
    Đọc file products.txt, phân tách thủ công bằng split('|'),
    trả về list các đối tượng SanPham.
    """
    danh_sach = []
    try:
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            cac_dong = f.readlines()
        
        for dong in cac_dong:
            dong = dong.strip()
            if dong == "":
                continue
            # Phân tách chuỗi thủ công bằng dấu '|'
            truong = dong.split(DELIMITER)
            if len(truong) >= 5:
                sp = SanPham(
                    ma_sp=truong[0],
                    ten=truong[1],
                    danh_muc=truong[2],
                    gia_ban=float(truong[3]),
                    ton_kho=int(truong[4])
                )
                danh_sach.append(sp)
    except FileNotFoundError:
        print(f"[CẢNH BÁO] File {PRODUCTS_FILE} không tồn tại. Đang tạo mới...")
        tao_du_lieu_mam_san_pham()
        return doc_danh_sach_san_pham()  # Gọi đệ quy sau khi tạo file
    return danh_sach

def doc_danh_sach_hoa_don():
    """
    Đọc file invoices.txt, phân tách thủ công bằng split('|'),
    trả về list các đối tượng HoaDon.
    """
    danh_sach = []
    try:
        with open(INVOICES_FILE, 'r', encoding='utf-8') as f:
            cac_dong = f.readlines()
        
        for dong in cac_dong:
            dong = dong.strip()
            if dong == "":
                continue
            truong = dong.split(DELIMITER)
            if len(truong) >= 7:
                hd = HoaDon(
                    ma_hd=truong[0],
                    ma_kh=truong[1],
                    ngay_lap=truong[2],
                    tong_tien_hang=float(truong[3]),
                    thue_vat=float(truong[4]),
                    tong_thanh_toan=float(truong[5]),
                    chi_tiet_mua=truong[6]
                )
                danh_sach.append(hd)
    except FileNotFoundError:
        print(f"[CẢNH BÁO] File {INVOICES_FILE} không tồn tại. Đang tạo mới...")
        tao_du_lieu_mam_hoa_don()
        return doc_danh_sach_hoa_don()
    return danh_sach

def ghi_danh_sach_san_pham(danh_sach):
    """
    Ghi toàn bộ danh sách sản phẩm từ bộ nhớ xuống file.
    Định dạng: ma_sp|ten_san_pham|danh_muc|gia_ban|ton_kho
    """
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        for sp in danh_sach:
            dong = f"{sp.ma_sp}{DELIMITER}{sp.ten}{DELIMITER}{sp.danh_muc}{DELIMITER}{sp.gia_ban}{DELIMITER}{sp.ton_kho}\n"
            f.write(dong)
    print(f"[FILE] Đã đồng bộ {len(danh_sach)} sản phẩm xuống {PRODUCTS_FILE}")

def ghi_danh_sach_hoa_don(danh_sach):
    """
    Ghi toàn bộ danh sách hóa đơn từ bộ nhớ xuống file.
    Định dạng: ma_hd|ma_kh|ngay_lap|tong_tien_hang|thue_vat|tong_thanh_toan|chi_tiet_mua
    """
    with open(INVOICES_FILE, 'w', encoding='utf-8') as f:
        for hd in danh_sach:
            dong = f"{hd.ma_hd}{DELIMITER}{hd.ma_kh}{DELIMITER}{hd.ngay_lap}{DELIMITER}{hd.tong_tien_hang}{DELIMITER}{hd.thue_vat}{DELIMITER}{hd.tong_thanh_toan}{DELIMITER}{hd.chi_tiet_mua}\n"
            f.write(dong)
    print(f"[FILE] Đã đồng bộ {len(danh_sach)} hóa đơn xuống {INVOICES_FILE}")