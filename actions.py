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

questions = ["¿Con qué frecuencia tiene poco interés o placer en realizar cosas?",
             "En las dos últimas semanas, ¿con qué frecuencia se ha sentido decaído/a, deprimido/a o sin esperanzas?",
             "¿Qué dificultad ha tenido para conciliar el sueño o, en caso opuesto, en levantarse de la cama?",
             "En las dos últimas semanas, ¿con qué frecuencia ha experimentado cansancio o falta de energía?",
             "¿Con qué frecuencia cree que ha sentido falta o exceso de apetito?",
             "En las dos últimas semanas, ¿con qué recurrencia se ha sentido mal consigo mismo/a, "
             "que es un fracaso o qué le ha fallado a sus seres queridos?",
             "¿Con cuánta dificultad se ha enfrentado para centrarse en actividades, como leer o ver la televisión?",
             "¿Con qué abundancia cree que se ha movido o hablado tan despacio/rápido que otras personas "
             "lo puedan haber notado?",
             "En las dos últimas semanas, ¿con qué frecuencia ha tenido pensamientos que impliquen autolesión o que"
             "impliquen que estaría mejor muerto/a?",
             ]


class ActionAskQuestion(Action):

    def name(self) -> Text:
        return "action_ask_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_question = int(tracker.get_slot('question_id'))
        dispatcher.utter_message(text=questions[current_question])
        return [SlotSet('question_id', min(float(current_question + 1.0), float(len(questions) - 1)))]
