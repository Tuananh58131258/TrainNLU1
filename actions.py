# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

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

        dispatcher.utter_message(text="Fallback fallback")
        log = tracker.latest_message.get('text')
        log = tracker.get_latest_entity_values.get('role')
        if log:
            print("khách hàng nhập: {}".format(log))
        else: print("somthing wrong but all are oke")
        return [UserUtteranceReverted()]

class ActionTestST(Action):

    def name(self) -> Text:
        return "action_test_st"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Fallback fallback")
        # log = tracker.latest_message.get('text')
        log = tracker.get_latest_entity_values.get('role')
        if log:
            res = "khách hàng nhập: {}".format(log)
        else: res = "somthing wrong but all are oke"
        dispatcher.utter_message(res)
        return 