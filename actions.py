# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
#region import
from typing import Any, Text, Dict, List
import time
import re
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType
from rasa_sdk.events import FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
from rasa.core.trackers import DialogueStateTracker
from InputModify import priceModify
from InputModify import productNameModify
from InputModify import romRamModify
from InputModify import PrepayPercentModify
from InputModify import InstallmentPaymentPeriod
from InputModify import RoundNum
from InputModify import GetColName
from dbConnect import getData
from CreateJsonMessageTemplate import GenericTemplate
from CreateJsonMessageTemplate import ButtonPostbackTemplate
from CreateJsonMessageTemplate import ItemsTemplate
from CreateJsonMessageTemplate import HardwareAnswer
from CreateJsonMessageTemplate import QuickReply
from CreateJsonMessageTemplate import BackToList
#endregion
#

class ActionSessionStarted(Action):
    def name(self):
        return "action_session_start"
    async def run(self, dispatcher, tracker, domain):
        events = [SessionStarted()]
        message = "test session start"
        dispatcher.utter_message(message)
        events.append(ActionExecuted("action_listen"))
        return events

class ActionCustomFallback(Action):

    def name(self) -> Text:
        return "action_custom_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        time_temp = time.localtime()
        tgian = time.strftime("%d/%m/%Y, %H:%M:%S", time_temp)
        dispatcher.utter_message(text="Hiện tại mình chưa có khả năng trả lời câu này. Mình sẽ cập nhật thêm kiến thức để trả lời cho bạn vào lần tới.")

        temp = tracker.latest_message.get('text')
        log = ""
        # log = tracker.get_latest_entity_values.get('role')
        if temp:
            log = temp
        else:
            log = "Khách hàng gửi icon hoặc bỏ trống!"
        conversation_log = "Thời gian: {}\nNội dung khách hàng gửi: {}\n--------------------------\n".format(
            tgian, log)
        # print(conversation_log)
        fobj = open('LOG/log.txt', 'a', encoding='utf-8')
        fobj.write(conversation_log)
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
        sqlQuery =""
        dispatcher.utter_message(res)
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        return


class ActionProductPrice(Action):
    # action trả lời giá sản phẩm
    def name(self) -> Text:
        return "action_product_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        Pname_temp = ""
        sqlQuery = ""
        getMess=''
        ram=''
        rom=''
        message=''
        #region try-cath entity
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = productNameModify(tracker.get_slot('product_name'))
            pass
        #endregion
        if productName:
            sqlQuery = "Select * from dienthoai where ten like '%{}%'".format(
                productName)
            #region try-catch ram/rom
            try:
                ram = romRamModify(
                    next(tracker.get_latest_entity_values(entity_type='ram')))
                sqlQuery = sqlQuery + "and ram like '%{}%'".format(ram)
            except:
                pass
            try:
                rom = romRamModify(
                    next(tracker.get_latest_entity_values(entity_type='rom')))
                sqlQuery = sqlQuery + "and rom like '%{}%'".format(rom)
            except:
                pass
            #endregion
            sqlQuery = sqlQuery + "order by ten limit 9;"
            data = getData(sqlQuery)
            if data:
                getMess = tracker.latest_message.get('text')
                list_item = []
                for item in data:
                    list_btn = [ButtonPostbackTemplate("Xem chi tiết", "Cấu hình của {}".format(
                        item['ten'])), ButtonPostbackTemplate("Đặt mua", 'đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia = "Giá: {:,} vnđ".format(item['gia'])
                    else:
                        gia = "Sản phẩm tin đồn"
                    mess_item = ItemsTemplate(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)
                message = GenericTemplate(list_item)
                message_str = "Danh sách sản phẩm có tên là {} hoặc tương tự".format(productName)
            else:
                message_str = "Hiện tại của hàng không có thông tin về sản phẩm {} ".format(productName)
                if ram:
                    message_str = message_str + "ram {} ".format(ram)
                if rom:
                    message_str = message_str + 'rom {} '.format(rom)
                message_str = message_str + "hay các sản phẩm có tên tương tự. Mong bạn thông cảm và thử tìm kiếm sản phẩm khác."
                Pname_temp = productName
        else:
            message_str = "Bạn đang hỏi thông tin về giá của sản phẩm nào ạ?"
        dispatcher.utter_message(text = message_str,json_message=message)
        # print(getMess)
        print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),Pname_temp))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp),SlotSet('get_list',getMess)]


class ActionOnlinePrice(Action):
    # action trả lời giá online
    def name(self) -> Text:
        return "action_online_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        Pname_temp = ""
        sqlQuery =""
        getMess =''
        #region try-catch pname
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = productNameModify(tracker.get_slot('product_name'))
            pass
        #endregion
        if productName:
            sqlQuery = "Select * from dienthoai where ten like '%{}%'".format(
                productName)
            #region try-catch ram/rom
            try:
                ram = romRamModify(
                    next(tracker.get_latest_entity_values(entity_type='ram')))
                sqlQuery = sqlQuery + "and ram like '%{}%'".format(ram)
            except:
                pass
            try:
                rom = romRamModify(
                    next(tracker.get_latest_entity_values(entity_type='rom')))
                sqlQuery = sqlQuery + "and rom like '%{}%'".format(rom)
            except:
                pass
            #endregion
            sqlQuery = sqlQuery + "order by ten limit 9 ;"
            data = getData(sqlQuery)
            if data:
                getMess = tracker.latest_message.get('text')
                list_item = []
                for item in data:
                    list_btn = [ButtonPostbackTemplate("Xem chi tiết", "Cấu hình của {}".format(
                        item['ten'])), ButtonPostbackTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia_online']:
                        gia = "Giá online: {:,} vnđ".format(item['gia_online'])
                    else:
                        gia = "Giá online: Đang cập nhật"
                    mess_item = ItemsTemplate(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(
                    text="Giá bán online của sản phẩm {} và các sản phẩm có tên tương tự".format(productName), json_message=message_str)
            else:
                dispatcher.utter_message(
                    "Hiện tại của hàng không có thông tin về sản phẩm {} hay các sản phẩm có tên tương tự. Mong bạn thông cảm và thử tìm kiếm sản phẩm khác.".format(productName))
                Pname_temp = productName
        else:
            dispatcher.utter_message(
                "Bạn đang hỏi thông tin về giá bán online của sản phẩm nào ạ?")
        print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),Pname_temp))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp),SlotSet('get_list',getMess)]


