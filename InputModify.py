import re


def productNameModify(productName: str):
    data = productName.lower()
    if data.find("ip") > -1 and data.find("iphone") == -1:
        temp = data.replace("ip", "iphone")
        return temp
    elif data.find("ss") > -1 and data.find("galaxy") == -1:
        temp = data.replace("ss", "samsung galaxy")
        return temp
    elif data.find("samsung") > -1 and data.find("galaxy") == -1:
        temp = data.replace("samsung", "samsung galaxy")
        return temp
    elif data.find("ss") > -1 and data.find("galaxy") > -1:
        temp = data.replace("ss", "samsung")
        return temp
    elif data.find("opo")>-1:
        temp = data.replace("opo", "oppo")
        return temp
    elif data.find("vv") > -1:
        temp = data.replace("vv", "vivo")
        return temp

    return data


def romRamModify(rom: str):
    data = rom.lower()
    if data.find("gb") > -1 and data.find(" ") == -1:
        temp = data.replace("gb", " gb")
        return temp

    if data.find("gb") == -1 and data.find(" ") == -1 and data.find("g") > -1:
        temp = data.replace("g", " gb")
        return temp
    return data


def priceModify(price: str):
    data = price.lower().strip(" ").replace("lăm", "5").replace("mốt", "1").replace("tư", "4").replace(" ", "").replace(".", ",").replace("rưởi","5")
    word = ['một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín']
    result = 0
    for i in range(0, 9):
        data = data.replace(word[i], str(i+1))
    # specialword = ["m","tr","trịu","trieu"]
    # for item in specialword:
        # data = data.replace(item,"triệu")
    if re.match("[0-9]mươi[0-9].", data):
        data = data.replace('mươi','')
    if re.match("[0-9]mươi[^0-9]",data):
        data = data.replace('mươi','0')

    if re.match("[0-9]+triệu[0-9]+", data) or re.match("[0-9]+m[0-9]+", data) or re.match("[0-9]+tr[0-9]+", data):
        temp = data.replace("triệu", ".").replace("tr",".").replace("m",".")
        # print(temp)
        num = temp.split(".")
        # print(num)
        if len(num[1]) == 1:
            result = int(num[0])*1000000+int(num[1])*100000
        if len(num[1]) == 2:
            result = int(num[0])*1000000+int(num[1])*10000
        if len(num[1]) == 3:
            result = int(num[0])*1000000+int(num[1])*1000
        return result
    elif re.match("[0-9]+,[0-9]+triệu", data) or re.match("[0-9]+,[0-9]+m", data) or re.match("[0-9]+,[0-9]+tr", data):
        temp = data.replace("triệu", "").replace("tr",".").replace("m",".")
        num = temp.split(".")
        # print(len(num[1]))
        if len(num[1]) == 1:
            result = int(num[0])*1000000+int(num[1])*100000
        if len(num[1]) == 2:
            result = int(num[0])*1000000+int(num[1])*10000
        if len(num[1]) == 3:
            result = int(num[0])*1000000+int(num[1])*1000
        return result
    elif re.match("[0-9]+triệu", data) or re.match("[0-9]+m", data) or re.match("[0-9]+tr", data):
        temp = data.replace("triệu", "").replace("tr","").replace("m","")
        # num = temp.split(".")
        # # print(len(num[1]))
        # if len(num[1])==1:
        #     result = num[0]+"."+num[1]+"00.000"
        # if len(num[1])==2:
        #     result = num[0]+"."+num[1]+"0.000"
        # if len(num[1])==3:
        result = int(temp)*1000000
        return result

    return data

def PrepayPercentModify(temp:str):
    res_tmp = temp.replace(" ","").replace("%","").strip('\n')
    res = int(res_tmp)
    return res

def InstallmentPaymentPeriod(temp:str):
    res = int(temp.isdigit())
    return res

def RoundNum(temp:int):
    res = round(temp/10000)*10000
    return res

def GetColName(temp:str):
    data = {"Công nghệ màn hình":"cong_nghe_man_hinh","Độ phân giải màn hình":"do_phan_giai","Màu màn hình":"mau_man_hinh","Chuẩn màn hình":"chuan_man_hinh","Công nghệ cảm ứng":"cong_nghe_cam_ung","Màn hình":"man_hinh","Mặt kính màn hình":"mat_kinh_man_hinh","RAM":"ram","Tốc độ CPU":"toc_do_cpu","Số nhân":"so_nhan","Chipset":"chipset","Chip đồ họa (GPU)":"gpu","Cảm biến":"cam_bien","Thẻ nhớ ngoài":"the_nho_ngoai","Hỗ trợ thẻ nhớ tối đa":"dung_luong_the_nho_toi_da","Danh bạ lưu trữ":"dung_luong_danh_ba","ROM":"rom","Bộ nhớ còn lại":"bo_nho_con_lai","Kích thước":"kich_thuoc","Trọng lượng":"trong_luong","Kiểu dáng":"kieu_dang","Chất liệu":"chat_lieu","Khả năng chống nước":"chong_nuoc","Loại pin":"loai_pin","Dung lượng pin":"dung_luong_pin","Pin có thể tháo rời":"thao_roi_pin","Thời gian chờ":"thoi_gian_cho","Thời gian đàm thoại":"thoi_gian_dam_thoai","Thời gian sạc đầy":"thoi_gian_sac","Chế độ sạc nhanh":"sac_nhanh","Kết nối USB":"ket_noi_usb","Cổng kết nối khác":"cong_ket_noi_khac","Cổng sạc":"cong_sac","Jack (Input & Output)":"jack_in_out","Wifi":"wifi","GPS":"gps","Bluetooth":"bluetooth","GPRS":"gprs","EDGE":"edge","Loại SIM":"loai_sim","Băng tần 2G":"mang_2g","Băng tần 3G":"mang_3g","Băng tần 4G":"mang_4g","Khe cắm sim":"khe_cam_sim","NFC":"nfc","Model Series":"model_series","Hệ điều hành":"he_dieu_hanh","Xem phim":"xem_phim","Nghe nhạc":"nghe_nhac","Ghi âm":"ghi_am","FM radio":"fm_radio","Đèn pin":"den_pin","Chức năng khác":"chuc_nang_khac","Thời gian bảo hành":"thoi_gian_bao_hanh","Xuất xứ":"xuat_xu","Năm sản xuất":"nam_san_xuat","Độ phân giải cam sau":"do_phan_giai_cam_sau","Độ phân giải cam trước":"do_phan_giai_cam_truoc","Thông tin khác":"thong_tin_khac","Quay phim":"quay_phim","Đèn Flash":"den_flash","Chụp ảnh nâng cao":"chup_anh_nang_cao","Video Call":"video_call","GPRS/EDGE":"gprs","Công nghệ pin":"cong_nghe_pin","Mạng di động":"mang_2g"}
    result = data[temp]
    return result
# print("{:,}".format(priceAnalysis("2 củ")))
# print(RoundNum(809216))