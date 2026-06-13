"""
Module: business.py
Mô tả: Chứa các thuật toán nền tảng tự cài đặt (Sắp xếp nổi bọt, Tìm kiếm tuyến tính)
và các chức năng nghiệp vụ: lập hóa đơn, thống kê doanh thu.
"""

from models import SanPham, HoaDon
from file_handler import doc_danh_sach_san_pham, doc_danh_sach_hoa_don
from file_handler import ghi_danh_sach_san_pham, ghi_danh_sach_hoa_don

# ===== THUẬT TOÁN NỀN TẢNG TỰ CÀI ĐẶT =====

def sap_xep_noi_bot_san_pham_theo_gia(danh_sach, tang_dan=True):
    n = len(danh_sach)
    for i in range(n - 1):
        # Cờ kiểm tra đã sắp xếp xong chưa để tối ưu dừng sớm
        da_hoan_doi = False
        for j in range(n - 1 - i):
            # So sánh phần tử j và j+1
            can_hoan_doi = False
            if tang_dan:
                # Sắp xếp tăng dần: phần tử trước > phần tử sau thì hoán đổi
                if danh_sach[j].gia_ban > danh_sach[j+1].gia_ban:
                    can_hoan_doi = True
            else:
                # Sắp xếp giảm dần: phần tử trước < phần tử sau thì hoán đổi
                if danh_sach[j].gia_ban < danh_sach[j+1].gia_ban:
                    can_hoan_doi = True
            
            if can_hoan_doi:
                # Hoán đổi vị trí 2 phần tử
                danh_sach[j], danh_sach[j+1] = danh_sach[j+1], danh_sach[j]
                da_hoan_doi = True
        
        # Nếu không có hoán đổi nào, mảng đã sắp xếp xong -> dừng sớm
        if not da_hoan_doi:
            break
    return danh_sach

def sap_xep_noi_bot_san_pham_theo_ton_kho(danh_sach, giam_dan=True):
    n = len(danh_sach)
    for i in range(n - 1):
        da_hoan_doi = False
        for j in range(n - 1 - i):
            can_hoan_doi = False
            if giam_dan:
                if danh_sach[j].ton_kho < danh_sach[j+1].ton_kho:
                    can_hoan_doi = True
            else:
                if danh_sach[j].ton_kho > danh_sach[j+1].ton_kho:
                    can_hoan_doi = True
            
            if can_hoan_doi:
                danh_sach[j], danh_sach[j+1] = danh_sach[j+1], danh_sach[j]
                da_hoan_doi = True
        
        if not da_hoan_doi:
            break
    return danh_sach

def tim_kiem_tuyen_tinh_san_pham_theo_ten(danh_sach, tu_khoa):
    ket_qua = []
    tu_khoa_lower = tu_khoa.lower()
    
    for sp in danh_sach:
        ten_lower = sp.ten.lower()
        # Tự cài đặt kiểm tra chuỗi con thay vì dùng 'in'
        if kiem_tra_chuoi_con(ten_lower, tu_khoa_lower):
            ket_qua.append(sp)
    return ket_qua

def kiem_tra_chuoi_con(chuoi_goc, chuoi_con):
  
    len_goc = len(chuoi_goc)
    len_con = len(chuoi_con)
    
    if len_con == 0:
        return True
    if len_con > len_goc:
        return False
    
    # Duyệt qua từng vị trí bắt đầu có thể trong chuỗi gốc
    for i in range(len_goc - len_con + 1):
        khop = True
        # Kiểm tra từng ký tự của chuỗi con
        for j in range(len_con):
            if chuoi_goc[i + j] != chuoi_con[j]:
                khop = False
                break
        if khop:
            return True
    return False

def tim_san_pham_theo_ma(danh_sach, ma_sp):
   
    for sp in danh_sach:
        if sp.ma_sp == ma_sp:
            return sp
    return None

# ===== CHỨC NĂNG NGHIỆP VỤ =====