class ActionOldProduct(Action):
    # action trả lời giá của sản phẩm cũ
    def name(self) -> Text:
        return "action_old_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        Pname_temp = ""
        sqlQuery =""
        getMess=''
        #region try-catch pname
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = productNameModify(tracker.get_slot('product_name'))
            pass
        #endregion
        if productName:
            sqlQuery = "Select * from dienthoai where ten like '%{}%'".format(
                productName)
            #region try-catch ram/rom
            try:
                ram = romRamModify(
                    next(tracker.get_latest_entity_values(entity_type='ram')))
                sqlQuery = sqlQuery + "and ram like '%{}%'".format(ram)
            except:
                pass
            try:
                rom = romRamModify(
                    next(tracker.get_latest_entity_values(entity_type='rom')))
                sqlQuery = sqlQuery + "and rom like '%{}%'".format(rom)
            except:
                pass
            #endregion
            sqlQuery = sqlQuery + "order by ten limit 9;"
            data = getData(sqlQuery)
            if data:
                getMess = tracker.latest_message.get('text')
                list_item = []
                for item in data:
                    list_btn = [ButtonPostbackTemplate("Xem chi tiết", "Cấu hình của {}".format(
                        item['ten'])), ButtonPostbackTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['ghi_chu'].find('tin đồn') > -1:
                        gia = "Sản phẩm tin đồn"
                    else:
                        gia = "Giá cũ: {:,} vnđ".format(item['gia_cu'])
                    mess_item = ItemsTemplate(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(
                    text="Giá của sản phẩm {} đã qua sử dụng hoặc các sản phẩm có tên tương tự.".format(productName), json_message=message_str)
            else:
                dispatcher.utter_message(
                    "Hiện tại của hàng không có thông tin về sản phẩm {} hay các sản phẩm có tên tương tự. Mong bạn thông cảm và thử tìm kiếm sản phẩm khác.".format(productName))
                Pname_temp = productName
        else:
            dispatcher.utter_message(
                "Bạn đang hỏi thông tin về giá của sản phẩm nào ạ?")
        print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),Pname_temp))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp),SlotSet('get_list',getMess)]


class ActionProductConfiguration(Action):
    # action trả lời cấu hình của sản phẩm
    def name(self) -> Text:
        return "action_product_configuration"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        Pname_temp = ""
        sqlQuery =""
        message = ""
        temp_mess = tracker.get_slot('get_list')
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = productNameModify(tracker.get_slot('product_name'))
            pass
        if productName:
            sqlQuery = 'select * from dienthoai where ten like "%{}%"'.format(productName)
            #region try-catch
            try:
                ram = romRamModify(
                    next(tracker.get_latest_entity_values(entity_type='ram')))
                sqlQuery = sqlQuery + " and ram like '%{}%'".format(ram)
            except:
                pass
            try:
                rom = romRamModify(
                    next(tracker.get_latest_entity_values(entity_type='rom')))
                sqlQuery = sqlQuery + " and rom like '%{}%'".format(rom)
            except:
                pass
            #endregion
            sqlQuery = sqlQuery + ' ORDER by ten'
            data = getData(sqlQuery)
            if data:
                Pname_temp = data[0]['ten']
                if data[0]['ghi_chu'] == "Sản phẩm tin đồn":
                    message_str = "Sản phẩm {} chỉ là tin đồn. Bên mình sẽ thông báo cho bạn biết khi có thêm thông tin của sản phẩm. Xin cảm ơn.".format(Pname_temp)
                    message=BackToList(temp_mess)
                else:
                    man_hinh = "{},{},{}.".format(data[0]['chuan_man_hinh'], data[0]['cong_nghe_man_hinh'], data[0]['do_phan_giai'])
                    camera_truoc = data[0]['do_phan_giai_cam_truoc']
                    camera_sau = data[0]['do_phan_giai_cam_sau']
                    ram = data[0]['ram']
                    rom = data[0]['rom']
                    cpu = "{},{} nhân, tốc độ {}.".format(data[0]['chipset'], data[0]['so_nhan'], data[0]['toc_do_cpu'])
                    gpu = data[0]['gpu']
                    pin = data[0]['dung_luong_pin']
                    message_str = "Thông tin của sản phẩm: {}.\nMàn hình :{}\nCamera trước:{}\nCamera sau:{}\nRam:{}\nBộ nhớ trong:{} \nCPU: {}\nGPU:{} \nDung lượng pin:{}".format(Pname_temp,man_hinh,camera_truoc,camera_sau,ram,rom,cpu,gpu,pin)
                    message = QuickReply(self.name(),temp_mess)
                    # dispatcher.utter_message(text = message_str,json_message = message)
            else:
                message_str = "Hiện tại cửa hàng không có thông tin của sản phẩm {} mong bạn thông cảm!".format(productName)
                Pname_temp = productName
        else:
            message_str = "Bạn đang hỏi thông tin cấu hình của sản phẩm nào ạ?"
        # dispatcher.utter_message(message_str)
        # print('mess list' + temp_mess)
        dispatcher.utter_message(text=message_str,json_message=message)
        print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),Pname_temp))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]


class ActionTypeOfProduct(Action):
    # action trả lời các hãng điện thoại sẵn có
    def name(self) -> Text:
        return "action_type_of_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sqlQuery = "select * from hangdienthoai limit 9;"
        data = getData(sqlQuery)
        if data:
            list_item = []
            for item in data:
                list_btn = [ButtonPostbackTemplate("Danh sách điện thoại của {}".format(
                    item['ten']), "Danh sách điện thoại của {}".format(item['ten']))]
                template_item = ItemsTemplate(
                    item['ten'], item['url_logo'], item['ten'], list_btn)
                list_item.append(template_item)
            message_str = GenericTemplate(list_item)
            dispatcher.utter_message(json_message=message_str)
        else:
            dispatcher.utter_message(
                "Không có danh sách hãng điện thoại để hiển thị!")
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        return


