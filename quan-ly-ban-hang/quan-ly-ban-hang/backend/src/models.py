"""
Module: models.py
Mô tả: Định nghĩa các class đối tượng thô (chỉ chứa thuộc tính) để mô phỏng
cấu trúc dữ liệu tĩnh, không sử dụng dictionary phức tạp.
"""

class SanPham:
    """Class mô phỏng struct sản phẩm - chỉ chứa thuộc tính, không phương thức xử lý"""
    def __init__(self, ma_sp="", ten="", danh_muc="", gia_ban=0.0, ton_kho=0):
        self.ma_sp = ma_sp            # Mã sản phẩm (SP001, SP002,...)
        self.ten = ten                # Tên sản phẩm
        self.danh_muc = danh_muc      # Danh mục (CPU, GPU, RAM,...)
        self.gia_ban = gia_ban        # Giá bán (VNĐ)
        self.ton_kho = ton_kho        # Số lượng tồn kho

class HoaDon:
    """Class mô phỏng struct hóa đơn - chỉ chứa thuộc tính"""
    def __init__(self, ma_hd="", ma_kh="", ngay_lap="", tong_tien_hang=0.0, 
                 thue_vat=0.0, tong_thanh_toan=0.0, chi_tiet_mua=""):
        self.ma_hd = ma_hd            # Mã hóa đơn (HD001, HD002,...)
        self.ma_kh = ma_kh            # Mã khách hàng
        self.ngay_lap = ngay_lap      # Ngày lập (YYYY-MM-DD)
        self.tong_tien_hang = tong_tien_hang  # Tổng tiền trước thuế
        self.thue_vat = thue_vat      # Thuế VAT (8%)
        self.tong_thanh_toan = tong_thanh_toan  # Tổng thanh toán sau thuế
        self.chi_tiet_mua = chi_tiet_mua  # Chuỗi chi tiết: "ma_sp1:sl1;ma_sp2:sl2"