from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, Restarted

MAX_FALLBACK = 1

QUESTIONS = ["¿Con qué frecuencia tiene poco interés o placer en realizar cosas?",
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

FEEDBACK_RESPONSES = {"low": ["Me alegra mucho. ¡Continúa así!"],
                      "low-medium": ["Más o menos lo llevas bien, pero tengo la certeza de que puedes sentirte mejor."],
                      "medium": ["Todos tenemos de vez en cuando un mal día ¡Ánimo!"],
                      "medium-high": ["Uy, eso no tiene buena pinta. Hay que procurar cambiar esa actitud."],
                      "high": ["¡Eso es terrible! ¡Deberías evitar ese comportamiento a toda costa!"],
                      }

QUESTIONS_BUTTONS = [{"title": "Muy pocas veces", "payload": "/low"},
                     {"title": "Pocas veces", "payload": "/low-medium"},
                     {"title": "En ocasiones", "payload": "/medium"},
                     {"title": "A menudo", "payload": "/medium-high"},
                     {"title": "Muchas veces", "payload": "/high"},
                     ]

INTRO_BUTTONS = [{"title": "Sí, adelante", "payload": "/affirm"},
                 {"title": "Ahora no", "payload": "/deny"}
                 ]


class ActionAskQuestion(Action):

    def name(self) -> Text:
        return "action_ask_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_question = int(tracker.get_slot('question_id'))
        if bool(tracker.get_slot('is_asking_questions')):
            user_intent = tracker.latest_message['intent'].get('name')
            if user_intent in FEEDBACK_RESPONSES:
                dispatcher.utter_message(text=FEEDBACK_RESPONSES[user_intent][0])
            if current_question == len(QUESTIONS):
                return [FollowupAction("action_end_conversation")]
            dispatcher.utter_message(text=QUESTIONS[current_question])

        return [SlotSet('question_id', float(current_question + 1.0)),
                SlotSet('fallback_count', 0.0)]


class ActionStartQuestions(Action):

    def name(self) -> Text:
        return "action_start_questions"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if not bool(tracker.get_slot('is_asking_questions')):
            dispatcher.utter_message(text="Muy bien, ¡comencemos!")
            return [SlotSet('is_asking_questions', True), SlotSet('fallback_count', 0.0)]
        return []


class ActionEndConversation(Action):

    def name(self) -> Text:
        return "action_end_conversation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        is_asking = bool(tracker.get_slot('is_asking_questions'))
        response = "Gracias por responder a mis preguntas :)" if is_asking \
            else "Podemos hablar en otro momento si así lo prefiere."
        dispatcher.utter_message(text=response)
        return [Restarted()]


class ActionFallback(Action):

    def name(self) -> Text:
        return "action_fallback_management"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        is_asking = bool(tracker.get_slot('is_asking_questions'))
        if int(tracker.get_slot('fallback_count') >= MAX_FALLBACK):
            if is_asking:
                dispatcher.utter_button_message(
                    text="Sigo sin entenderte. Puedes intentar explicarlo mejor o usar una de las opciones.",
                    buttons=QUESTIONS_BUTTONS
                )
            else:
                dispatcher.utter_button_message(
                    text="Sigo sin entenderte. Puedes intentar explicarlo mejor o usar una de las opciones.",
                    buttons=INTRO_BUTTONS
                )
            return []
        else:
            dispatcher.utter_message(text="No te estoy entendiendo, ¿podrías decirmelo de manera más sencilla?")
            return [SlotSet('fallback_count', tracker.get_slot('fallback_count') + 1.0)]
