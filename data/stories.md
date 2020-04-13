## start conversation
* start
    - utter_introduction
    - utter_ask_question_request    

## user accepts questions
* affirm
    - action_start_questions
    - action_ask_question

## user rejects questions
* deny
    - action_end_conversation
    
## ask question low intent
* low
    - action_ask_question
    
## ask question low-medium intent
* low-medium
    - action_ask_question
    
## ask question medium intent
* medium
    - action_ask_question
    
## ask question medium-high intent
* medium-high
    - action_ask_question
    
## ask question high intent
* high
    - action_ask_question