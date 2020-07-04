# _*_ encoding=utf-8 _*_
import re


def productNameModify(productName: str):
    data = productName.lower()
    data = re.sub(r"^ip+(?=[\s])","iphone",data)
    if data.find("ss") > -1 and data.find("galaxy") == -1:
        temp = data.replace("ss", "samsung galaxy")
        return temp
    elif data.find("samsung") > -1 and data.find("galaxy") == -1:
        temp = data.replace("samsung", "samsung galaxy")
        return temp
    elif data.find("samsung") == -1 and data.find("sung") >-1 and data.find("galaxy") == -1:
        temp = data.replace("sung", "samsung galaxy")
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
    if price.isnumeric():
        data = int(price)
        if data/1000<100 and data/1000>0:
            return data*1000
        else:
            return data
    else:
        data = price.lower().strip(" ").replace('mốt','1').replace(" ","").replace(".",",")
    so5 = ['lăm',"rưởi",'lam',"ruoi"]
    so4 = ['tu','tư','tứ']
    data = data.replace('trieu','triệu')
    for item in so5:
        data = data.replace(item,'5')
    for item in so4:
        data = data.replace(item,'4')
    word = ['một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín']
    word2 = ['mot', 'hai', 'ba', 'bon', 'nam', 'sau', 'bay', 'tam', 'chin']
    result = 0
    for i in range(0, 9):
        data = data.replace(word[i], str(i+1))
    for i in range(0, 9):
        data = data.replace(word2[i], str(i+1))
    if re.match("[0-9]mươi[0-9].", data) or re.match("[0-9]muoi[0-9].", data):
        data = data.replace('mươi','').replace('muoi','')
    if re.match("[0-9]mươi[^0-9]",data) or re.match("[0-9]muoi[^0-9].", data):
        data = data.replace('mươi','0').replace('muoi','0')

    if re.match("[0-9]+triệu[0-9]+", data) or re.match("[0-9]+m[0-9]+", data) or re.match("[0-9]+tr[0-9]+", data):
        temp = data.replace("triệu", ".").replace("tr",".").replace("m",".")
        num = temp.split(".")
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
        if len(num[1]) == 1:
            result = int(num[0])*1000000+int(num[1])*100000
        if len(num[1]) == 2:
            result = int(num[0])*1000000+int(num[1])*10000
        if len(num[1]) == 3:
            result = int(num[0])*1000000+int(num[1])*1000
        return result
    elif re.match("[0-9]+triệu", data) or re.match("[0-9]+m", data) or re.match("[0-9]+tr", data):
        temp = data.replace("triệu", "").replace("tr","").replace("m","")
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
    data = {"công nghệ màn hình":"cong_nghe_man_hinh","độ phân giải màn hình":"do_phan_giai","màu màn hình":"mau_man_hinh","chuẩn màn hình":"chuan_man_hinh","công nghệ cảm ứng":"cong_nghe_cam_ung","màn hình":"man_hinh","mặt kính màn hình":"mat_kinh_man_hinh","ram":"ram","tốc độ cpu":"toc_do_cpu","số nhân":"so_nhan","chipset":"chipset","chip đồ họa (gpu)":"gpu","cảm biến":"cam_bien","thẻ nhớ ngoài":"the_nho_ngoai","hỗ trợ thẻ nhớ tối đa":"dung_luong_the_nho_toi_da","danh bạ lưu trữ":"dung_luong_danh_ba","rom":"rom","bộ nhớ còn lại":"bo_nho_con_lai","kích thước":"kich_thuoc","trọng lượng":"trong_luong","kiểu dáng":"kieu_dang","chất liệu":"chat_lieu","khả năng chống nước":"chong_nuoc","loại pin":"loai_pin","dung lượng pin":"dung_luong_pin","pin có thể tháo rời":"thao_roi_pin","thời gian chờ":"thoi_gian_cho","thời gian đàm thoại":"thoi_gian_dam_thoai","thời gian sạc đầy":"thoi_gian_sac","chế độ sạc nhanh":"sac_nhanh","kết nối usb":"ket_noi_usb","cổng kết nối khác":"cong_ket_noi_khac","cổng sạc":"cong_sac","jack (input & output)":"jack_in_out","wifi":"wifi","gps":"gps","bluetooth":"bluetooth","gprs":"gprs","edge":"edge","loại sim":"loai_sim","băng tần 2g":"mang_2g","băng tần 3g":"mang_3g","băng tần 4g":"mang_4g","khe cắm sim":"khe_cam_sim","nfc":"nfc","model series":"model_series","hệ điều hành":"he_dieu_hanh","xem phim":"xem_phim","nghe nhạc":"nghe_nhac","ghi âm":"ghi_am","fm radio":"fm_radio","đèn pin":"den_pin","chức năng khác":"chuc_nang_khac","thời gian bảo hành":"thoi_gian_bao_hanh","xuất xứ":"xuat_xu","năm sản xuất":"nam_san_xuat","độ phân giải cam sau":"do_phan_giai_cam_sau","độ phân giải cam trước":"do_phan_giai_cam_truoc","thông tin khác":"thong_tin_khac","quay phim":"quay_phim","đèn flash":"den_flash","chụp ảnh nâng cao":"chup_anh_nang_cao","video call":"video_call","gprs/edge":"gprs","công nghệ pin":"cong_nghe_pin","mạng di động":"mang_2g"}
    result = data[temp]
    return result

print(priceModify('8500000'))
