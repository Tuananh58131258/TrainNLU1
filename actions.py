# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import time
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
from inputAnalysis import priceAnalysis
from inputAnalysis import productNameAnalysis
from inputAnalysis import romramAnalysis
from inputAnalysis import PrepayPercent
from inputAnalysis import InstallmentPaymentPeriod
from inputAnalysis import RoundNum
from dbConnect import getData
from makemessage import GenericTemplate
from makemessage import ButtonTemplate
from makemessage import TemplateItems
from makemessage import Hardware
#
#


class ActionCustomFallback(Action):

    def name(self) -> Text:
        return "action_custom_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        time_temp = time.localtime()
        tgian = time.strftime("%d/%m/%Y, %H:%M:%S", time_temp)
        dispatcher.utter_message(text="Fallback fallback")

        temp = tracker.latest_message.get('text')
        log = ""
        # log = tracker.get_latest_entity_values.get('role')
        if temp:
            log = temp
        else:
            log = "Khách hàng gửi icon hoặc bỏ trống!"
        convertion_log = "Thời gian: {}\nNội dung khách hàng gửi: {}\n--------------------------\n".format(
            tgian, log)
        # print(convertion_log)
        fobj = open('LOG/log.txt', 'a', encoding='utf-8')
        fobj.write(convertion_log)
        fobj.close()
        return [UserUtteranceReverted()]


class ActionTestST(Action):

    def name(self) -> Text:
        return "action_test_st"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        des = ""
        role = ""
        try:
            des = next(tracker.get_latest_entity_values(
                entity_type='hardware', entity_role='WHQ'))
            role = "WHQ"
        except StopIteration:
            pass
        try:
            des = next(tracker.get_latest_entity_values(
                entity_type='hardware', entity_role='YorN'))
            role = "YorN"
        except StopIteration:
            pass
        res = "entity value : {}, role: {}".format(des, role)
        dispatcher.utter_message(res)
        return


