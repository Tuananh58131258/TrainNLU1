# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import time
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
from inputAnalysis import priceAnalysis
from inputAnalysis import productNameAnalysis
from inputAnalysis import romramAnalysis
from dbConnect import getData
from makemessage import GenericTemplate
from makemessage import ButtonTemplate
from makemessage import TemplateItems
#
#
class ActionCustomFallback(Action):

    def name(self) -> Text:
        return "action_custom_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        time_temp  = time.localtime()
        tgian = time.strftime("%d/%m/%Y, %H:%M:%S", time_temp)
        dispatcher.utter_message(text="Fallback fallback")
        
        temp = tracker.latest_message.get('text')
        log =""
        # log = tracker.get_latest_entity_values.get('role')
        if temp:
            log = temp
        else: log = "Khách hàng gửi icon hoặc bỏ trống!"
        convertion_log = "Thời gian: {}\nNội dung khách hàng gửi: {}\n--------------------------\n".format(tgian,log)
        # print(convertion_log)
        fobj = open('LOG/log.txt','a', encoding='utf-8')
        fobj.write(convertion_log)
        fobj.close()
        return [UserUtteranceReverted()]

class ActionTestST(Action):

    def name(self) -> Text:
        return "action_test_st"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        des =""
        role = ""
        try:
            des = next(tracker.get_latest_entity_values(entity_type='hardware',entity_role='WHQ'))
            role = "WHQ"
        except StopIteration:
            pass
        try:
            des = next(tracker.get_latest_entity_values(entity_type='hardware',entity_role='YorN'))
            role = "YorN"
        except StopIteration:
            pass
        res = "entity value : {}, role: {}".format(des,role)
        dispatcher.utter_message(res)
        return 