class ActionListProduct(Action):
    # action trả lời danh sách các sản phẩm của 1 hãng
    def name(self) -> Text:
        return "action_list_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_company = ""
        sqlQuery =""
        getMess=''
        try:
            product_company = next(tracker.get_latest_entity_values(
                entity_type="product_company"))
        except:
            pass
        if product_company:
            sqlQuery = "Select dienthoai.ten,dienthoai.gia,dienthoai.url_img from dienthoai,hangdienthoai where dienthoai.idhangdienthoai = hangdienthoai.idHangDienThoai and  hangdienthoai.ten like '%{}%' ORDER by dienthoai.gia DESC limit 9;".format(
                product_company)
            data = getData(sqlQuery)
            if data:
                getMess = tracker.latest_message.get('text')
                list_item = []
                for item in data:
                    list_btn = [ButtonPostbackTemplate("Xem cấu hình", "Cấu hình của {}".format(
                        item['ten'])), ButtonPostbackTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia = "Giá: {:,} vnđ".format(item['gia'])
                    else:
                        gia = "Đang cập nhật"
                    mess_item = ItemsTemplate(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(text="Danh sách điện thoại của {}".format(
                    product_company), json_message=message_str)
            else:
                dispatcher.utter_message("Không có điện thoại nào của hãng {} để hiển thị. Vui lòng thử lại sau.".format(product_company))
                pass
        else:
            dispatcher.utter_message(
                "Không tìm thấy hãng điện thoại bạn vừa nhập, vui lòng thử lại")
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        return[SlotSet('get_list',getMess)]


class ActionCheckPrice(Action):
    # action kiểm tra giá sản phẩm
    def name(self) -> Text:
        return "action_check_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        price = 0
        sqlQuery =""
        try:
            price = priceModify(
                next(tracker.get_latest_entity_values(entity_type='price')))
        except:
            pass
        if price != 0:
            productName = ""
            try:
                productName = productNameModify(
                    next(tracker.get_latest_entity_values(entity_type='product_name')))
            except:
                productName = productNameModify(tracker.get_slot('product_name'))
                pass
            if productName:
                sqlQuery = "Select * from dienthoai where ten like '%{}%'".format(
                    productName)
                try:
                    ram = romRamModify(
                        next(tracker.get_latest_entity_values(entity_type='ram')))
                    sqlQuery = sqlQuery + "and ram like '%{}%'".format(ram)
                except:
                    pass
                try:
                    rom = romRamModify(
                        next(tracker.get_latest_entity_values(entity_type='rom')))
                    sqlQuery = sqlQuery + "and rom like '%{}%'".format(rom)
                except:
                    pass
                sqlQuery = sqlQuery + "order by ten limit 9;"
                data = getData(sqlQuery)
                if data:
                    Pname_temp = data[0]['ten']
                    for item in data:
                        if item['gia'] == price:
                            message_str = "Dạ đúng rồi ạ. Giá của sản phẩm {} là {:,} vnđ ạ.".format(item['ten'], item['gia'])
                        else:
                            message_str = "Dạ không phải ạ. Giá của sản phẩm {} là {:,} vnđ ạ.".format(item['ten'], item['gia'])
                else:
                    Pname_temp = productName
                    message_str = "Hiện tại cửa hàng không còn hỗ trợ cho sản phẩm {} nữa ạ. Mong bạn thông cảm.".format(productName)
            else:
                message_str = "Bạn đang hỏi hỏi giá của sản phẩm nào ạ?"
            dispatcher.utter_message(message_str)
            print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),Pname_temp))
            return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]


class ActionFindProductInRangePrice(Action):
    # action tìm kiếm sản phẩm trong 1 khoảng giá
    def name(self) -> Text:
        return "action_find_product_in_range_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        from_price = 0
        to_price = 0
        try:
            from_price = priceModify(next(tracker.get_latest_entity_values(
                entity_type='price', entity_role='from_price')))
        except:
            pass
        try:
            to_price = priceModify(next(tracker.get_latest_entity_values(
                entity_type='price', entity_role='to_price')))
        except:
            pass
        sqlQuery =""
        if from_price and to_price and from_price != to_price:
            if from_price > to_price:
                text = "Danh sách sản phẩm có giá từ {:,} vnđ đến {:,} vnđ".format(
                    to_price, from_price)
                sqlQuery = "select * from dienthoai where gia between {} and {} order by gia desc limit 9".format(
                    to_price, from_price)
            else:
                text = "Danh sách sản phẩm có giá từ {:,} vnđ đến {:,} vnđ".format(
                    from_price, to_price)
                sqlQuery = "select * from dienthoai where gia between {} and {} order by gia desc limit 9".format(
                    from_price, to_price)
            data = getData(sqlQuery)
            if data:
                list_item = []
                getMess=tracker.latest_message.get('text')
                for item in data:
                    list_btn = [ButtonPostbackTemplate("Xem chi tiết", "Cấu hình của {}".format(
                        item['ten'])), ButtonPostbackTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia = "Giá: {}".format(item['gia'])
                    else:
                        gia = "Đang cập nhật"
                    mess_item = ItemsTemplate(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)
                message_str = GenericTemplate(list_item)
            else:
                text = "Hiện tại chúng tôi không có sản phẩm nào trong mức giá mà bạn đưa ra. Vui lòng thử một mức giá khác."
        else:
            text = "Hiện tại chúng tôi không có sản phẩm nào trong mức giá mà bạn đưa ra. Vui lòng thử một mức giá khác."
        dispatcher.utter_message(text=text, json_message=message_str)
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        return[SlotSet('get_list',getMess)]


class ActionFindProductLowerPrice(Action):
    # action tìm sản phấm dưới 1 mức giá
    def name(self) -> Text:
        return "action_find_product_lower_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        price = 0
        product_company = ''
        sqlQuery = ""
        try:
            product_company = next(tracker.get_latest_entity_values(entity_type='product_company'))
        except:
            pass
        try:
            price = priceModify(
                next(tracker.get_latest_entity_values(entity_type='price')))
        except:
            pass
        print(price)
        if price != 0:
            sqlQuery = "select dienthoai.ten,dienthoai.gia,dienthoai.url_img from dienthoai,hangdienthoai where dienthoai.idhangdienthoai = hangdienthoai.idHangDienThoai and gia <= {} ".format(
                price)
            if product_company:
                sqlQuery = sqlQuery + "and hangdienthoai.ten like '%{}%' ".format(product_company)

            sqlQuery = sqlQuery + " order by gia desc limit 9"
            data = getData(sqlQuery)
            if data:
                list_item = []
                for item in data:
                    list_btn = [ButtonPostbackTemplate("Xem chi tiết", "Cấu hình của {}".format(
                        item['ten'])), ButtonPostbackTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = "Giá: {:,} vnđ".format(item['gia'])
                    mess_item = ItemsTemplate(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                text = "Danh sách một số sản phẩm có giá dưới {:,} vnđ".format(price)
                dispatcher.utter_message(text=text,json_message=message_str)
            else:
                dispatcher.utter_message("Hiện tại cửa hàng không có sản phẩm nào dưới {:,} vnđ bạn vui lòng thử lại với mức giá khác. Xin cảm ơn".format(price))
        else:
            dispatcher.utter_message("Mức giá bạn đưa ra không chính xác, vui lòng thử lại.")
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        return


class ActionFindProductUpperPrice(Action):
    # action tìm sản phẩm trên 1 mức giá
    def name(self) -> Text:
        return "action_find_product_upper_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        price = 0
        product_company = ''
        sqlQuery = ""
        try:
            product_company = next(tracker.get_latest_entity_values(entity_type='product_company'))
        except:
            pass
        try:
            price = priceModify(
                next(tracker.get_latest_entity_values(entity_type='price')))
        except:
            pass
        if price != 0:
            sqlQuery = "select dienthoai.ten,dienthoai.gia,dienthoai.url_img from dienthoai,hangdienthoai where dienthoai.idhangdienthoai = hangdienthoai.idHangDienThoai and gia >= {} ".format(
                price)
            if product_company:
                sqlQuery = sqlQuery + "and hangdienthoai.ten like '%{}%' ".format(product_company)

            sqlQuery = sqlQuery + " order by gia asc limit 9"
            data = getData(sqlQuery)
            if data:
                list_item = []
                for item in data:
                    list_btn = [ButtonPostbackTemplate("Xem chi tiết", "Cấu hình của {}".format(
                        item['ten'])), ButtonPostbackTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = "Giá: {:,} vnđ".format(item['gia'])
                    mess_item = ItemsTemplate(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                text = "Danh sách một số sản phẩm có giá trên {:,} vnđ".format(price)
                dispatcher.utter_message(text=text,json_message=message_str)
            else:
                dispatcher.utter_message("Hiện tại cửa hàng không có sản phẩm nào dưới {:,} vnđ bạn vui lòng thử lại với mức giá khác. Xin cảm ơn".format(price))
        else:
            dispatcher.utter_message("Mức giá bạn đưa ra không chính xác, vui lòng thử lại.")
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        return


class ActionFindProductAroundPrice(Action):
    # action tìm sản phẩm quanh 1 mức giá
    def name(self) -> Text:
        return "action_find_product_around_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        price = 0
        sqlQuery =""
        product_company = ''
        #region try-catch 
        try:
            price = priceModify(
                next(tracker.get_latest_entity_values(entity_type='price')))
        except:
            pass
        try:
            product_company = next(tracker.get_latest_entity_values(entity_type='product_company'))
        except:
            pass
        #endregion
        if price != 0:
            p1 = price - 300000
            p2 = price + 700000
            sqlQuery = "select dienthoai.ten,dienthoai.gia,dienthoai.url_img from dienthoai,hangdienthoai where dienthoai.idhangdienthoai = hangdienthoai.idHangDienThoai and gia between {} and {}".format(
                p1, p2)
            if product_company:
                sqlQuery = sqlQuery + " and hangdienthoai.ten like '%{}%'".format(product_company)

            sqlQuery = sqlQuery + " order by gia desc limit 9"
            data = getData(sqlQuery)
            if data:
                list_item = []
                for item in data:
                    list_btn = [ButtonPostbackTemplate("Xem chi tiết", "Cấu hình của {}".format(
                        item['ten'])), ButtonPostbackTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia = "Giá: {:,} vnđ".format(item['gia'])
                    else:
                        gia = "Đang cập nhật"
                    mess_item = ItemsTemplate(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(json_message=message_str)
            else:
                dispatcher.utter_message("Thông tin bạn yêu cầu chưa chính xác, vui lòng kiểm tra lại!")
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        return


class ActionScreenInfo(Action):
    # action thông tin màn hình
    def name(self) -> Text:
        return "action_scree_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        sqlQuery = ""
        Pname_temp = ""
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = productNameModify(tracker.get_slot('product_name'))
            pass
        if productName:
            sqlQuery = 'select * from dienthoai where ten like "%{}%"'.format(productName)
            data = getData(sqlQuery)
            if data[0]['ghi_chu'] == "Sản phẩm tin đồn":
                message_str = "Sản phẩm {} mới chỉ là tin đồn. Bên cửa hàng sẽ thông báo cho bạn khi có thông tin mới về sản phẩm này ạ.".format(data[0]['ten'])
            else:
                Pname_temp = data[0]['ten']
                message_str = "Sản phẩm {} sử dụng màn hình: {} {} với độ phân giải {}".format(data[0]['ten'],data[0]['cong_nghe_man_hinh'],data[0]['chuan_man_hinh'],data[0]['do_phan_giai'])
        else:
            message_str = "Bạn đang hỏi thông tin màn hình của sản phẩm nào vậy ạ?"
        dispatcher.utter_message(message_str)
        print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),Pname_temp))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]


class ActionPinInfo(Action):
    # action thông tin về pin
    def name(self) -> Text:
        return "action_pin_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = productNameModify(tracker.get_slot('product_name'))
            pass
        Pname_temp = ""
        if productName:
            sqlQuery = "Select * from dienthoai where ten like '%{}%'".format(
                productName)
            data = getData(sqlQuery)
            if data:
                if data[0]['ghi_chu'] == "Sản phẩm tin đồn":
                    message_str = "Sản phẩm {} mới chỉ là tin đồn. Bên cửa hàng sẽ thông báo cho bạn khi có thông tin mới về sản phẩm này ạ.".format(data[0]['ten'])
                else:
                    Pname_temp = data[0]['ten']
                    loai_pin = data[0]['loai_pin']
                    dung_luong_pin = data[0]['dung_luong_pin']
                    thoi_gian_dam_thoai = data[0]['thoi_gian_dam_thoai']
                    message_str = "Sản phẩm {} sử dụng pin: {} , có dung lượng: {} cho thời gian đàm thoại lên tới {}".format(productName,loai_pin,dung_luong_pin,thoi_gian_dam_thoai)
            else:
                Pname_temp = productName
                message_str = "Hiên tại cửa hàng chúng tôi không có thông tin về sản phẩm {}. Mong bạn thông cảm."
        else:
            message_str = "Bạn đang hỏi thông tin về pin của sản phẩm nào ạ?"
        print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),Pname_temp))
        dispatcher.utter_message(message_str)
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]


