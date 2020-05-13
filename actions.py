from random import randint

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, Restarted

MAX_FALLBACK = 1
CUTOFF_POINT = 10

QUESTIONS = [
    "¿Con qué frecuencia tiene poco interés o placer en realizar cosas?",
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

FEEDBACK_RESPONSES = {
    "normal_response":
        [
            "Gracias por tu respuesta, me lo apunto, vamos ahora a por la siguiente pregunta.",
            "De acuerdo, anotado, seguimos con la siguiente pregunta.",
            "De acuerdo, seguimos con el resto de las preguntas."
        ],
    "intermediate_response":
        [
            "Gracias, te entiendo, seguimos un poco más con la siguiente pregunta.",
            "Gracias, ya solo nos quedan unas pocas preguntas más."
        ],
    "last_response":
        ["Gracias, ya solo queda la última pregunta."],
}

QUESTIONS_BUTTONS = [
    {"title": "Muy pocas veces", "payload": "/low"},
    {"title": "Pocas veces", "payload": "/low-medium"},
    {"title": "En ocasiones", "payload": "/medium"},
    {"title": "A menudo", "payload": "/medium-high"},
    {"title": "Muchas veces", "payload": "/high"},
]

INTRO_BUTTONS = [
    {"title": "Sí, adelante", "payload": "/affirm"},
    {"title": "Ahora no", "payload": "/deny"},
]

SCORE_MAP = {
    "low": 0,
    "low-medium": 1,
    "medium": 2,
    "medium-high": 3,
    "high": 4,
}


class ActionAskQuestion(Action):

    def name(self) -> Text:
        return "action_ask_question"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_question = int(tracker.get_slot('question_id'))
        if bool(tracker.get_slot('is_asking_questions')):
            dispatcher.utter_message(text=self.__choose_answer(current_question))
            if current_question == len(QUESTIONS):
                return [FollowupAction("action_end_conversation")]
            dispatcher.utter_message(text=QUESTIONS[current_question])
        return [SlotSet('question_id', float(current_question + 1.0)),
                SlotSet('fallback_count', 0.0)]

    def __choose_answer(self, current_question) -> Text:
        if current_question == 0 or current_question >= len(QUESTIONS):
            return ""
        if current_question == len(QUESTIONS) - 1:
            return FEEDBACK_RESPONSES['last_response'][randint(0, len(FEEDBACK_RESPONSES['last_response']) - 1)]
        elif current_question < (len(QUESTIONS) - 1) / 2:
            return FEEDBACK_RESPONSES['normal_response'][randint(0, len(FEEDBACK_RESPONSES['normal_response']) - 1)]
        else:
            return FEEDBACK_RESPONSES['intermediate_response'][
                randint(0, len(FEEDBACK_RESPONSES['intermediate_response']) - 1)]


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
        if is_asking:
            dispatcher.utter_message(text="Gracias por responder a mis preguntas :)")
            if self.__user_needs_evaluation(tracker):
                score_resolution = "Con la información que me has proporcionado he podido determinar que existe " \
                                   "cierto riesgo de que estés sufriendo un trastorno del ánimo. Por lo tanto, " \
                                   "es importante que te pongas en contacto con un profesional de la salud para " \
                                   "realizar una evaluación más completa."
            else:
                score_resolution = "Con la información que me has proporcionado he podido determinar que no " \
                                   "existe un riesgo alto de que padezcas un trastorno del ánimo. No obstante, " \
                                   "te recomiendo que si notas cualquier malestar te pongas en contacto con tu " \
                                   "profesional de la salud."
            dispatcher.utter_message(text=score_resolution)
        return [Restarted()]

    def __user_needs_evaluation(self, tracker: Tracker) -> bool:
        return int(tracker.get_slot('score_questions')) > CUTOFF_POINT


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


class ActionUpdateScore(Action):

    def name(self) -> Text:
        return "action_update_score"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return[SlotSet('score_questions', float(tracker.get_slot('score_questions')) +
                       SCORE_MAP[tracker.latest_message['intent'].get('name')])]