"""
Module: menu.py (CHƯƠNG TRÌNH CHÍNH)
Mô tả: Giao diện Console đa cấp với đầy đủ chức năng.
Có validation bắt lỗi đầu vào, hiển thị dạng bảng (tabular display).
"""
import sys
import os

# 1. BẮC CẦU TỪ FRONTEND SANG BACKEND
# Lấy vị trí file hiện tại (frontend/src/menu.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Lùi ra 2 cấp (src -> frontend -> thư mục gốc), sau đó chui vào thư mục backend
backend_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "backend", "src"))

# Đưa backend vào danh sách hệ thống để Python có thể tìm thấy models, business,...
sys.path.insert(0, backend_dir)

# ==========================================
# 2. SAU KHI BẮC CẦU XONG MỚI BẮT ĐẦU IMPORT
# ==========================================
from models import SanPham, HoaDon
from file_handler import (doc_danh_sach_san_pham, doc_danh_sach_hoa_don, 
                          ghi_danh_sach_san_pham, ghi_danh_sach_hoa_don,
                          tao_du_lieu_mam_san_pham, tao_du_lieu_mam_hoa_don)

from business import (sap_xep_noi_bot_san_pham_theo_gia, 
                      sap_xep_noi_bot_san_pham_theo_ton_kho,
                      tim_kiem_tuyen_tinh_san_pham_theo_ten,
                      tim_san_pham_theo_ma,
                      lap_hoa_don,
                      thong_ke_doanh_thu)

# ... (Giữ nguyên toàn bộ các hàm nhap_so_nguyen, hien_thi_danh_sach,... ở dưới)

# ===== HÀM VALIDATION - BẪY LỖI ĐẦU VÀO =====

def nhap_so_nguyen(loi_nhac, min_val=None, max_val=None):
    """
    Yêu cầu người dùng nhập số nguyên, bắt lỗi nếu nhập sai.
    Lặp đến khi nhận được giá trị hợp lệ.
    """
    while True:
        try:
            gia_tri = input(loi_nhac).strip()
            so = int(gia_tri)
            if min_val is not None and so < min_val:
                print(f"[LỖI] Giá trị phải >= {min_val}. Vui lòng nhập lại!")
                continue
            if max_val is not None and so > max_val:
                print(f"[LỖI] Giá trị phải <= {max_val}. Vui lòng nhập lại!")
                continue
            return so
        except ValueError:
            print("[LỖI] Vui lòng nhập một số nguyên hợp lệ!")

def nhap_so_thuc(loi_nhac, min_val=0.0):
    """Yêu cầu nhập số thực, không âm."""
    while True:
        try:
            gia_tri = input(loi_nhac).strip()
            so = float(gia_tri)
            if so < min_val:
                print(f"[LỖI] Giá trị phải >= {min_val}. Vui lòng nhập lại!")
                continue
            return so
        except ValueError:
            print("[LỖI] Vui lòng nhập một số thực hợp lệ!")

def nhap_chuoi_khong_trong(loi_nhac):
    """Yêu cầu nhập chuỗi không được để trống."""
    while True:
        gia_tri = input(loi_nhac).strip()
        if gia_tri != "":
            return gia_tri
        print("[LỖI] Không được để trống. Vui lòng nhập lại!")

def nhap_ngay(loi_nhac):
    """Yêu cầu nhập ngày đúng định dạng YYYY-MM-DD."""
    while True:
        ngay = input(loi_nhac).strip()
        # Kiểm tra định dạng cơ bản
        if len(ngay) == 10 and ngay[4] == '-' and ngay[7] == '-':
            try:
                nam = int(ngay[0:4])
                thang = int(ngay[5:7])
                ngay_trong_thang = int(ngay[8:10])
                if 2020 <= nam <= 2030 and 1 <= thang <= 12 and 1 <= ngay_trong_thang <= 31:
                    return ngay
            except:
                pass
        print("[LỖI] Định dạng ngày không hợp lệ. Vui lòng nhập theo mẫu YYYY-MM-DD!")

# ===== HÀM HIỂN THỊ DẠNG BẢNG (TABULAR DISPLAY) =====