class ActionProductPrice(Action):
# action trả lời giá sản phẩm
    def name(self) -> Text:
        return "action_product_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName =""
        try:
            productName = productNameAnalysis(next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            pass
        if productName:
            sqlQuery = "Select * from fptshop.dienthoai where ten like '%{}%'".format(productName)
            try:
                ram = romramAnalysis(next(tracker.get_latest_entity_values(entity_type='ram')))
                sqlQuery =  sqlQuery + "and ram like '%{}%'".format(ram)
            except:
                pass
            try:
                rom = romramAnalysis(next(tracker.get_latest_entity_values(entity_type='rom')))
                sqlQuery =  sqlQuery + "and rom like '%{}%'".format(rom)
            except:
                pass
            sqlQuery = sqlQuery + "limit 9;"
            result = getData(sqlQuery)
            if result:
                list_item = []
                for item in result:
                    list_btn = [ButtonTemplate("Xem chi tiết","Cấu hình của {} như thế nào".format(item['ten'])),ButtonTemplate("Đặt mua",'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia  = "Giá: {}".format(item['gia'])
                    else:
                        gia = "Đang cập nhật"
                    mess_item = TemplateItems(item['ten'],item['url_img'],gia,list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(text="Giá nè", json_message=message_str)
            else:
                dispatcher.utter_message("Không tìm thấy sản phẩm. Vui lòng thử lại")
            print(sqlQuery)
        else:
            dispatcher.utter_message("Không tìm thấy sản phẩm vui lòng thử lại sau")
        return

class ActionOnlinePrice(Action):
# action trả lời giá online
    def name(self) -> Text:
        return "action_online_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName =""
        try:
            productName = productNameAnalysis(next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            pass
        if productName:
            sqlQuery = "Select * from fptshop.dienthoai where ten like '%{}%'".format(productName)
            try:
                ram = romramAnalysis(next(tracker.get_latest_entity_values(entity_type='ram')))
                sqlQuery =  sqlQuery + "and ram like '%{}%'".format(ram)
            except:
                pass
            try:
                rom = romramAnalysis(next(tracker.get_latest_entity_values(entity_type='rom')))
                sqlQuery =  sqlQuery + "and rom like '%{}%'".format(rom)
            except:
                pass
            sqlQuery = sqlQuery + "limit 9;"
            result = getData(sqlQuery)
            if result:
                list_item = []
                for item in result:
                    list_btn = [ButtonTemplate("Xem chi tiết","Cấu hình của {} như thế nào".format(item['ten'])),ButtonTemplate("Đặt mua",'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia_online']:
                        gia  = "Giá online: {}".format(item['gia_online'])
                    else:
                        gia = "Giá online: Đang cập nhật"
                    mess_item = TemplateItems(item['ten'],item['url_img'],gia,list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(text="Giá nè", json_message=message_str)
            else:
                dispatcher.utter_message("Không tìm thấy sản phẩm. Vui lòng thử lại")
            print(sqlQuery)
        else:
            dispatcher.utter_message("Không tìm thấy sản phẩm vui lòng thử lại sau")
        return

class ActionOldProduct(Action):
# action trả lời giá của sản phẩm cũ
    def name(self) -> Text:
        return "action_old_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName =""
        try:
            productName = productNameAnalysis(next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            pass
        if productName:
            sqlQuery = "Select * from fptshop.dienthoai where ten like '%{}%'".format(productName)
            try:
                ram = romramAnalysis(next(tracker.get_latest_entity_values(entity_type='ram')))
                sqlQuery =  sqlQuery + "and ram like '%{}%'".format(ram)
            except:
                pass
            try:
                rom = romramAnalysis(next(tracker.get_latest_entity_values(entity_type='rom')))
                sqlQuery =  sqlQuery + "and rom like '%{}%'".format(rom)
            except:
                pass
            sqlQuery = sqlQuery + "limit 9;"
            result = getData(sqlQuery)
            if result:
                list_item = []
                for item in result:
                    list_btn = [ButtonTemplate("Xem chi tiết","Cấu hình của {} như thế nào".format(item['ten'])),ButtonTemplate("Đặt mua",'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia_cu']:
                        gia  = "Giá cũ: {}".format(item['gia_cu'])
                    else:
                        gia = "Giá cũ: Đang cập nhật"
                    mess_item = TemplateItems(item['ten'],item['url_img'],gia,list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(text="Giá nè", json_message=message_str)
            else:
                dispatcher.utter_message("Không tìm thấy sản phẩm. Vui lòng thử lại")
            print(sqlQuery)
        else:
            dispatcher.utter_message("Không tìm thấy sản phẩm vui lòng thử lại sau")
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
                list_btn = [ButtonTemplate("Danh sách điện thoại của {}".format(item['ten']),"Danh sách điện thoại của {}".format(item['ten']))]
                template_item = TemplateItems(item['ten'],item['url_logo'],item['ten'],list_btn)
                list_item.append(template_item)
            message_str = GenericTemplate(list_item)
            dispatcher.utter_message(json_message=message_str)
        except:
            dispatcher.utter_message("Không có danh sách hãng điện thoại để hiển thị!")
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
            product_company = next(tracker.get_latest_entity_values(entity_type="product_company"))
        except:
            pass
        if product_company:
            sqlQuery = "Select * from fptshop.dienthoai where ten like '%{}%' limit 9;".format(product_company)
            try:
                data = getData(sqlQuery)
                list_item = []
                for item in data:
                    list_btn = [ButtonTemplate("Xem chi tiết","Cấu hình của {} như thế nào".format(item['ten'])),ButtonTemplate("Đặt mua",'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia  = "Giá: {}".format(item['gia'])
                    else:
                        gia = "Đang cập nhật"
                    mess_item = TemplateItems(item['ten'],item['url_img'],gia,list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(text="Danh sách điện thoại của {}".format(product_company), json_message=message_str)
            except:
                print(sqlQuery)
                pass
        else:
            dispatcher.utter_message("Không tìm thấy hãng điện thoại bạn vừa nhập, vui lòng thử lại")
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
            price = priceAnalysis(next(tracker.get_latest_entity_values(entity_type='price')))
        except:
            pass
        if price != 0:
            productName =""
            try:
                productName = productNameAnalysis(next(tracker.get_latest_entity_values(entity_type='product_name')))
            except:
                pass
            if productName:
                sqlQuery = "Select * from fptshop.dienthoai where ten like '%{}%'".format(productName)
                try:
                    ram = romramAnalysis(next(tracker.get_latest_entity_values(entity_type='ram')))
                    sqlQuery =  sqlQuery + "and ram like '%{}%'".format(ram)
                except:
                    pass
                try:
                    rom = romramAnalysis(next(tracker.get_latest_entity_values(entity_type='rom')))
                    sqlQuery =  sqlQuery + "and rom like '%{}%'".format(rom)
                except:
                    pass
                sqlQuery = sqlQuery + "limit 9;"
                data = getData(sqlQuery)
                for item in data:
                    if item['gia'] == price:
                        dispatcher.utter_message("Dạ đúng rồi ạ. Giá của sản phẩm {} là {} ạ.".format(item['ten'],item['gia']))
                    else:
                        dispatcher.utter_message("Dạ không phải ạ. Giá của sản phẩm {} là {} ạ.".format(item['ten'],item['gia']))
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
            from_price = priceAnalysis(tracker.get_latest_entity_values(entity_type='price',entity_role='from_price'))
        except:
            pass
        try:
            to_price = priceAnalysis(tracker.get_latest_entity_values(entity_type='price',entity_role='to_price'))
        except:
            pass
        if from_price and to_price and from_price != to_price: 
            if from_price > to_price:
                text = "Danh sách sản phẩm có giá từ {} đến {}".format(to_price,from_price)
                sqlQuery = "select * from fptshop.dienthoai where gia between {} and {} limit 9".format(to_price,from_price)
            else:
                text = "Danh sách sản phẩm có giá từ {} đến {}".format(from_price,to_price)
                sqlQuery = "select * from fptshop.dienthoai where gia between {} and {} limit 9".format(from_price,to_price)
            data = getData(sqlQuery)
            list_item = []
            for item in data:
                list_btn = [ButtonTemplate("Xem chi tiết","Cấu hình của {} như thế nào".format(item['ten'])),ButtonTemplate("Đặt mua",'Đặt mua {}'.format(item['ten']))]
                gia = ""
                if item['gia']:
                    gia  = "Giá: {}".format(item['gia'])
                else:
                    gia = "Đang cập nhật"
                mess_item = TemplateItems(item['ten'],item['url_img'],gia,list_btn)
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
            price = priceAnalysis(next(tracker.get_latest_entity_values(entity_type='price')))
        except:
            pass
        if price:
            sqlQuery = "select * from fptshop.dienthoai where gia <= {} order by gia desc limit 9".format(price)
            try:
                data = getData(sqlQuery)
                list_item = []
                for item in data:
                    list_btn = [ButtonTemplate("Xem chi tiết","Cấu hình của {} như thế nào".format(item['ten'])),ButtonTemplate("Đặt mua",'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia  = "Giá: {}".format(item['gia'])
                    else:
                        gia = "Đang cập nhật"
                    mess_item = TemplateItems(item['ten'],item['url_img'],gia,list_btn)
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
            price = priceAnalysis(next(tracker.get_latest_entity_values(entity_type='price')))
        except:
            pass
        if price:
            sqlQuery = "select * from fptshop.dienthoai where gia >= {} order by gia asc limit 9".format(price)
            try:
                data = getData(sqlQuery)
                list_item = []
                for item in data:
                    list_btn = [ButtonTemplate("Xem chi tiết","Cấu hình của {} như thế nào".format(item['ten'])),ButtonTemplate("Đặt mua",'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia  = "Giá: {}".format(item['gia'])
                    else:
                        gia = "Đang cập nhật"
                    mess_item = TemplateItems(item['ten'],item['url_img'],gia,list_btn)
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
            price = priceAnalysis(next(tracker.get_latest_entity_values(entity_type='price')))
        except:
            pass
        if price:
            p1 = price - 500000
            p2 = price + 1000000
            sqlQuery = "select * from fptshop.dienthoai where gia between {} and {} order by gia asc limit 9".format(p1,p2)
            try:
                data = getData(sqlQuery)
                list_item = []
                for item in data:
                    list_btn = [ButtonTemplate("Xem chi tiết","Cấu hình của {} như thế nào".format(item['ten'])),ButtonTemplate("Đặt mua",'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia  = "Giá: {}".format(item['gia'])
                    else:
                        gia = "Đang cập nhật"
                    mess_item = TemplateItems(item['ten'],item['url_img'],gia,list_btn)
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
        dispatcher.utter_message("this is test")

        return

class ActionPinInfo(Action):
# action thông tin về pin
    def name(self) -> Text:
        return "action_pin_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("this is test")

        return

class ActionBuyOldProduct(Action):
# action thu mua lại sản phẩm cũ
    def name(self) -> Text:
        return "action_buy_old_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("this is test")

        return

class ActionHowManyPerMonth(Action):
# action cần trả bao nhiêu tiền 1 tháng
    def name(self) -> Text:
        return "action_how_many_per_month"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("this is test")

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
        dispatcher.utter_message("this is test")

        return

class ActionHarwareInfo(Action):
# action thông tin chi tiết phần cứng
    def name(self) -> Text:
        return "action_hardware_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("this is test")

        return

class ActionMainCamera(Action):
# action thông tin về camera sau
    def name(self) -> Text:
        return "action_main_camera"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("this is test")

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
        dispatcher.utter_message("this is test")

        return

class ActionPromotionsAndGift(Action):
# action thông tin khuyến mãi và quà tặng 
    def name(self) -> Text:
        return "action_promotions_and_gift"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("this is test")

        return

class ActionFindProduct(Action):
# action tìm kiếm 1 sản phẩm
    def name(self) -> Text:
        return "action_find_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("this is test")

        return

class ActionFindAnotherProduct(Action):
# action tìm kiếm 1 bản khác
    def name(self) -> Text:
        return "action_find_another_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("this is test")

        return