class ActionProductPrice(Action):
    # action trả lời giá sản phẩm
    def name(self) -> Text:
        return "action_product_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        try:
            productName = productNameAnalysis(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            pass
        if productName:
            sqlQuery = "Select * from fptshop.dienthoai where ten like '%{}%'".format(
                productName)
            try:
                ram = romramAnalysis(
                    next(tracker.get_latest_entity_values(entity_type='ram')))
                sqlQuery = sqlQuery + "and ram like '%{}%'".format(ram)
            except:
                pass
            try:
                rom = romramAnalysis(
                    next(tracker.get_latest_entity_values(entity_type='rom')))
                sqlQuery = sqlQuery + "and rom like '%{}%'".format(rom)
            except:
                pass
            sqlQuery = sqlQuery + "limit 9;"
            result = getData(sqlQuery)
            if result:
                list_item = []
                for item in result:
                    list_btn = [ButtonTemplate("Xem chi tiết", "Cấu hình của {} như thế nào".format(
                        item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia = "Giá: {}".format(item['gia'])
                    else:
                        gia = "Đang cập nhật"
                    mess_item = TemplateItems(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(
                    text="Giá nè", json_message=message_str)
            else:
                dispatcher.utter_message(
                    "Không tìm thấy sản phẩm. Vui lòng thử lại")
            print(sqlQuery)
        else:
            dispatcher.utter_message(
                "Không tìm thấy sản phẩm vui lòng thử lại sau")
        return


class ActionOnlinePrice(Action):
    # action trả lời giá online
    def name(self) -> Text:
        return "action_online_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        try:
            productName = productNameAnalysis(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            pass
        if productName:
            sqlQuery = "Select * from fptshop.dienthoai where ten like '%{}%'".format(
                productName)
            try:
                ram = romramAnalysis(
                    next(tracker.get_latest_entity_values(entity_type='ram')))
                sqlQuery = sqlQuery + "and ram like '%{}%'".format(ram)
            except:
                pass
            try:
                rom = romramAnalysis(
                    next(tracker.get_latest_entity_values(entity_type='rom')))
                sqlQuery = sqlQuery + "and rom like '%{}%'".format(rom)
            except:
                pass
            sqlQuery = sqlQuery + "limit 9;"
            result = getData(sqlQuery)
            if result:
                list_item = []
                for item in result:
                    list_btn = [ButtonTemplate("Xem chi tiết", "Cấu hình của {} như thế nào".format(
                        item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia_online']:
                        gia = "Giá online: {}".format(item['gia_online'])
                    else:
                        gia = "Giá online: Đang cập nhật"
                    mess_item = TemplateItems(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(
                    text="Giá nè", json_message=message_str)
            else:
                dispatcher.utter_message(
                    "Không tìm thấy sản phẩm. Vui lòng thử lại")
            print(sqlQuery)
        else:
            dispatcher.utter_message(
                "Không tìm thấy sản phẩm vui lòng thử lại sau")
        return


class ActionOldProduct(Action):
    # action trả lời giá của sản phẩm cũ
    def name(self) -> Text:
        return "action_old_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        try:
            productName = productNameAnalysis(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            pass
        if productName:
            sqlQuery = "Select * from fptshop.dienthoai where ten like '%{}%'".format(
                productName)
            try:
                ram = romramAnalysis(
                    next(tracker.get_latest_entity_values(entity_type='ram')))
                sqlQuery = sqlQuery + "and ram like '%{}%'".format(ram)
            except:
                pass
            try:
                rom = romramAnalysis(
                    next(tracker.get_latest_entity_values(entity_type='rom')))
                sqlQuery = sqlQuery + "and rom like '%{}%'".format(rom)
            except:
                pass
            sqlQuery = sqlQuery + "limit 9;"
            result = getData(sqlQuery)
            if result:
                list_item = []
                for item in result:
                    list_btn = [ButtonTemplate("Xem chi tiết", "Cấu hình của {} như thế nào".format(
                        item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia_cu']:
                        gia = "Giá cũ: {}".format(item['gia_cu'])
                    else:
                        gia = "Giá cũ: Đang cập nhật"
                    mess_item = TemplateItems(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(
                    text="Giá nè", json_message=message_str)
            else:
                dispatcher.utter_message(
                    "Không tìm thấy sản phẩm. Vui lòng thử lại")
            print(sqlQuery)
        else:
            dispatcher.utter_message(
                "Không tìm thấy sản phẩm vui lòng thử lại sau")
        return


class ActionProductConfiguration(Action):
    # action trả lời cấu hình của sản phẩm
    def name(self) -> Text:
        return "action_product_configuration"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("this is test")

        return


class ActionTypeOfProduct(Action):
    # action trả lời các hãng điện thoại sẵn có
    def name(self) -> Text:
        return "action_type_of_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sqlQuery = "select * from fptshop.hangdienthoai limit 9;"
        data = getData(sqlQuery)
        try:
            list_item = []
            for item in data:
                list_btn = [ButtonTemplate("Danh sách điện thoại của {}".format(
                    item['ten']), "Danh sách điện thoại của {}".format(item['ten']))]
                template_item = TemplateItems(
                    item['ten'], item['url_logo'], item['ten'], list_btn)
                list_item.append(template_item)
            message_str = GenericTemplate(list_item)
            dispatcher.utter_message(json_message=message_str)
        except:
            dispatcher.utter_message(
                "Không có danh sách hãng điện thoại để hiển thị!")
        return


class ActionListProduct(Action):
    # action trả lời danh sách các sản phẩm của 1 hãng
    def name(self) -> Text:
        return "action_list_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("this is test")
        product_company = ""
        try:
            product_company = next(tracker.get_latest_entity_values(
                entity_type="product_company"))
        except:
            pass
        if product_company:
            sqlQuery = "Select * from fptshop.dienthoai where ten like '%{}%' limit 9;".format(
                product_company)
            try:
                data = getData(sqlQuery)
                list_item = []
                for item in data:
                    list_btn = [ButtonTemplate("Xem chi tiết", "Cấu hình của {} như thế nào".format(
                        item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia = "Giá: {}".format(item['gia'])
                    else:
                        gia = "Đang cập nhật"
                    mess_item = TemplateItems(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(text="Danh sách điện thoại của {}".format(
                    product_company), json_message=message_str)
            except:
                print(sqlQuery)
                pass
        else:
            dispatcher.utter_message(
                "Không tìm thấy hãng điện thoại bạn vừa nhập, vui lòng thử lại")
        return


class ActionCheckPrice(Action):
    # action kiểm tra giá sản phẩm
    def name(self) -> Text:
        return "action_check_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        price = 0
        try:
            price = priceAnalysis(
                next(tracker.get_latest_entity_values(entity_type='price')))
        except:
            pass
        if price != 0:
            productName = ""
            try:
                productName = productNameAnalysis(
                    next(tracker.get_latest_entity_values(entity_type='product_name')))
            except:
                pass
            if productName:
                sqlQuery = "Select * from fptshop.dienthoai where ten like '%{}%'".format(
                    productName)
                try:
                    ram = romramAnalysis(
                        next(tracker.get_latest_entity_values(entity_type='ram')))
                    sqlQuery = sqlQuery + "and ram like '%{}%'".format(ram)
                except:
                    pass
                try:
                    rom = romramAnalysis(
                        next(tracker.get_latest_entity_values(entity_type='rom')))
                    sqlQuery = sqlQuery + "and rom like '%{}%'".format(rom)
                except:
                    pass
                sqlQuery = sqlQuery + "limit 9;"
                data = getData(sqlQuery)
                for item in data:
                    if item['gia'] == price:
                        dispatcher.utter_message(
                            "Dạ đúng rồi ạ. Giá của sản phẩm {} là {} ạ.".format(item['ten'], item['gia']))
                    else:
                        dispatcher.utter_message(
                            "Dạ không phải ạ. Giá của sản phẩm {} là {} ạ.".format(item['ten'], item['gia']))
            else:
                dispatcher.utter_message("Không tìm thấy sản phẩm yêu cầu")

            return


class ActionFindProductInRangePrice(Action):
    # action tìm kiếm sản phẩm trong 1 khoảng giá
    def name(self) -> Text:
        return "action_find_product_in_range_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            from_price = priceAnalysis(tracker.get_latest_entity_values(
                entity_type='price', entity_role='from_price'))
        except:
            pass
        try:
            to_price = priceAnalysis(tracker.get_latest_entity_values(
                entity_type='price', entity_role='to_price'))
        except:
            pass
        if from_price and to_price and from_price != to_price:
            if from_price > to_price:
                text = "Danh sách sản phẩm có giá từ {} đến {}".format(
                    to_price, from_price)
                sqlQuery = "select * from fptshop.dienthoai where gia between {} and {} limit 9".format(
                    to_price, from_price)
            else:
                text = "Danh sách sản phẩm có giá từ {} đến {}".format(
                    from_price, to_price)
                sqlQuery = "select * from fptshop.dienthoai where gia between {} and {} limit 9".format(
                    from_price, to_price)
            data = getData(sqlQuery)
            list_item = []
            for item in data:
                list_btn = [ButtonTemplate("Xem chi tiết", "Cấu hình của {} như thế nào".format(
                    item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                gia = ""
                if item['gia']:
                    gia = "Giá: {}".format(item['gia'])
                else:
                    gia = "Đang cập nhật"
                mess_item = TemplateItems(
                    item['ten'], item['url_img'], gia, list_btn)
                list_item.append(mess_item)

            message_str = GenericTemplate(list_item)
            dispatcher.utter_message(text=text, json_message=message_str)
        else:
            dispatcher.utter_message("Nothing here to display")
        return


class ActionFindProductLowerPrice(Action):
    # action tìm sản phấm dưới 1 mức giá
    def name(self) -> Text:
        return "action_find_product_lower_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            price = priceAnalysis(
                next(tracker.get_latest_entity_values(entity_type='price')))
        except:
            pass
        if price:
            sqlQuery = "select * from fptshop.dienthoai where gia <= {} order by gia desc limit 9".format(
                price)
            try:
                data = getData(sqlQuery)
                list_item = []
                for item in data:
                    list_btn = [ButtonTemplate("Xem chi tiết", "Cấu hình của {} như thế nào".format(
                        item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia = "Giá: {}".format(item['gia'])
                    else:
                        gia = "Đang cập nhật"
                    mess_item = TemplateItems(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(json_message=message_str)
            except:
                print(sqlQuery)
                pass
        else:
            dispatcher.utter_message("Nothing here")
        return


class ActionFindProductUpperPrice(Action):
    # action tìm sản phẩm trên 1 mức giá
    def name(self) -> Text:
        return "action_find_product_upper_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            price = priceAnalysis(
                next(tracker.get_latest_entity_values(entity_type='price')))
        except:
            pass
        if price:
            sqlQuery = "select * from fptshop.dienthoai where gia >= {} order by gia asc limit 9".format(
                price)
            try:
                data = getData(sqlQuery)
                list_item = []
                for item in data:
                    list_btn = [ButtonTemplate("Xem chi tiết", "Cấu hình của {} như thế nào".format(
                        item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia = "Giá: {}".format(item['gia'])
                    else:
                        gia = "Đang cập nhật"
                    mess_item = TemplateItems(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(json_message=message_str)
            except:
                print(sqlQuery)
                pass
        else:
            dispatcher.utter_message("Nothing here")
        return


class ActionFindProductAroundPrice(Action):
    # action tìm sản phẩm quanh 1 mức giá
    def name(self) -> Text:
        return "action_find_product_around_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            price = priceAnalysis(
                next(tracker.get_latest_entity_values(entity_type='price')))
        except:
            pass
        if price:
            p1 = price - 500000
            p2 = price + 1000000
            sqlQuery = "select * from fptshop.dienthoai where gia between {} and {} order by gia asc limit 9".format(
                p1, p2)
            try:
                data = getData(sqlQuery)
                list_item = []
                for item in data:
                    list_btn = [ButtonTemplate("Xem chi tiết", "Cấu hình của {} như thế nào".format(
                        item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia = "Giá: {}".format(item['gia'])
                    else:
                        gia = "Đang cập nhật"
                    mess_item = TemplateItems(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(json_message=message_str)
            except:
                print(sqlQuery)
                pass
        else:
            dispatcher.utter_message("Nothing here")
        return


class ActionScreenInfo(Action):
    # action thông tin màn hình
    def name(self) -> Text:
        return "action_scree_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            productName = productNameAnalysis(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
            sqlQuery = "Select * from fptshop.dienthoai where ten like '%{}%'".format(
                productName)
            data = getData(sqlQuery)
            hardware_lable = data[0]['lable'].split('/')
            hardware_data = data[0]['data'].split('/')
            for item in hardware_lable:
                if item.find('Công nghệ màn hình') > -1:
                    temp = hardware_lable.index(item)

            message_str = "Điện thoại {} sử dụng công ngệ màn hình: {}".format(
                productName, hardware_data[temp])
            dispatcher.utter_message(message_str)
        except:
            dispatcher.utter_message("không có tên sản phẩm")

        return


class ActionPinInfo(Action):
    # action thông tin về pin
    def name(self) -> Text:
        return "action_pin_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            productName = productNameAnalysis(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
            sqlQuery = "Select * from fptshop.dienthoai where ten like '%{}%'".format(
                productName)
            data = getData(sqlQuery)
            hardware_lable = data[0]['lable'].split('/')
            hardware_data = data[0]['data'].split('/')
            for item in hardware_lable:
                if item.find('Loại pin') > -1:
                    temp = hardware_lable.index(item)

            message_str = "Điện thoại {} sử dụng pin: {}".format(
                productName, hardware_data[temp])
            dispatcher.utter_message(message_str)
        except:
            dispatcher.utter_message("không có tên sản phẩm")

        return


class ActionBuyOldProduct(Action):
    # action thu mua lại sản phẩm cũ
    def name(self) -> Text:
        return "action_buy_old_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("thu mua lại sản phẩm cũ")

        return


class ActionHowManyPerMonth(Action):
    # action cần trả bao nhiêu tiền 1 tháng
    def name(self) -> Text:
        return "action_how_many_per_month"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        try:
            productName = productNameAnalysis(
                next(tracker.get_latest_entity_values(entity_type="product_name")))
        except:
            pass
        if productName:
            sqlQuery = "select * from fptshop.dienthoai where ten like '%{}%'".format(
                productName)
            laisuat = ''
            prepay_percent = 0
            tgian_tragop = 0
            tratruoc = 0
            try:
                tgian_tragop = InstallmentPaymentPeriod(
                    next(tracker.get_latest_entity_values(entity_type='installment_payment_period')))
            except:
                pass
            try:
                tratruoc = priceAnalysis(next(tracker.get_latest_entity_values(
                    entity_type='price', entity_role='prepay')))
            except:
                pass
            try:
                prepay_percent = PrepayPercent(
                    next(tracker.get_latest_entity_values(entity_type='prepay_percent')))
            except:
                pass
            try:
                laisuat = next(tracker.get_latest_entity_values(
                    entity_type='interest_rate'))
            except:
                pass
            data = getData(sqlQuery)
            gia_goc = int(data[0]['gia'])
            tienno = 0
            tienthang = 0
            prepay = 0
            if laisuat:
                pass
            else:
                laisuat = 1.66/100
            if tratruoc:
                tienno = gia_goc - tratruoc
                prepay = tratruoc
            if prepay_percent:
                tienno = gia_goc*(100 - prepay_percent)/100
                prepay = prepay_percent
            if tgian_tragop == 0:
                tgian_tragop = 4
            tienthang = tienno/tgian_tragop + tienno*laisuat
            tienthang = RoundNum(int(tienthang))
            message_str = "Trả góp trả trước {}\nTrả trong {} tháng\nThì mỗi tháng phải trả {}".format(
                prepay, tgian_tragop, tienthang)
            print(gia_goc)
            print(tratruoc)
            dispatcher.utter_message(message_str)
        else:
            dispatcher.utter_message('action_how_many_per_month')
        return


class ActionCaseHowManyPerMonth(Action):
    # action cần trả bao nhiêu tiền 1 tháng trong 2 trường hợp
    def name(self) -> Text:
        return "action_case_how_many_per_month"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("this is test")
        return


class ActionIsProductCanBuyOnInstallment(Action):
    # action sản phẩm có được mua trả góp hay không
    def name(self) -> Text:
        return "action_is_product_can_buy_on_installment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        try:
            productName = productNameAnalysis(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            pass
        if productName:
            sqlQuery = "select * from fptshop.dienthoai where ten like '%{}%'".format(
                productName)
            data = getData(sqlQuery)
            if data[0]['url_installment']:
                gia = int(data[0]['gia'])
                tienno = gia*70/100
                tienthang = tienno/4 + tienno*1.66/100
                message_str = "Sản phẩm {} có hỗ trợ trả góp. Bạn có thể tham khảo gói trả góp sau.\n  Trả trước 30%.\nTrả góp trong 4 tháng.\nMỗi tháng trả {}.\n*Lưu ý: Số liệu trên đây chỉ mang tính chất tham khảo.\nĐể biết thêm chi tiết về các gói trả góp của {} bạn có thể truy cập trang web sau. {}".format(
                    data[0]['ten'], tienthang, data[0]['ten'], data[0]['url_installment'])
                dispatcher.utter_message(message_str)
        else:
            dispatcher.utter_message('message_str')

        return


class ActionHarwareInfo(Action):
    # action thông tin chi tiết phần cứng
    def name(self) -> Text:
        return "action_hardware_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            productName = productNameAnalysis(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            pass
        try:
            hardware_name = next(tracker.get_latest_entity_values(
                entity_type='hardware', entity_role='WHQ'))
            role = "WHQ"
        except StopIteration:
            pass
        try:
            hardware_name = next(tracker.get_latest_entity_values(
                entity_type='hardware', entity_role='YorN'))
            role = "YorN"
        except StopIteration:
            pass
        sqlQuery = 'select * from fptshop.dienthoai where ten like "%{}%"'.format(
            productName)
        data = getData(sqlQuery)
        if data:
            hardware_label = data[0]['label'].split('/')
            hardware_data = data[0]['data'].split('/')
            temp = -1
            for item in hardware_label:
                if item.find(hardware_name) > -1:
                    temp = hardware_label.index(item)
                    break
            if hardware_data[temp] == "không" or hardware_data[temp] is None:
                message_str = Hardware(hardware_name, role, 'no')
            else:
                message_str = Hardware(hardware_name, role, 'yes')
        else:
            message_str = "Không tìm thấy sản phẩm!"

        dispatcher.utter_message(message_str)
        return


class ActionMainCamera(Action):
    # action thông tin về camera sau
    def name(self) -> Text:
        return "action_main_camera"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        most_recent_state = tracker.current_state()
        print(most_recent_state)
        dispatcher.utter_message('demo')

        return


class ActionSelfieCamera(Action):
    # action thông tin camera trước
    def name(self) -> Text:
        return "action_selfie_camera"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("this is test")

        return


class ActionResolutionCamera(Action):
    # action thông tin độ phân giải của cả camera trước và sau
    def name(self) -> Text:
        return "action_resolution_camrea"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("this is test")

        return


class ActionGuarantee(Action):
    # action thông tin bảo hành
    def name(self) -> Text:
        return "action_guarantee"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            productName = productNameAnalysis(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            pass
        sqlQuery = 'select * from fptshop.dienthoai where ten like "%{}%"'.format(
            productName)
        data = getData(sqlQuery)
        if data:
            i = -1
            temp = data[0]['label'].split('/')
            value = data[0]['data'].split('/')
            for item in temp:
                if item.find('bảo hành') > -1:
                    i = temp.index(item)
                    break
            if value[i]:
                message_str = "Thời gian bảo hành của sản phẩm là: {}.\nTrong thời gian bảo hành nếu sản phẩm có phát sinh lỗi thì bạn có thể mang sản phẩm đến cửa hàng để được sửa chữa miễn phí ngoại trừ các trường hợp sau: Sản phẩm bị rơi vỡ, ngấm dung dịch chất lỏng(nước,vv),cấn, móp do va đập.".format(
                    value[i])
            else:
                message_str = "Sản phẩm này hiện không có thông tin bảo hành."
        else:
            message_str = "Không tim thấy thông tin sản phẩm"
        dispatcher.utter_message(message_str)
        return


class ActionPromotionsAndGift(Action):
    # action thông tin khuyến mãi và quà tặng
    def name(self) -> Text:
        return "action_promotions_and_gift"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        try:
            productName = productNameAnalysis(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            pass
        if productName:
            sqlQuery = "select * from fptshop.dienthoai where ten like '%{}%'".format(
                productName)
            data = getData(sqlQuery)
            if data:
                ten = data[0]['ten']
                khuyen_mai = data[0]['khuyen_mai']
                message_str = "Các khuyến mãi của sản phẩm {} là:\n{}".format(
                    ten, khuyen_mai.replace("Xem chi tiết", ""))

        dispatcher.utter_message(message_str)
        return


class ActionFindProduct(Action):
    # action tìm kiếm 1 sản phẩm
    def name(self) -> Text:
        return "action_find_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        try:
            productName = productNameAnalysis(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            pass
        if productName:
            sqlQuery = "Select * from fptshop.dienthoai where ten like '%{}%'".format(
                productName)
            try:
                ram = romramAnalysis(
                    next(tracker.get_latest_entity_values(entity_type='ram')))
                sqlQuery = sqlQuery + "and ram like '%{}%'".format(ram)
            except:
                pass
            try:
                rom = romramAnalysis(
                    next(tracker.get_latest_entity_values(entity_type='rom')))
                sqlQuery = sqlQuery + "and rom like '%{}%'".format(rom)
            except:
                pass
            sqlQuery = sqlQuery + "limit 9;"
            result = getData(sqlQuery)
            if result:
                list_item = []
                for item in result:
                    list_btn = [ButtonTemplate("Xem chi tiết", "Cấu hình của {} như thế nào".format(
                        item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia = "Giá: {}".format(item['gia'])
                    else:
                        gia = "Đang cập nhật"
                    mess_item = TemplateItems(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(
                    text="Giá nè", json_message=message_str)
            else:
                dispatcher.utter_message(
                    "Không tìm thấy sản phẩm. Vui lòng thử lại")
            print(sqlQuery)
        else:
            dispatcher.utter_message(
                "Không tìm thấy sản phẩm vui lòng thử lại sau")

        return


class ActionFindAnotherProduct(Action):
    # action tìm kiếm 1 bản khác
    def name(self) -> Text:
        return "action_find_another_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        try:
            productName = productNameAnalysis(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            pass
        if productName:
            sqlQuery = "Select * from fptshop.dienthoai where ten like '%{}%'".format(
                productName)
            try:
                ram = romramAnalysis(
                    next(tracker.get_latest_entity_values(entity_type='ram')))
                sqlQuery = sqlQuery + "and ram like '%{}%'".format(ram)
            except:
                pass
            try:
                rom = romramAnalysis(
                    next(tracker.get_latest_entity_values(entity_type='rom')))
                sqlQuery = sqlQuery + "and rom like '%{}%'".format(rom)
            except:
                pass
            sqlQuery = sqlQuery + "limit 9;"
            result = getData(sqlQuery)
            if result:
                list_item = []
                for item in result:
                    list_btn = [ButtonTemplate("Xem chi tiết", "Cấu hình của {} như thế nào".format(
                        item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia = "Giá: {}".format(item['gia'])
                    else:
                        gia = "Đang cập nhật"
                    mess_item = TemplateItems(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(
                    text="Giá nè", json_message=message_str)
            else:
                dispatcher.utter_message(
                    "Không tìm thấy sản phẩm. Vui lòng thử lại")
            print(sqlQuery)
        else:
            dispatcher.utter_message(
                "Không tìm thấy sản phẩm vui lòng thử lại sau")

        return


class ActionGreet(Action):
    # action lấy tên của người dùng facebook
    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        page_acess_token = 'EAAXU2UZANCBcBAGnKBsT6ETH2nWZCjDEDqNa7OFqKEiO1KalIoeTc70TKdqhbq1pE5ZCMwIAnZCvVy4K8RgmL6BZAlBRuyyvWCQ35HeuZAN1kAt5XgghErQRL1FpipDQ0TMFOSNspIXPLJ5CoZAyg7Wu0ZBFPDMe5dBsbMi0B3sA3gZDZD'
        current_state = tracker.current_state()
        sender_id = current_state['sender_id']
        r = requests.get('https://graph.facebook.com/{}?fields=first_name,last_name,profile_pic&access_token={}'.format(sender_id,page_acess_token)).json()
        first_name = r['first_name']
        last_name = r['last_name']
        tracker.SlotSet('first_name', first_name)
        tracker.SlotSet('last_name', last_name)
        message_str = "Xin chào bạn {} {}. Mình có thể giúp gì cho bạn?".format(last_name,first_name)
        dispatcher.utter_message(message_str)
        return