def hien_thi_danh_sach_san_pham(danh_sach):
    """Hiển thị danh sách sản phẩm dạng bảng với f-string padding."""
    if len(danh_sach) == 0:
        print("\n[THÔNG BÁO] Danh sách sản phẩm trống!")
        return
    
    # Định nghĩa độ rộng cột
    print("\n" + "=" * 95)
    print(f"{'MÃ SP':<10} {'TÊN SẢN PHẨM':<35} {'DANH MỤC':<15} {'GIÁ BÁN':>15} {'TỒN KHO':>10}")
    print("-" * 95)
    
    for sp in danh_sach:
        # Định dạng giá bán có dấu phân cách hàng nghìn
        gia_formatted = f"{sp.gia_ban:,.0f} VNĐ"
        print(f"{sp.ma_sp:<10} {sp.ten:<35} {sp.danh_muc:<15} {gia_formatted:>15} {sp.ton_kho:>10}")
    
    print("=" * 95)
    print(f"Tổng số sản phẩm: {len(danh_sach)}")

# ===== CÁC CHỨC NĂNG MENU =====

def menu_them_san_pham():
    """Thêm sản phẩm mới vào danh sách."""
    print("\n=== THÊM SẢN PHẨM MỚI ===")
    danh_sach = doc_danh_sach_san_pham()
    
    # Tự sinh mã sản phẩm mới
    if len(danh_sach) == 0:
        ma_moi = "SP001"
    else:
        # Tìm mã lớn nhất
        so_lon_nhat = 0
        for sp in danh_sach:
            try:
                so = int(sp.ma_sp[2:])
                if so > so_lon_nhat:
                    so_lon_nhat = so
            except:
                continue
        ma_moi = f"SP{so_lon_nhat + 1:03d}"
    
    print(f"Mã sản phẩm tự động: {ma_moi}")
    ten = nhap_chuoi_khong_trong("Nhập tên sản phẩm: ")
    danh_muc = nhap_chuoi_khong_trong("Nhập danh mục (CPU/GPU/RAM/...): ")
    gia_ban = nhap_so_thuc("Nhập giá bán (VNĐ): ", min_val=1000)
    ton_kho = nhap_so_nguyen("Nhập số lượng tồn kho: ", min_val=0)
    
    sp_moi = SanPham(ma_moi, ten, danh_muc, gia_ban, ton_kho)
    danh_sach.append(sp_moi)
    ghi_danh_sach_san_pham(danh_sach)
    print(f"[THÀNH CÔNG] Đã thêm sản phẩm {ma_moi} - {ten}")

def menu_hien_thi_san_pham():
    """Hiển thị danh sách sản phẩm."""
    danh_sach = doc_danh_sach_san_pham()
    hien_thi_danh_sach_san_pham(danh_sach)

def menu_tim_kiem_san_pham():
    """Tìm kiếm sản phẩm theo tên (Linear Search tự viết)."""
    print("\n=== TÌM KIẾM SẢN PHẨM THEO TÊN ===")
    tu_khoa = nhap_chuoi_khong_trong("Nhập từ khóa tìm kiếm: ")
    
    danh_sach = doc_danh_sach_san_pham()
    ket_qua = tim_kiem_tuyen_tinh_san_pham_theo_ten(danh_sach, tu_khoa)
    
    if len(ket_qua) == 0:
        print(f"[KẾT QUẢ] Không tìm thấy sản phẩm nào chứa '{tu_khoa}'")
    else:
        print(f"[KẾT QUẢ] Tìm thấy {len(ket_qua)} sản phẩm:")
        hien_thi_danh_sach_san_pham(ket_qua)