class ActionAcquisitionOldProduct(Action):
    # action thu mua lại sản phẩm cũ
    def name(self) -> Text:
        return "action_acquisition_old_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        sqlQuery =""
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = productNameModify(tracker.get_slot('product_name'))
            pass
        Pname_temp = ""
        if productName:
            sqlQuery = "select * from dienthoai where ten like '%{}%'".format(productName)
            data = getData(sqlQuery)
            if data:
                if data[0]['ghi_chu'] == "Sản phẩm tin đồn":
                    message_str = "Sản phẩm {} mới chỉ là tin đồn. Bên cửa hàng sẽ thông báo cho bạn khi có thông tin mới về sản phẩm này ạ.".format(data[0]['ten'])
                else:
                    Pname_temp = data[0]['ten']
                    gia = int(data[0]['gia'])
                    temp = int(gia*75/100)
                    gia_mua_lai = RoundNum(temp)
                    message_str = "Đối với sản phẩm {} còn trong thời gian bảo hành, không bị rơi vỡ, cấn móp do va đập hay ngấm các dung dịch chất lỏng như nước v.v thì bên cửa hàng sẽ mua lại sản phẩm với giá khoảng 75% giá bán ra tức là khoảng {:,} vnđ ạ.".format(data[0]['ten'],gia_mua_lai)
            else:
                Pname_temp = productName
                message_str = "Hiện cửa hàng không cung cấp dịch vụ cho sản phẩm {} nữa ạ. Mong bạn thông cảm.".format(productName)
        else:
            message_str = "Bạn đang hỏi thông tin thu mua cũ cho sản phẩm nào ạ?"
        print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),Pname_temp))
        dispatcher.utter_message(message_str)
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]


