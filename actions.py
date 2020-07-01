# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
#region import
from typing import Any, Text, Dict, List
import time
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
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
from CreateJsonMessageTemplate import ButtonTemplate
from CreateJsonMessageTemplate import ItemsTemplate
from CreateJsonMessageTemplate import HardwareAnswer
#endregion
#


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
        #region try-cath entity
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = tracker.get_slot('product_name')
            pass
        #endregion
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
            sqlQuery = sqlQuery + "limit 9;"
            data = getData(sqlQuery)
            if data:
                list_item = []
                for item in data:
                    list_btn = [ButtonTemplate("Xem chi tiết", "Cấu hình của {}".format(
                        item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia = "Giá: {:,} vnđ".format(item['gia'])
                    else:
                        gia = "Sản phẩm tin đồn"
                    mess_item = ItemsTemplate(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(
                    text="Danh sách sản phẩm có tên là  {} hoặc tương tự".format(productName), json_message=message_str)
            else:
                dispatcher.utter_message(
                    "Hiện tại của hàng không có thông tin về sản phẩm {} hay các sản phẩm có tên tương tự. Mong bạn thông cảm và thử tìm kiếm sản phẩm khác.".format(productName))
                Pname_temp = productName
        else:
            dispatcher.utter_message(
                "Bạn đang hỏi thông tin về giá của sản phẩm nào ạ?")
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]


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
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = tracker.get_slot('product_name')
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
            sqlQuery = sqlQuery + "limit 9;"
            data = getData(sqlQuery)
            if data:
                list_item = []
                for item in data:
                    list_btn = [ButtonTemplate("Xem chi tiết", "Cấu hình của {}".format(
                        item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
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
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]


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
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = tracker.get_slot('product_name')
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
            sqlQuery = sqlQuery + "limit 9;"
            data = getData(sqlQuery)
            if data:
                list_item = []
                for item in data:
                    list_btn = [ButtonTemplate("Xem chi tiết", "Cấu hình của {}".format(
                        item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
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
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]


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
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = tracker.get_slot('product_name')
            pass
        if productName:
            sqlQuery = 'select * from dienthoai where ten like "%{}%"'.format(productName)
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
            data = getData(sqlQuery)
            if data:
                Pname_temp = data[0]['ten']
                if data[0]['ghi_chu'] == "Sản phẩm tin đồn":
                    message_str = "Sản phẩm {} chỉ là tin đồn. Bên mình sẽ thông báo cho bạn biết khi có thêm thông tin của sản phẩm. Xin cảm ơn.".format(Pname_temp)
                else:
                    man_hinh = "{},{},{}.".format(data[0]['chuan_man_hinh'], data[0]['cong_nghe_man_hinh'], data[0]['do_phan_giai'])
                    camera_truoc = data[0]['do_phan_giai_cam_truoc']
                    camera_sau = data[0]['do_phan_giai_cam_sau']
                    ram = data[0]['ram']
                    rom = data[0]['rom']
                    cpu = "{},{},{}.".format(data[0]['chipset'], data[0]['so_nhan'], data[0]['toc_do_cpu'])
                    gpu = data[0]['gpu']
                    pin = data[0]['dung_luong_pin']
                    message_str = "Thông tin của sản phẩm: {}.\nMàn hình :{}\nCamera trước:{}\nCamera sau:{}\nRam:{}\nBộ nhớ trong:{} \nCPU: {}\nGPU:{} \nDung lượng pin:{}".format(Pname_temp,man_hinh,camera_truoc,camera_sau,ram,rom,cpu,gpu,pin)
            else:
                message_str = "Hiện tại cửa hàng không có thông tin của sản phẩm {} mong bạn thông cảm!".format(productName)
                Pname_temp = productName
        else:
            message_str = "Bạn đang hỏi thông tin cấu hình của sản phẩm nào ạ?"
        dispatcher.utter_message(message_str)
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
                list_btn = [ButtonTemplate("Danh sách điện thoại của {}".format(
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
        dispatcher.utter_message("this is test")
        product_company = ""
        sqlQuery =""
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
                list_item = []
                for item in data:
                    list_btn = [ButtonTemplate("Xem cấu hình", "Cấu hình của {}".format(
                        item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
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
        return


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
                productName = tracker.get_slot('product_name')
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
                sqlQuery = sqlQuery + "limit 9;"
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
            print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
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
            from_price = priceModify(tracker.get_latest_entity_values(
                entity_type='price', entity_role='from_price'))
        except:
            pass
        try:
            to_price = priceModify(tracker.get_latest_entity_values(
                entity_type='price', entity_role='to_price'))
        except:
            pass
        sqlQuery =""
        if from_price and to_price and from_price != to_price:
            if from_price > to_price:
                text = "Danh sách sản phẩm có giá từ {} đến {}".format(
                    to_price, from_price)
                sqlQuery = "select * from dienthoai where gia between {} and {} limit 9".format(
                    to_price, from_price)
            else:
                text = "Danh sách sản phẩm có giá từ {} đến {}".format(
                    from_price, to_price)
                sqlQuery = "select * from dienthoai where gia between {} and {} limit 9".format(
                    from_price, to_price)
            data = getData(sqlQuery)
            if data:
                list_item = []
                for item in data:
                    list_btn = [ButtonTemplate("Xem chi tiết", "Cấu hình của {}".format(
                        item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia = "Giá: {}".format(item['gia'])
                    else:
                        gia = "Đang cập nhật"
                    mess_item = ItemsTemplate(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)
                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(text=text, json_message=message_str)
        else:
            dispatcher.utter_message("Hiện tại chúng tôi không có sản phẩm nào trong mức giá mà bạn đưa ra. Vui lòng thử một mức giá khác.")
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        return


class ActionFindProductLowerPrice(Action):
    # action tìm sản phấm dưới 1 mức giá
    def name(self) -> Text:
        return "action_find_product_lower_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        price = 0
        product_company =""
        sqlQuery = ""
        try:
            price = priceModify(
                next(tracker.get_latest_entity_values(entity_type='price')))
        except:
            pass
        try:
            product_company = next(tracker.get_latest_entity_values(entity_type='product_company'))
        except:
            pass
        if price != 0:
            sqlQuery = "select dienthoai.ten,dienthoai.gia,dienthoai.url_img from dienthoai,hangdienthoai where dienthoai.idhangdienthoai = hangdienthoai.idHangDienThoai and gia <= {}".format(
                price)
            if product_company:
                sqlQuery = sqlQuery + " and hangdienthoai.ten like '%{}%'".format(product_company)

            sqlQuery = sqlQuery + " order by gia desc limit 9"
            data = getData(sqlQuery)
            if data:
                list_item = []
                for item in data:
                    list_btn = [ButtonTemplate("Xem chi tiết", "Cấu hình của {}".format(
                        item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
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
            dispatcher.utter_message("Mức giá bạn đưa ra không có, vui lòng thử lại!")
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

            sqlQuery = sqlQuery + " order by gia desc limit 9"
            data = getData(sqlQuery)
            if data:
                list_item = []
                for item in data:
                    list_btn = [ButtonTemplate("Xem chi tiết", "Cấu hình của {}".format(
                        item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
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
        try:
            price = priceModify(
                next(tracker.get_latest_entity_values(entity_type='price')))
        except:
            pass
        product_company = ''
        try:
            product_company = next(tracker.get_latest_entity_values(entity_type='product_company'))
        except:
            pass
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
                    list_btn = [ButtonTemplate("Xem chi tiết", "Cấu hình của {}".format(
                        item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
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
            productName = tracker.get_slot('product_name')
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
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
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
            productName = tracker.get_slot('product_name')
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
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        dispatcher.utter_message(message_str)
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]


class ActionBuyOldProduct(Action):
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
            productName = tracker.get_slot('product_name')
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
                    temp = gia*75/100
                    message_str = "Đối với sản phẩm {} còn trong thời gian bảo hành, không bị rơi vỡ, cấn móp do va đập hay ngấm các dung dịch chất lỏng như nước v.v thì bên cửa hàng sẽ mua lại sản phẩm với giá khoảng 75% giá bán ra tứ là khoảng {:,} vnđ ạ.".format(data[0]['ten'],temp)
            else:
                Pname_temp = productName
                message_str = "Hiện cửa hàng không cung cấp dịch vụ cho sản phẩm {} nữa ạ. Mong bạn thông cảm.".format(productName)
        else:
            message_str = "Bạn đang hỏi thông tin thu mua cũ cho sản phẩm nào ạ?"
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
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
            tratruoc = 0
            #region try catch entity
            try:
                tgian_tragop = InstallmentPaymentPeriod(
                    next(tracker.get_latest_entity_values(entity_type='installment_payment_period')))
            except:
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
                elif data[0]['url_installment'].fin('tra-gop') >-1:
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
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
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
                        tienthang = tienno/4 + tienno*1.66/100
                        message_str = "Sản phẩm {} có hỗ trợ trả góp. Bạn có thể tham khảo gói trả góp sau:  \n  Trả trước 30%.  \nTrả góp trong 4 tháng.  \nMỗi tháng trả {:,} vnđ.  \n*Lưu ý: Số liệu trên đây chỉ mang tính chất tham khảo.  \nĐể biết thêm chi tiết về các gói trả góp của {} bạn có thể truy cập trang web sau. {}".format(
                            data[0]['ten'], tienthang, data[0]['ten'], data[0]['url_installment'])
                    else:
                        message_str = "Sản phẩm {} hiện tại chưa hỗ trợ trả góp. Mong bạn thông cảm.".format(productName)
            else:
                Pname_temp = productName
        else:
            message_str ='Bạn đang hỏi thông tin trả góp của sản phẩm nào ạ?'
        dispatcher.utter_message(message_str)
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
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
        #region try-catch entity
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            tracker.get_slot('product_name')
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
                    message_str = "Sản phẩm {0} chỉ là tin đồn. Cửa hàng sẽ thông báo cho bạn thông tin mới nhất về sản phẩm {0} khi được cập nhật.".format(productName)
                else:
                    col = GetColName(hardware_name.lower())
                    value = data[0][col]
                    if value is None:
                        message_str = HardwareAnswer(value,role,'no')
                    else:
                        message_str = HardwareAnswer(value,role,'yes')
            else:
                Pname_temp = productName
                message_str = "Hiện tại cửa hàng của chúng tôi không có thông tin về sản phẩm {}. Vui lòng thử tìm kiếm sản phẩm khác.".format(productName)
        else:
            message_str = "Bạn đang hỏi thông tin của sản phẩm nào ạ?"
        dispatcher.utter_message(message_str)
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
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
            productName = tracker.get_slot('product_name')
            pass
        #endregion
        if productName:
            sqlQuery = "select * from dienthoai where ten like '%{}%'".format(productName)
            data = getData(sqlQuery)
            if data:
                Pname_temp = data[0]['ten']
                if data[0]['ghi_chu'].find('tin đồn') > -1:
                    message_str = "Sản phẩm {0} chỉ là tin đồn. Cửa hàng sẽ thông báo cho bạn thông tin mới nhất về sản phẩm {0} khi được cập nhật.".format(productName)
                else:
                    chup_anh = data[0]['chup_anh_nang_cao']
                    if chup_anh.find('xóa phông') > -1:
                        message_str = "Sản phẩm {} có hỗ trở chụp ảnh xóa phông ạ.".format(Pname_temp)
                    else:
                        message_str = "Sản phẩm {} chưa hỗ trở chụp ảnh xóa phông ạ.".format(Pname_temp)
            else:
                Pname_temp = productName
                message_str = "Hiện tại cửa hàng của chúng tôi không có thông tin về sản phẩm {}. Vui lòng thử tìm kiếm sản phẩm khác.".format(productName)
        else:
            message_str = "Bạn đang hỏi thông tin chụp ảnh xóa phông của sản phẩm nào ạ?"
        dispatcher.utter_message(message_str)
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
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
            productName = tracker.get_slot('product_name')
            pass
        #endregion
        if productName:
            sqlQuery = "select * from dienthoai where ten like '%{}%'".format(productName)
            data = getData(sqlQuery)
            if data:
                Pname_temp = data[0]['ten']
                if data[0]['ghi_chu'].find('tin đồn') > -1:
                    message_str = "Sản phẩm {0} chỉ là tin đồn. Cửa hàng sẽ thông báo cho bạn thông tin mới nhất về sản phẩm {0} khi được cập nhật.".format(productName)
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
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
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
            productName = tracker.get_slot('product_name')
            pass
        #endregion
        if productName:
            sqlQuery = "select * from dienthoai where ten like '%{}%'".format(productName)
            data = getData(sqlQuery)
            if data:
                Pname_temp = data[0]['ten']
                if data[0]['ghi_chu'].find('tin đồn')>-1:
                    message_str = "Sản phẩm {0} chỉ là tin đồn. Cửa hàng sẽ thông báo cho bạn thông tin mới nhất về sản phẩm {0} khi được cập nhật.".format(productName)
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
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
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
            productName = tracker.get_slot('product_name')
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
                    message_str = "Sản phẩm {0} chỉ là tin đồn. Cửa hàng sẽ thông báo cho bạn thông tin mới nhất về sản phẩm {0} khi được cập nhật.".format(productName)
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
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
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
                elif data[0]['thoi_gian_bao_hanh']:
                    Pname_temp = data[0]['ten']
                    message_str = "Thời gian bảo hành của {} là: {}".format(productName,data[0]['thoi_gian_bao_hanh'])
            else:
                Pname_temp = productName
                message_str = "Hiện cửa hàng không có thông tin về sản phẩm {}. Mong bạn thông cảm!"
        else:
            message_str = "Bạn đang hỏi thông tin bảo hành của sản phẩm nào ạ?"
        dispatcher.utter_message(message_str)
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
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
        Pname_temp =""
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            productName = tracker.get_slot('product_name')
            pass
        if productName:
            sqlQuery = "select * from dienthoai where ten like '%{}%'".format(
                productName)
            data = getData(sqlQuery)
            if data:
                if data[0]['ghi_chu'] == "Sản phẩm tin đồn":
                    message_str = "Sản phẩm {} mới chỉ là tin đồn. Bên cửa hàng sẽ thông báo cho bạn khi có thông tin mới về sản phẩm này ạ.".format(data[0]['ten'])
                elif data[0]['khuyen_mai']:
                    Pname_temp = data[0]['ten']
                    khuyen_mai = data[0]['khuyen_mai']
                    message_str = "Hiện sản phẩm {} đang có các chương trình khuyến mãi như sau:\n{}".format(
                        Pname_temp, khuyen_mai)
            else:
                Pname_temp = productName
                message_str = "Sản phẩm {} hiện không có khuyến mãi nào. Xin cảm ơn".format(Pname_temp)
        else:
            message_str = "Bản đang hỏi thông tin khuyến mãi của sản phẩm nào ạ?"
        dispatcher.utter_message(message_str)
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',Pname_temp)]


class ActionFindProduct(Action):
    # action tìm kiếm 1 sản phẩm
    def name(self) -> Text:
        return "action_find_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        sqlQuery = ""
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
            pass
        if productName:
            sqlQuery = "Select * from dienthoai where ten like '%{}%'".format(
                productName)
            #region try-catch enity
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
            sqlQuery = sqlQuery + "limit 9;"
            data = getData(sqlQuery)
            if data:
                list_item = []
                for item in data:
                    list_btn = [ButtonTemplate("Xem cấu hình", "Cấu hình của {}".format(
                        item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
                    gia = ""
                    if item['gia']:
                        gia = "Giá: {:,} vnđ".format(item['gia'])
                    else:
                        gia = "Sản phẩm tin đồn"
                    mess_item = ItemsTemplate(
                        item['ten'], item['url_img'], gia, list_btn)
                    list_item.append(mess_item)

                message_str = GenericTemplate(list_item)
                dispatcher.utter_message(
                    text="Giá nè", json_message=message_str)
            else:
                dispatcher.utter_message(
                    "Cửa hàng mình chưa có thông tin về sản phẩm {}. Bên mình sẽ thông báo đến bạn khi có thông tin về sản phẩm này. Xin cảm ơn!")
        else:
            dispatcher.utter_message(
                "Bạn đang tìm kiếm sản phẩm nào ạ?")
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',productName)]


class ActionFindAnotherProduct(Action):
    # action tìm kiếm 1 bản khác
    def name(self) -> Text:
        return "action_find_another_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        productName = ""
        try:
            productName = productNameModify(
                next(tracker.get_latest_entity_values(entity_type='product_name')))
        except:
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
            sqlQuery = sqlQuery + "limit 9;"
            result = getData(sqlQuery)
            if result:
                list_item = []
                for item in result:
                    list_btn = [ButtonTemplate("Xem chi tiết", "Cấu hình của {}".format(
                        item['ten'])), ButtonTemplate("Đặt mua", 'Đặt mua {}'.format(item['ten']))]
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
            print(sqlQuery)
        else:
            dispatcher.utter_message(
                "Không tìm thấy sản phẩm vui lòng thử lại sau!")
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        return[SlotSet('latest_action',self.name()),SlotSet('product_name',productName)]


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
        print("--------------\n{}\n{}\n{}".format(self.name(),sqlQuery,tracker.latest_message.get('text')))
        if productName:
            sqlQuery = "select * from dienthoai where ten like '%{}%'".format(productName)
            data = getData(sqlQuery)
            print("--------------\n{}\n{}\n-----------".format(self.name(),previus_action))
            if data:
                SlotSet('product_name',data[0]['ten'])
                if previus_action:
                    return[FollowupAction(name=previus_action)]
                else:
                    return[FollowupAction("action_find_product")]
        else:
            dispatcher.utter_message('Vui lòng nhập tên sản phẩm bạn muốn tìm hiểu thông tin!')
            return

class ActionOptionInBox(Action):
    # action thông tin khuyến mãi và quà tặng
    def name(self) -> Text:
        return "action_option_in_box"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # productName = ""
        # sqlQuery = ""
        # Pname_temp =""
        return

class ActionCanPlayGame(Action):
    # action thông tin khuyến mãi và quà tặng
    def name(self) -> Text:
        return "action_can_play_game"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # productName = ""
        # sqlQuery = ""
        # Pname_temp =""
        return