def menu_sap_xep_san_pham():
    """Menu sắp xếp sản phẩm với Bubble Sort tự viết."""
    print("\n=== SẮP XẾP SẢN PHẨM ===")
    print("1. Sắp xếp theo giá bán (tăng dần)")
    print("2. Sắp xếp theo giá bán (giảm dần)")
    print("3. Sắp xếp theo tồn kho (giảm dần)")
    print("4. Sắp xếp theo tồn kho (tăng dần)")
    print("0. Quay lại")
    
    lua_chon = nhap_so_nguyen("Chọn: ", min_val=0, max_val=4)
    if lua_chon == 0:
        return
    
    danh_sach = doc_danh_sach_san_pham()
    
    if lua_chon == 1:
        danh_sach = sap_xep_noi_bot_san_pham_theo_gia(danh_sach, tang_dan=True)
        print("[KẾT QUẢ] Đã sắp xếp theo giá tăng dần (Bubble Sort)")
    elif lua_chon == 2:
        danh_sach = sap_xep_noi_bot_san_pham_theo_gia(danh_sach, tang_dan=False)
        print("[KẾT QUẢ] Đã sắp xếp theo giá giảm dần (Bubble Sort)")
    elif lua_chon == 3:
        danh_sach = sap_xep_noi_bot_san_pham_theo_ton_kho(danh_sach, tang_dan=False)
        print("[KẾT QUẢ] Đã sắp xếp theo tồn kho giảm dần (Bubble Sort)")
    elif lua_chon == 4:
        danh_sach = sap_xep_noi_bot_san_pham_theo_ton_kho(danh_sach, tang_dan=True)
        print("[KẾT QUẢ] Đã sắp xếp theo tồn kho tăng dần (Bubble Sort)")
    
    hien_thi_danh_sach_san_pham(danh_sach)
    ghi_danh_sach_san_pham(danh_sach)

def menu_lap_hoa_don():
    """Lập hóa đơn bán hàng mới."""
    print("\n=== LẬP HÓA ĐƠN BÁN HÀNG ===")
    
    danh_sach_sp = doc_danh_sach_san_pham()
    hien_thi_danh_sach_san_pham(danh_sach_sp)
    
    ma_kh = nhap_chuoi_khong_trong("\nNhập mã khách hàng: ")
    ngay_lap = nhap_ngay("Nhập ngày lập hóa đơn (YYYY-MM-DD): ")
    
    danh_sach_mua = []
    so_mon = nhap_so_nguyen("Nhập số loại sản phẩm mua: ", min_val=1)
    
    for i in range(so_mon):
        print(f"\n--- Sản phẩm thứ {i+1} ---")
        while True:
            ma_sp = nhap_chuoi_khong_trong("Nhập mã sản phẩm: ").upper()
            sp = tim_san_pham_theo_ma(danh_sach_sp, ma_sp)
            if sp is None:
                print(f"[LỖI] Sản phẩm {ma_sp} không tồn tại!")
                continue
            so_luong = nhap_so_nguyen(f"Nhập số lượng (tồn kho: {sp.ton_kho}): ", min_val=1)
            if so_luong > sp.ton_kho:
                print(f"[LỖI] Tồn kho không đủ! Chỉ còn {sp.ton_kho} sản phẩm.")
                continue
            danh_sach_mua.append((ma_sp, so_luong))
            break
    
    # SỬA LẠI: Truyền đúng 3 tham số và nhận về 2 giá trị (hoa_don, loi)
    hoa_don, loi = lap_hoa_don(ma_kh, ngay_lap, danh_sach_mua)
    
    if loi:
        print(f"\n[THẤT BẠI] {loi}")
    else:
        print("\n[THÀNH CÔNG] Hóa đơn đã được lập!")
        # Nếu cậu có hàm hien_thi_chi_tiet_hoa_don() thì mở comment dòng dưới
        # hien_thi_chi_tiet_hoa_don(hoa_don)

def menu_xem_hoa_don():
    """Xem danh sách hóa đơn."""
    danh_sach = doc_danh_sach_hoa_don()
    
    if len(danh_sach) == 0:
        print("\n[THÔNG BÁO] Chưa có hóa đơn nào!")
        return
    
    print("\n" + "=" * 90)
    # Tiêu đề đang ghim lề phải với độ rộng: 15, 12, 15
    print(f"{'MÃ HĐ':<10} {'MÃ KH':<10} {'NGÀY LẬP':<12} {'TIỀN HÀNG':>15} {'VAT':>12} {'T.THANH TOÁN':>15}")
    print("-" * 90)
    
    for hd in danh_sach:
        # Đã đồng bộ data thành 15, 12, 15 để khớp tuyệt đối với tiêu đề ở trên
        print(f"{hd.ma_hd:<10} {hd.ma_kh:<10} {hd.ngay_lap:<12} {hd.tong_tien_hang:>15,.0f} {hd.thue_vat:>12,.0f} {hd.tong_thanh_toan:>15,.0f}")
    
    print("=" * 90)
    print(f"Tổng số hóa đơn: {len(danh_sach)}")