class ActionHowManyPerMonth(Action):
    # action cần trả bao nhiêu tiền 1 tháng
    def name(self) -> Text:
        return "action_pay_per_month"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #region try-catch entity
        productName = ""
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type="product_name")))
        except:
            pass
        #endregion
        Pname_temp = ""
        sqlQuery =""
        if productName:
            sqlQuery = "select * from dienthoai where ten like '%{}%'".format(
                productName)
            laisuat = ''
            prepay_percent = 0
            tgian_tragop = 0
            message_str =''
            tratruoc = 0
            #region try catch entity
            try:
                tgian_tragop = InstallmentPaymentPeriod(
                    next(tracker.get_latest_entity_values(entity_type='installment_payment_period')))
            except:
                print(next(tracker.get_latest_entity_values(entity_type='installment_payment_period')))
                pass
            try:
                tratruoc = priceModify(next(tracker.get_latest_entity_values(
                    entity_type='price', entity_role='prepay')))
            except:
                pass
            try:
                prepay_percent = PrepayPercentModify(
                    next(tracker.get_latest_entity_values(entity_type='prepay_percent')))
            except:
                pass
            try:
                laisuat = next(tracker.get_latest_entity_values(
                    entity_type='interest_rate'))
            except:
                pass
            #endregion
            data = getData(sqlQuery)
            if data:
                if data[0]['ghi_chu'] == "Sản phẩm tin đồn":
                    message_str = "Sản phẩm {} mới chỉ là tin đồn. Bên cửa hàng sẽ thông báo cho bạn khi có thông tin mới về sản phẩm này ạ.".format(data[0]['ten'])
                elif data[0]['url_installment'].find('tra-gop') >-1:
                    Pname_temp = data[0]['ten']
                    gia_goc = int(data[0]['gia'])
                    tienno = 0
                    tienthang = 0
                    prepay = ""
                    if laisuat:
                        pass
                    else:
                        laisuat = 1.66/100
                    if tratruoc:
                        tienno = gia_goc - tratruoc
                        prepay = "{:,} vnđ".format(tratruoc)
                    if prepay_percent:
                        tienno = gia_goc*(100 - prepay_percent)/100
                        prepay = "{}%".format(prepay_percent)
                    else:
                        tienno = gia_goc*70/100
                        prepay = "30%"
                    if tgian_tragop == 0:
                        tgian_tragop = 4
                    tienthang = tienno/tgian_tragop + tienno*laisuat
                    tienthang = RoundNum(int(tienthang))
                    message_str = "Đối với sản phẩm {}:\nTrả góp trả trước {}\nTrả trong {} tháng\nThì mỗi tháng phải trả {:,} vnđ".format(Pname_temp,
                        prepay, tgian_tragop, tienthang)
                else:
                    message_str = "Sản phẩm {} hiện đang không hỗ trợ trả góp. Mong bạn thông cảm!".format(productName)
                    Pname_temp = productName
        else:
            message_str = 'Bạn đang hỏi thông tin số tiền góp hàng tháng cho sản phẩm nào ạ!'
        print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),Pname_temp))
        dispatcher.utter_message(message_str)
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]


class ActionCaseHowManyPerMonth(Action):
    # action cần trả bao nhiêu tiền 1 tháng trong 2 trường hợp
    def name(self) -> Text:
        return "action_case_pay_per_month"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sqlQuery =""
        dispatcher.utter_message("this is test")
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
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
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            pass
        Pname_temp = ""
        sqlQuery =""
        if productName:
            sqlQuery = "select * from dienthoai where ten like '%{}%'".format(
                productName)
            data = getData(sqlQuery)
            if data:
                if data[0]['ghi_chu'] == "Sản phẩm tin đồn":
                    message_str = "Sản phẩm {} mới chỉ là tin đồn. Bên cửa hàng sẽ thông báo cho bạn khi có thông tin mới về sản phẩm này ạ.".format(data[0]['ten'])
                else:
                    if data[0]['url_installment']:
                        Pname_temp = data[0]['ten']
                        gia = int(data[0]['gia'])
                        tienno = gia*70/100
                        tmp = tienno/4 + tienno*1.66/100
                        tienthang = RoundNum(int(tmp))
                        message_str = "Sản phẩm {} có hỗ trợ trả góp. Bạn có thể tham khảo gói trả góp sau:  \n  Trả trước 30%.  \nTrả góp trong 4 tháng.  \nMỗi tháng trả {:,} vnđ.  \n*Lưu ý: Số liệu trên đây chỉ mang tính chất tham khảo.  \nĐể biết thêm chi tiết về các gói trả góp của {} bạn có thể truy cập trang web sau. {}".format(
                            data[0]['ten'], tienthang, data[0]['ten'], data[0]['url_installment'])
                    else:
                        message_str = "Sản phẩm {} hiện tại chưa hỗ trợ trả góp. Mong bạn thông cảm.".format(productName)
            else:
                Pname_temp = productName
        else:
            message_str ='Bạn đang hỏi thông tin trả góp của sản phẩm nào ạ?'
        dispatcher.utter_message(message_str)
        print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),Pname_temp))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]


class ActionHarwareInfo(Action):
    # action thông tin chi tiết phần cứng
    def name(self) -> Text:
        return "action_hardware_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        sqlQuery = ""
        Pname_temp = ""
        hardware_name= ""
        #region try-catch entity
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = tracker.get_slot('product_name')
            pass
        try:
            hardware_name = next(tracker.get_latest_entity_values(
                entity_type='hardware', entity_role='WHQ'))
            role = "WHQ"
        except:
            pass
        try:
            hardware_name = next(tracker.get_latest_entity_values(
                entity_type='hardware', entity_role='YorN'))
            role = "YorN"
        except:
            pass
        #endregion
        if productName:
            sqlQuery = 'select * from dienthoai where ten like "%{}%"'.format(
                productName)
            data = getData(sqlQuery)
            if data:
                if data[0]['ghi_chu'].find('tin đồn')>-1:
                    message_str = "Sản phẩm {0} chỉ là tin đồn. Cửa hàng sẽ thông báo cho bạn thông tin mới nhất về sản phẩm {0} khi được cập nhật.".format(data[0]['ten'])
                else:
                    col = GetColName(hardware_name.lower())
                    Pname_temp = data[0]['ten']
                    temp = data[0][col]
                    YNQ = 'yes'
                    value = temp
                    if temp.lower() == 'không' or temp is None or temp.lower()=='đang cập nhật':
                        YNQ = 'no'
                    if role == 'YorN':
                        value = hardware_name

                    message_str = HardwareAnswer(value,role,YNQ)
            else:
                Pname_temp = productName
                message_str = "Hiện tại cửa hàng của chúng tôi không có thông tin về sản phẩm {}. Vui lòng thử tìm kiếm sản phẩm khác.".format(productName)
        else:
            message_str = "Bạn đang hỏi thông tin của sản phẩm nào ạ?"
        dispatcher.utter_message(message_str)
        print("--------------\n{}\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),Pname_temp,hardware_name))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]

class ActionTakePhotoEraseBackground(Action):
    # action thông tin về camera sau
    def name(self) -> Text:
        return "action_take_photo_erase_background"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sqlQuery = ""
        Pname_temp = ""
        productName = ""
        #region try-catch entity
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = productNameModify(tracker.get_slot('product_name'))
            pass
        #endregion
        if productName:
            sqlQuery = "select * from dienthoai where ten like '%{}%'".format(productName)
            data = getData(sqlQuery)
            if data:
                Pname_temp = data[0]['ten']
                if data[0]['ghi_chu'].find('tin đồn') > -1:
                    message_str = "Sản phẩm {0} chỉ là tin đồn. Cửa hàng sẽ thông báo cho bạn thông tin mới nhất về sản phẩm {0} khi được cập nhật.".format(data[0]['ten'])
                else:
                    chup_anh = data[0]['chup_anh_nang_cao']
                    if chup_anh.find('xóa phông') > -1:
                        message_str = "Sản phẩm {} có hỗ trở chụp ảnh xóa phông ạ.".format(Pname_temp)
                    else:
                        message_str = "Sản phẩm {} không hỗ trở chụp ảnh xóa phông ạ.".format(Pname_temp)
            else:
                Pname_temp = productName
                message_str = "Hiện tại cửa hàng của chúng tôi không có thông tin về sản phẩm {}. Vui lòng thử tìm kiếm sản phẩm khác.".format(productName)
        else:
            message_str = "Bạn đang hỏi thông tin chụp ảnh xóa phông của sản phẩm nào ạ?"
        dispatcher.utter_message(message_str)
        print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),Pname_temp))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]

