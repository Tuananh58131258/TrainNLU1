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

        return

class ActionOnlinePrice(Action):
# action trả lời giá online
    def name(self) -> Text:
        return "action_online_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionOldProduct(Action):
# action trả lời giá của sản phẩm cũ
    def name(self) -> Text:
        return "action_old_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionProductConfiguration(Action):
# action trả lời cấu hình của sản phẩm
    def name(self) -> Text:
        return "action_product_configuration"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionTypeOfProduct(Action):
# action trả lời các hãng điện thoại sẵn có
    def name(self) -> Text:
        return "action_type_of_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionListProduct(Action):
# action trả lời danh sách các sản phẩm của 1 hãng
    def name(self) -> Text:
        return "action_list_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionCheckPrice(Action):
# action kiểm tra giá sản phẩm
    def name(self) -> Text:
        return "action_check_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionFindProductInRangePrice(Action):
# action tìm kiếm sản phẩm trong 1 khoảng giá
    def name(self) -> Text:
        return "action_find_product_in_range_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionFindProductLowerPrice(Action):
# action tìm sản phấm dưới 1 mức giá
    def name(self) -> Text:
        return "action_find_product_lower_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionFindProductUpperPrice(Action):
# action tìm sản phẩm trên 1 mức giá
    def name(self) -> Text:
        return "action_find_product_upper_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionFindProductAroundPrice(Action):
# action tìm sản phẩm quanh 1 mức giá
    def name(self) -> Text:
        return "action_find_product_around_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionScreenInfo(Action):
# action thông tin màn hình
    def name(self) -> Text:
        return "action_scree_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionPinInfo(Action):
# action thông tin về pin
    def name(self) -> Text:
        return "action_pin_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionBuyOldProduct(Action):
# action thu mua lại sản phẩm cũ
    def name(self) -> Text:
        return "action_buy_old_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionHowManyPerMonth(Action):
# action cần trả bao nhiêu tiền 1 tháng
    def name(self) -> Text:
        return "action_how_many_per_month"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionCaseHowManyPerMonth(Action):
# action cần trả bao nhiêu tiền 1 tháng trong 2 trường hợp
    def name(self) -> Text:
        return "action_case_how_many_per_month"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionIsProductCanBuyOnInstallment(Action):
# action sản phẩm có được mua trả góp hay không
    def name(self) -> Text:
        return "action_is_product_can_buy_on_installment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionHarwareInfo(Action):
# action thông tin chi tiết phần cứng
    def name(self) -> Text:
        return "action_hardware_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionMainCamera(Action):
# action thông tin về camera sau
    def name(self) -> Text:
        return "action_main_camera"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionSelfieCamera(Action):
# action thông tin camera trước
    def name(self) -> Text:
        return "action_selfie_camera"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return
class ActionResolutionCamera(Action):
# action thông tin độ phân giải của cả camera trước và sau
    def name(self) -> Text:
        return "action_resolution_camrea"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionGuarantee(Action):
# action thông tin bảo hành
    def name(self) -> Text:
        return "action_guarantee"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionPromotionsAndGift(Action):
# action thông tin khuyến mãi và quà tặng 
    def name(self) -> Text:
        return "action_promotions_and_gift"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionFindProduct(Action):
# action tìm kiếm 1 sản phẩm
    def name(self) -> Text:
        return "action_find_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return

class ActionFindAnotherProduct(Action):
# action tìm kiếm 1 bản khác
    def name(self) -> Text:
        return "action_find_another_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return