def menu_thong_ke_doanh_thu():
    """Thống kê doanh thu theo khoảng ngày."""
    print("\n=== THỐNG KÊ DOANH THU ===")
    ngay_bd = nhap_ngay("Nhập ngày bắt đầu (YYYY-MM-DD): ")
    ngay_kt = nhap_ngay("Nhập ngày kết thúc (YYYY-MM-DD): ")
    
    if ngay_bd > ngay_kt:
        print("[LỖI] Ngày bắt đầu phải trước hoặc bằng ngày kết thúc!")
        return
    
    danh_sach_hd = doc_danh_sach_hoa_don()
    
    # SỬA LỖI TRUYỀN THAM SỐ Ở ĐÂY
    so_hoa_don, tong_doanh_thu = thong_ke_doanh_thu(danh_sach_hd, ngay_bd, ngay_kt)
    
    print("\n" + "=" * 50)
    print(f"=== KẾT QUẢ THỐNG KÊ ===")
    print(f"Khoảng thời gian: {ngay_bd} đến {ngay_kt}")
    print(f"Số hóa đơn trong kỳ: {so_hoa_don}")
    print(f"TỔNG DOANH THU: {tong_doanh_thu:,.0f} VNĐ")
    print("=" * 50)

# ===== MENU CHÍNH =====

def menu_chinh():
    """Vòng lặp menu chính của chương trình."""
    while True:
        print("\n" + "=" * 50)
        print("=== HỆ THỐNG QUẢN LÝ BÁN HÀNG ===")
        print("=== CỬA HÀNG MÁY TÍNH HUST FAMI ===")
        print("=" * 50)
        print("1. QUẢN LÝ SẢN PHẨM")
        print("2. QUẢN LÝ BÁN HÀNG")
        print("3. THỐNG KÊ DOANH THU")
        print("0. THOÁT")
        print("-" * 50)
        
        lua_chon = nhap_so_nguyen("Chọn chức năng: ", min_val=0, max_val=3)
        
        if lua_chon == 0:
            print("\n[CẢM ƠN] Đã thoát chương trình. Tạm biệt!")
            break
        elif lua_chon == 1:
            menu_san_pham()
        elif lua_chon == 2:
            menu_ban_hang()
        elif lua_chon == 3:
            menu_thong_ke_doanh_thu()

def menu_san_pham():
    """Menu con - Quản lý sản phẩm."""
    while True:
        print("\n--- QUẢN LÝ SẢN PHẨM ---")
        print("1. Xem danh sách sản phẩm")
        print("2. Thêm sản phẩm mới")
        print("3. Tìm kiếm sản phẩm theo tên")
        print("4. Sắp xếp sản phẩm")
        print("0. Quay lại menu chính")
        
        lua_chon = nhap_so_nguyen("Chọn: ", min_val=0, max_val=4)
        
        if lua_chon == 0:
            break
        elif lua_chon == 1:
            menu_hien_thi_san_pham()
        elif lua_chon == 2:
            menu_them_san_pham()
        elif lua_chon == 3:
            menu_tim_kiem_san_pham()
        elif lua_chon == 4:
            menu_sap_xep_san_pham()

def menu_ban_hang():
    """Menu con - Quản lý bán hàng."""
    while True:
        print("\n--- QUẢN LÝ BÁN HÀNG ---")
        print("1. Lập hóa đơn mới")
        print("2. Xem danh sách hóa đơn")
        print("0. Quay lại menu chính")
        
        lua_chon = nhap_so_nguyen("Chọn: ", min_val=0, max_val=2)
        
        if lua_chon == 0:
            break
        elif lua_chon == 1:
            menu_lap_hoa_don()
        elif lua_chon == 2:
            menu_xem_hoa_don()

# ===== ĐIỂM BẮT ĐẦU CHƯƠNG TRÌNH =====

if __name__ == "__main__":
    print("=== KHỞI ĐỘNG HỆ THỐNG ===")
    print("[HỆ THỐNG] Đang kiểm tra dữ liệu...")
    
    # LƯỢC BỎ HARDCODE: Sử dụng trực tiếp logic của file_handler
    sp_hien_tai = doc_danh_sach_san_pham()
    if not sp_hien_tai:
        tao_du_lieu_mam_san_pham()
        
    hd_hien_tai = doc_danh_sach_hoa_don()
    if not hd_hien_tai:
        tao_du_lieu_mam_hoa_don()
    
    print("[HỆ THỐNG] Sẵn sàng phục vụ!")
    menu_chinh()