class ActionMainCamera(Action):
    # action thông tin về camera sau
    def name(self) -> Text:
        return "action_main_camera"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sqlQuery = ""
        Pname_temp = ""
        productName = ""
        #region try-catch entity
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = productNameModify(tracker.get_slot('product_name'))
            pass
        #endregion
        if productName:
            sqlQuery = "select * from dienthoai where ten like '%{}%'".format(productName)
            data = getData(sqlQuery)
            if data:
                Pname_temp = data[0]['ten']
                if data[0]['ghi_chu'].find('tin đồn') > -1:
                    message_str = "Sản phẩm {0} chỉ là tin đồn. Cửa hàng sẽ thông báo cho bạn thông tin mới nhất về sản phẩm {0} khi được cập nhật.".format(data[0]['ten'])
                else:
                    do_phan_giai = "Đang cập nhật."
                    chup_anh = "Đang cập nhật."
                    if data[0]['do_phan_giai_cam_sau']:
                        do_phan_giai = data[0]['do_phan_giai_cam_sau']
                    if data[0]['chup_anh_nang_cao']:
                        chup_anh = data[0]['chup_anh_nang_cao']
                    message_str = "Sản phẩm {} có hệ thống camera sau với độ phân giải: {}\n Và các chức năng hỗ trợ chụp ảnh: {}.".format(Pname_temp,do_phan_giai,chup_anh)
            else:
                Pname_temp = productName
                message_str = "Hiện tại cửa hàng của chúng tôi không có thông tin về sản phẩm {}. Vui lòng thử tìm kiếm sản phẩm khác.".format(productName)
        else:
            message_str = "Bạn đang hỏi thông tin camera sau của sản phẩm nào ạ?"
        dispatcher.utter_message(message_str)
        print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),Pname_temp))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]


class ActionSelfieCamera(Action):
    # action thông tin camera trước
    def name(self) -> Text:
        return "action_selfie_camera"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sqlQuery = ""
        Pname_temp = ""
        productName = ""
        #region try-catch entity
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = productNameModify(tracker.get_slot('product_name'))
            pass
        #endregion
        if productName:
            sqlQuery = "select * from dienthoai where ten like '%{}%'".format(productName)
            data = getData(sqlQuery)
            if data:
                Pname_temp = data[0]['ten']
                if data[0]['ghi_chu'].find('tin đồn')>-1:
                    message_str = "Sản phẩm {0} chỉ là tin đồn. Cửa hàng sẽ thông báo cho bạn thông tin mới nhất về sản phẩm {0} khi được cập nhật.".format(data[0]['ten'])
                else:
                    do_phan_giai = "Đang cập nhật."
                    if data[0]['do_phan_giai_cam_truoc']:
                        do_phan_giai = data[0]['do_phan_giai_cam_truoc']
                    message_str = "Sản phẩm {} có hệ thống camera trước với độ phân giải: {}.".format(Pname_temp,do_phan_giai)
            else:
                Pname_temp = productName
                message_str = "Hiện tại cửa hàng của chúng tôi không có thông tin về sản phẩm {}. Vui lòng thử tìm kiếm sản phẩm khác.".format(productName)
        else:
            message_str = "Bạn đang hỏi thông tin camera trước của sản phẩm nào ạ?"
        dispatcher.utter_message(message_str)
        print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),Pname_temp))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]


class ActionResolutionCamera(Action):
    # action thông tin độ phân giải của cả camera trước và sau
    def name(self) -> Text:
        return "action_resolution_camrea"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        sqlQuery = ""
        Pname_temp = ""
        productName = ""
        loai_camera = ""
        #region try-catch entity
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = productNameModify(tracker.get_slot('product_name'))
            pass
        try:
            loai_camera = next(tracker.get_latest_entity_values(entity_type='camera'))
        except:
            loai_camera = tracker.get_slot('loai_camera')
            pass
        #endregion
        if productName:
            sqlQuery = "select * from dienthoai where ten like '%{}%'".format(productName)
            data = getData(sqlQuery)
            if data:
                Pname_temp = data[0]['ten']
                if data[0]['ghi_chu'].find('tin đồn')>-1:
                    message_str = "Sản phẩm {0} chỉ là tin đồn. Cửa hàng sẽ thông báo cho bạn thông tin mới nhất về sản phẩm {0} khi được cập nhật.".format(data[0]['ten'])
                else:
                    if loai_camera.find('trước') > -1:
                        message_str = "Sản phẩm {} có camera trước với độ phân giải: {}. Với các tính năng: {}".format(Pname_temp,data[0]['do_phan_giai_cam_truoc'],data[0]['thong_tin_khac'])
                    else:
                        message_str = "Sản phẩm {} có camera sau với độ phân giải: {}. Với các tính năng chụp ảnh nâng cao: {}. Hỗ trợ quay phim: {}".format(Pname_temp,data[0]['do_phan_giai_cam_sau'],data[0]['chup_anh_nang_cao'],data[0]['quay_phim'])
            else:
                Pname_temp = productName
                message_str = "Hiện tại cửa hàng của chúng tôi không có thông tin về sản phẩm {}. Vui lòng thử tìm kiếm sản phẩm khác.".format(productName)
        else:
            message_str = "Bạn đang hỏi thông tin {} của sản phẩm nào ạ?".format(loai_camera)
        dispatcher.utter_message(message_str)
        print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),Pname_temp))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp),SlotSet('loai_camera',loai_camera)]


