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