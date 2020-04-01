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

questions = ["Primera pregunta",
             "Segunda pregunta",
             "Tercera pregunta",
             "Cuarta pregunta",
             "Quinta pregunta",
             "Sexta pregunta",
             "Séptima pregunta",
             "Octava pregunta",
             "Novena pregunta",
             ]


class ActionAskQuestion(Action):

    def name(self) -> Text:
        return "action_ask_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_question = int(tracker.get_slot('question_id'))
        dispatcher.utter_message(text=questions[current_question])
        return [SlotSet('question_id', min(float(current_question + 1.0), float(len(questions) - 1)))]