class ActionGuarantee(Action):
    # action thông tin bảo hành
    def name(self) -> Text:
        return "action_guarantee"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #region try-catch entity
        productName = ""
        message = ""
        Pname_temp=""
        temp_mess = tracker.get_slot('get_list')
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = tracker.get_slot('product_name')
            pass
        #endregion
        if productName:
            sqlQuery = 'select * from dienthoai where ten like "%{}%"'.format(
                productName)
            data = getData(sqlQuery)
            if data:
                if data[0]['ghi_chu'] == "Sản phẩm tin đồn":
                    message_str = "Sản phẩm {} mới chỉ là tin đồn. Bên cửa hàng sẽ thông báo cho bạn khi có thông tin mới về sản phẩm này ạ.".format(data[0]['ten'])
                    message = BackToList(temp_mess)
                elif data[0]['thoi_gian_bao_hanh']:
                    Pname_temp = data[0]['ten']
                    message_str = "Thời gian bảo hành của {} là: {}".format(productName,data[0]['thoi_gian_bao_hanh'])
                    message = QuickReply(self.name(),temp_mess)
                    # dispatcher.utter_message(text = message_str,json_message = message)
            else:
                Pname_temp = productName
                message_str = "Hiện cửa hàng không có thông tin về sản phẩm {}. Mong bạn thông cảm!"
        else:
            message_str = "Bạn đang hỏi thông tin bảo hành của sản phẩm nào ạ?"
        # dispatcher.utter_message(message_str)
        dispatcher.utter_message(text = message_str,json_message = message)
        print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),Pname_temp))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]


class ActionPromotionsAndGift(Action):
    # action thông tin khuyến mãi và quà tặng
    def name(self) -> Text:
        return "action_promotions_and_gift"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        sqlQuery = ""
        message= ''
        Pname_temp =""
        temp_mess = tracker.get_slot('get_list')
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = productNameModify(tracker.get_slot('product_name'))
            pass
        if productName:
            sqlQuery = "select * from dienthoai where ten like '%{}%'".format(
                productName)
            data = getData(sqlQuery)
            if data:
                if data[0]['ghi_chu'] == "Sản phẩm tin đồn":
                    message_str = "Sản phẩm {} mới chỉ là tin đồn. Bên cửa hàng sẽ thông báo cho bạn khi có thông tin mới về sản phẩm này ạ.".format(data[0]['ten'])
                    message = BackToList(temp_mess)
                elif data[0]['khuyen_mai']:
                    Pname_temp = data[0]['ten']
                    khuyen_mai = data[0]['khuyen_mai']
                    message_str = "Hiện sản phẩm {} đang có các chương trình khuyến mãi như sau:\n{}".format(
                        Pname_temp, khuyen_mai)
                    message = QuickReply(self.name(),temp_mess)
                    # dispatcher.utter_message(text = message_str,json_message = message)
            else:
                # Pname_temp = productName
                message_str = "Sản phẩm {} hiện không có khuyến mãi nào. Xin cảm ơn".format(Pname_temp)
        else:
            message_str = "Bản đang hỏi thông tin khuyến mãi của sản phẩm nào ạ?"
        # dispatcher.utter_message(message_str)
        dispatcher.utter_message(text = message_str,json_message = message)
        print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),Pname_temp))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]


class ActionFindProduct(Action):
    # action tìm kiếm 1 sản phẩm
    def name(self) -> Text:
        return "action_find_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        message_str=""
        ram =''
        rom =''
        sqlQuery = "Select * from dienthoai where 1=1 "
        message_text = "Danh sách sản phẩm có "
        #region try-catch entity
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
            sqlQuery = sqlQuery + "and ten like '%{}%'".format(productName)
            message_text = message_text + "tên là {} ".format(productName)
        except:
            pass
        try:
            ram = romRamModify(
                next(tracker.get_latest_entity_values(entity_type='ram')))
            sqlQuery = sqlQuery + "and ram like '%{}%'".format(ram)
            message_text = message_text + "ram {} ".format(ram)
        except:
            pass
        try:
            rom = romRamModify(
                next(tracker.get_latest_entity_values(entity_type='rom')))
            sqlQuery = sqlQuery + "and rom like '%{}%'".format(rom)
            message_text = message_text + "rom {} ".format(rom)
        except:
            pass
        #endregion
        sqlQuery = sqlQuery + "order by ten limit 9;"
        if not productName and not ram and not rom:
            sqlQuery = ''
        data = getData(sqlQuery)
        if data:
            list_item = []
            for item in data:
                list_btn = [ButtonPostbackTemplate("Xem cấu hình", "Cấu hình của {}".format(
                    item['ten'])), ButtonPostbackTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                gia = ""
                if item['gia']:
                    gia = "Giá: {:,} vnđ".format(item['gia'])
                else:
                    gia = "Sản phẩm tin đồn"
                mess_item = ItemsTemplate(
                    item['ten'], item['url_img'], gia, list_btn)
                list_item.append(mess_item)

            message_str = GenericTemplate(list_item)
        else:
            message_text ="Cửa hàng mình hiện không có thông tin bạn đang tìm kiếm. Vui lòng thử lại!"
        dispatcher.utter_message(text=message_text,json_message=message_str)
        print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),productName))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',productName)]


class ActionFindAnotherProduct(Action):
    # action tìm kiếm 1 bản khác
    def name(self) -> Text:
        return "action_find_another_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        sqlQuery=''
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = tracker.get_slot('product_name')
            pass
        if productName:
            sqlQuery = "Select * from dienthoai where ten like '%{}%'".format(
                productName)
            #region try-catch entity
            try:
                ram = romRamModify(
                    next(tracker.get_latest_entity_values(entity_type='ram')))
                sqlQuery = sqlQuery + "and ram like '%{}%'".format(ram)
            except:
                pass
            try:
                rom = romRamModify(
                    next(tracker.get_latest_entity_values(entity_type='rom')))
                sqlQuery = sqlQuery + "and rom like '%{}%'".format(rom)
            except:
                pass
            #endregion
            sqlQuery = sqlQuery + "order by ten limit 9;"
            result = getData(sqlQuery)
            if result:
                list_item = []
                for item in result:
                    list_btn = [ButtonPostbackTemplate("Xem chi tiết", "Cấu hình của {}".format(
                        item['ten'])), ButtonPostbackTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia = "Giá: {}".format(item['gia'])
                    else:
                        gia = "Đang cập nhật"
                    mess_item = ItemsTemplate(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(
                    text="Giá nè", json_message=message_str)
            else:
                dispatcher.utter_message(
                    "Không tìm thấy sản phẩm. Vui lòng thử lại!")
            # print(sqlQuery)
        else:
            dispatcher.utter_message(
                "Không tìm thấy sản phẩm vui lòng thử lại sau!")
        print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),productName))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',productName)]


class ActionGreet(Action):
    # action lấy tên của người dùng facebook
    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        page_acess_token = 'EAAXU2UZANCBcBANnYJDZC5vT9kCKoZCYd0NWV9fdF6aK7vHiunQWn2VxDxBE91FVS2QOfF1YDXQcXsCNTGXsVUGqfs5MYFqW0jh8Qp7EmoTaQmJCOyYjDnO1472eJqybz88nJLwlbZAwJo7ZCvkRiRxvfa27LmCdIHspJ1byrAfF7ZCZBxUCoPi'
        current_state = tracker.current_state()
        sender_id = current_state['sender_id']
        r = requests.get('https://graph.facebook.com/{}?fields=first_name,last_name,profile_pic&access_token={}'.format(sender_id,page_acess_token)).json()
        first_name = r['first_name']
        last_name = r['last_name']
        message_str = "Xin chào bạn {} {}. Mình có thể giúp gì cho bạn?".format(last_name,first_name)
        dispatcher.utter_message(message_str)
        print("--------------\n{}\n{} {}\n-----------".format(self.name(),first_name,last_name))
        return[SlotSet('first_name',first_name),SlotSet('last_name',last_name)]

