## start conversation
* start
    - utter_introduction
    - utter_ask_question_request    

## user accepts receiving questions
* affirm
    - slot{"state" : "intro"}
    - action_start_questions
    - action_ask_question

## user denies receiving questions
* deny
    - slot{"state" : "intro"}
    - action_end_conversation
    
## user affirms while asking questions
* affirm
    - slot{"state" : "questions"}
    - action_fallback_management

## user denies while asking questions
* deny
    - slot{"state" : "questions"}
    - action_fallback_management
    
## user answers the current question ok
* answer_question
    - slot{"state" : "questions"}
    - action_update_score
    - action_give_feedback
    - action_ask_question
    - slot{"frequency" : null}
    
## user somehow answers the intro with no affirmation/denial
* answer_question
    - slot{"state" : "intro"}
    - action_fallback_management
    
## user does not understand the questions
* rephrase
    - slot{"state" : "questions"}
    - action_rephrase_sentence