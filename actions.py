# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionFeedbackLow(Action):

    def name(self) -> Text:
        return "action_give_feedback_low"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="LOW")
        return [SlotSet("answer", "low")]


class ActionFeedbackLowMedium(Action):

    def name(self) -> Text:
        return "action_give_feedback_low_medium"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="LOW-MEDIUM")
        return [SlotSet("answer", "low-medium")]


class ActionFeedbackMedium(Action):

    def name(self) -> Text:
        return "action_give_feedback_medium"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="MEDIUM")
        return [SlotSet("answer", "medium")]


class ActionFeedbackMediumHigh(Action):

    def name(self) -> Text:
        return "action_give_feedback_medium_high"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="MEDIUM-HIGH")
        return [SlotSet("answer", "medium-high")]


class ActionFeedbackHigh(Action):

    def name(self) -> Text:
        return "action_give_feedback_high"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="HIGH")
        return [SlotSet("answer", "high")]