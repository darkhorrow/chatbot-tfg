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
    - utter_not_valid_response

## user denies while asking questions
* deny
    - slot{"state" : "questions"}
    - utter_not_valid_response
    
## ask question low intent
* low
    - slot{"state" : "questions"}
    - action_update_score
    - action_give_feedback
    - action_ask_question
    
## ask question low-medium intent
* low-medium
    - slot{"state" : "questions"}
    - action_update_score
    - action_give_feedback
    - action_ask_question
    
## ask question medium intent
* medium
    - slot{"state" : "questions"}
    - action_update_score
    - action_give_feedback
    - action_ask_question
    
## ask question medium-high intent
* medium-high
    - slot{"state" : "questions"}
    - action_update_score
    - action_give_feedback
    - action_ask_question
    
## ask question high intent
* high
    - slot{"state" : "questions"}
    - action_update_score
    - action_give_feedback
    - action_ask_question
    
## user does not understand the questions
* rephrase
    - slot{"state" : "questions"}
    - action_rephrase_sentence