def lay_ma_hoa_don_tiep_theo():
    
    danh_sach_hd = doc_danh_sach_hoa_don()
    if len(danh_sach_hd) == 0:
        return "HD001"
    
    # Tìm mã lớn nhất bằng cách duyệt tuần tự
    so_lon_nhat = 0
    for hd in danh_sach_hd:
        # Mã hóa đơn có dạng HDxxx, lấy phần số
        try:
            so_hd = int(hd.ma_hd[2:])  # Bỏ "HD" lấy phần số
            if so_hd > so_lon_nhat:
                so_lon_nhat = so_hd
        except:
            continue
    
    so_tiep_theo = so_lon_nhat + 1
    return f"HD{so_tiep_theo:03d}"  # Định dạng 3 chữ số

def lap_hoa_don(ma_kh, ngay_lap, danh_sach_mua):
    """
    Lập hóa đơn bán hàng:
    - danh_sach_mua: list các tuple (ma_sp, so_luong)
    - Kiểm tra tồn kho, nếu đủ thì trừ tồn kho.
    - Tính tổng tiền hàng, thuế VAT 8%, tổng thanh toán.
    - Tạo đối tượng HoaDon và lưu vào file.
    - Trả về: (hoa_don, thong_bao_loi)
    """
    danh_sach_sp = doc_danh_sach_san_pham()
    
    # Kiểm tra tồn kho trước khi xử lý
    for ma_sp, so_luong in danh_sach_mua:
        sp = tim_san_pham_theo_ma(danh_sach_sp, ma_sp)
        if sp is None:
            return None, f"Sản phẩm {ma_sp} không tồn tại!"
        if sp.ton_kho < so_luong:
            return None, f"Sản phẩm {sp.ten} ({ma_sp}) chỉ còn {sp.ton_kho} sản phẩm, không đủ {so_luong}!"
    
    # Xử lý trừ tồn kho và tính tiền
    tong_tien_hang = 0.0
    chi_tiet_mua = ""
    
    for idx, (ma_sp, so_luong) in enumerate(danh_sach_mua):
        sp = tim_san_pham_theo_ma(danh_sach_sp, ma_sp)
        
        # Trừ tồn kho trực tiếp
        sp.ton_kho -= so_luong
        
        # Tính tiền
        thanh_tien = sp.gia_ban * so_luong
        tong_tien_hang += thanh_tien
        
        # Xây dựng chuỗi chi tiết mua
        if idx > 0:
            chi_tiet_mua += ";"
        chi_tiet_mua += f"{ma_sp}:{so_luong}"
    
    # Tính thuế VAT 8%
    thue_vat = tong_tien_hang * 0.08
    tong_thanh_toan = tong_tien_hang + thue_vat
    
    # Tạo hóa đơn mới
    ma_hd = lay_ma_hoa_don_tiep_theo()
    hoa_don_moi = HoaDon(
        ma_hd=ma_hd,
        ma_kh=ma_kh,
        ngay_lap=ngay_lap,
        tong_tien_hang=tong_tien_hang,
        thue_vat=thue_vat,
        tong_thanh_toan=tong_thanh_toan,
        chi_tiet_mua=chi_tiet_mua
    )
    
    # Lưu hóa đơn
    danh_sach_hd = doc_danh_sach_hoa_don()
    danh_sach_hd.append(hoa_don_moi)
    ghi_danh_sach_hoa_don(danh_sach_hd)
    
    # Đồng bộ thay đổi tồn kho xuống file
    ghi_danh_sach_san_pham(danh_sach_sp)
    
    return hoa_don_moi, None

def thong_ke_doanh_thu(danh_sach_hd, ngay_bat_dau, ngay_ket_thuc):
    """
    Thống kê doanh thu trong khoảng ngày.
    - Duyệt tuần tự danh sách hóa đơn, kiểm tra ngày lập nằm trong khoảng.
    - Cộng dồn tổng thanh toán.
    - So sánh ngày thủ công bằng cách so sánh chuỗi YYYY-MM-DD.
    """
    tong_doanh_thu = 0.0
    so_hoa_don = 0
    
    for hd in danh_sach_hd:
        # So sánh chuỗi ngày: định dạng YYYY-MM-DD có thể so sánh trực tiếp
        if ngay_bat_dau <= hd.ngay_lap <= ngay_ket_thuc:
            tong_doanh_thu += hd.tong_thanh_toan
            so_hoa_don += 1
    
    # Trả về đúng thứ tự: Số lượng hóa đơn trước, Tổng tiền sau
    return so_hoa_don, tong_doanh_thu