class ActionGetCustName(Action):
    # action lấy tên khách hàng
    def name(self) -> Text:
        return "action_get_customer_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("this is test")
        sqlQuery=""
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        return

class ActionGetPhoneNum(Action):
    # action lấy sđt
    def name(self) -> Text:
        return "action_get_phone_number"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("this is test")
        sqlQuery = ""
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        return

class ActionGetContact(Action):
    # action thông tin liên hệ gồm tên + sđt
    def name(self) -> Text:
        return "action_get_contact"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("this is test")
        sqlQuery = ""
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        return

class ActionFollow(Action):
    # action follow intent
    def name(self) -> Text:
        return "action_follow"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: DialogueStateTracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        previus_action = tracker.get_slot('latest_action')
        sqlQuery = ""
        productName = ""
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            pass
        print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),productName))
        if productName:
            sqlQuery = "select * from dienthoai where ten like '%{}%' order by ten".format(productName)
            data = getData(sqlQuery)
            print("--------------\n{}\n{}\n-----------".format(self.name(),previus_action))
            if data:
                Pname_temp = data[0]['ten']
                if previus_action is not None:
                    return[SlotSet('product_name',Pname_temp),FollowupAction(name=previus_action)]
            else:
                return[FollowupAction("action_find_product")]
        else:
            Pname_temp = productName
            dispatcher.utter_message('Vui lòng nhập tên sản phẩm bạn muốn tìm hiểu thông tin!')
            return[SlotSet('product_name',Pname_temp),FollowupAction("action_find_product")]

class ActionOptionInBox(Action):
    # action thông tin khuyến mãi và quà tặng
    def name(self) -> Text:
        return "action_option_in_box"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        sqlQuery = ""
        Pname_temp =""
        message = ''
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = productNameModify(tracker.get_slot('product_name'))
            pass
        if productName:
            sqlQuery = "select * from dienthoai where ten like '%{}%'".format(
                productName)
            #region try-catch ram/rom
            try:
                ram = romRamModify(
                    next(tracker.get_latest_entity_values(entity_type='ram')))
                sqlQuery = sqlQuery + "and ram like '%{}%'".format(ram)
            except:
                pass
            try:
                rom = romRamModify(
                    next(tracker.get_latest_entity_values(entity_type='rom')))
                sqlQuery = sqlQuery + "and rom like '%{}%'".format(rom)
            except:
                pass
            #endregion
            data = getData(sqlQuery)
            if data:
                if data[0]['ghi_chu'] == "Sản phẩm tin đồn":
                    message_str = "Sản phẩm {} mới chỉ là tin đồn. Bên cửa hàng sẽ thông báo cho bạn khi có thông tin mới về sản phẩm này ạ.".format(data[0]['ten'])
                elif data[0]['box']:
                    Pname_temp = data[0]['ten']
                    box = data[0]['box']
                    message_str = "Khi mua sản phẩm {} đi kèm có có:\n{}".format(
                        Pname_temp, box)
                    temp_mess = tracker.get_slot('get_list')
                    message = QuickReply(self.name(),temp_mess)
                    # dispatcher.utter_message(text = message_str,json_message = message)
                else:
                    message_str = "Không có thông tin về phụ kiện kèm theo hộp của sản phẩm {}.".format(
                        productName)
            else:
                Pname_temp = productName
                message_str = "Sản phẩm {} hiện không có thông tin về các phụ kiện trong hộp. Xin cảm ơn".format(Pname_temp)
        else:
            message_str = "Bản đang hỏi thông tin của sản phẩm nào ạ?"
        # dispatcher.utter_message(message_str)
        dispatcher.utter_message(text = message_str,json_message = message)
        print("--------------\n{}\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'),Pname_temp))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]

class ActionCanPlayGame(Action):
    # action thông tin khuyến mãi và quà tặng
    def name(self) -> Text:
        return "action_can_play_game"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        sqlQuery = ""
        # Pname_temp =""
        #region try-catch
        try:
            productName = productNameModify(next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = tracker.get_slot('product_name')
        if productName:
            sqlQuery ='select * from dienthoai where ten like "%{}%" order by ten'.format(productName)
            data = getData(sqlQuery)
            if data:
                if data[0]['ghi_chu'].find('tin đồn') >-1:
                    message_str = "Sản phẩm {} hiện mới chỉ là tin đồn. Mình sẽ cập nhật thêm khi có thông tin mới. Xin vui lòng thử sản phẩm khác."
                else:
                    if data[0]['choi_game']:
                        message_str = 'Sản phẩm {} có hỗ trợ chơi các game như Liên quân mobile hay PUBG mobile ạ.'.format(data[0]['ten'])
                    else:
                        message_str = 'Sản phẩm {} không hỗ trợ chơi các game ạ.'.format(data[0]['ten'])
            else:
                message_str = 'Không tìm thấy thông tin của sản phẩm {}, vui lòng kiểm tra lại.'.format(productName)
        else:
            message_str ='Bạn đang tìm kiếm thông tin của sản phẩm nào ạ?'

        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text'))) 
        dispatcher.utter_message(message_str) 
        return

class ActionWaterproof(Action):
    # action chống nước
    def name(self) -> Text:
        return "action_waterproof"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: DialogueStateTracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Pname_temp = ""
        sqlQuery = ''
        productName =''
        try:
            productName = productNameModify(next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = tracker.get_slot('product_name')
        if productName:
            sqlQuery = 'select * from dienthoai where ten like "%{}%" order by ten'.format(productName)
            data = getData(sqlQuery)
            if data:
                Pname_temp = data[0]['ten']
                if data[0]['ghi_chu'].find('tin đồn') >-1:
                    message_str = "Sản phẩm {} mới chỉ là tin đồn, mình sẽ cập nhật khi có thông tin mới.".format(Pname_temp)
                else:
                    if re.search(r"có|chuẩn",data[0]['chong_nuoc']) or re.search(r"chống nước",data[0]['chuc_nang_khac']):
                        message_str = "Sản phẩm {} có khả năng chống nước, tuy nhiên bạn không nên để sản phẩm ngâm trong nước quá lâu. Nên lau sạch và làm khô sản phẩm nếu có dính nước.".format(Pname_temp)
                    else:
                        message_str = "Sản phẩm {} không có khả năng chống nước. Bạn không nên để sản phẩm rơi xuống nước hay đổ nước lên sản phẩm. Nên lau sạch và làm khô sản phẩm nếu có dính nước.".format(Pname_temp)
            else:
                message_str = 'Hiện tại mình không có thông tin sản phẩm bạn đang tìm. Vui lòng thử tìm kiếm sản phẩm khác. Xin cảm ơn!'
                Pname_temp = productName
        else:
            message_str = "Bạn đang hỏi thông tin của sản phẩm nào ạ?"
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        dispatcher.utter_message(message_str)
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]