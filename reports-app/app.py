from flask import Flask, render_template, g, make_response
import sqlite3
import json
from config import APP_NAME, DATABASE

app = Flask(APP_NAME)


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    events = query_db("SELECT id, sender_id, datetime(timestamp, 'unixepoch') as date FROM events WHERE type_name = "
                      "'user' GROUP BY sender_id ORDER BY id")
    return render_template("index.html", data=events)


@app.route("/report/<sender_id>")
def report_by_id(sender_id):
    start_conversation = query_db(
        f"SELECT datetime(timestamp, 'unixepoch') as date FROM events WHERE sender_id = '{sender_id}' AND "
        f"type_name = 'user' AND "
        f"intent_name = 'start' LIMIT 1")

    end_conversation = query_db(
        f"SELECT datetime(timestamp, 'unixepoch') as date, data FROM events WHERE sender_id = '{sender_id}' AND "
        f"type_name = 'action' AND "
        f"action_name = 'action_end_conversation' LIMIT 1")

    did_finish = len(end_conversation) > 0

    questions_answers = query_db(f"SELECT * FROM events WHERE sender_id = '{sender_id}' AND ((type_name = 'user' AND "
                                 f"intent_name = 'answer_question') "
                                 f"OR(type_name='slot' AND action_name = 'question_id')"
                                 f"OR(type_name='slot' AND action_name = 'frequency')) ORDER BY id")

    questions_scores = query_db(f"SELECT * FROM events WHERE sender_id = '{sender_id}' AND type_name = 'slot' AND "
                                f"action_name = 'score_questions' ORDER BY id")

    rephrase_data = query_db(f"SELECT * FROM events WHERE sender_id = '{sender_id}' AND (type_name = 'user' AND "
                             f"intent_name = 'rephrase') OR (type_name = 'slot' AND action_name = 'question_id') "
                             f"ORDER BY id")

    bot_needs_help = query_db(f"SELECT * FROM events WHERE sender_id = '{sender_id}' AND ((type_name = 'action' AND "
                              f"action_name = 'action_fallback_management') OR "
                              f"(type_name = 'slot' AND action_name = 'question_id') OR "
                              f"(type_name = 'user')) "
                              f"ORDER BY id")

    answers_parsed = []
    scores_parsed = []
    answers_n = []
    valid_frequencies_id = []
    rephrase_parsed = []
    rephrase_questions_n = []
    misunderstandings_n = []
    misunderstandings_text = []

    for row in questions_answers:
        if row['action_name'] == 'frequency':
            if json.loads(row['data'])['value'] in ['low', 'low-medium', 'medium', 'medium-high', 'high']:
                valid_frequencies_id.append(row['id'])

    latest_question = 1
    for row in questions_answers:
        if row['action_name'] == 'question_id':
            latest_question = json.loads(row['data'])['value']
        else:
            if row['id'] + 1 in valid_frequencies_id:
                answers_n.append(int(latest_question))
                answers_parsed.append(json.loads(row['data']))

    final_score = 0

    for row in questions_scores:
        data = json.loads(row['data'])
        scores_parsed.append(data)
        final_score = data['value']

    latest_question = 1
    for row in rephrase_data:
        if row['action_name'] == 'question_id':
            latest_question = json.loads(row['data'])['value']
        else:
            rephrase_questions_n.append(int(latest_question))
            rephrase_parsed.append(json.loads(row['data']))

    latest_question = 1
    latest_phrase = ''
    for row in bot_needs_help:
        if row['action_name'] == 'question_id':
            latest_question = json.loads(row['data'])['value']
        elif row['type_name'] == 'user':
            latest_phrase = json.loads(row['data'])['text']
        else:
            misunderstandings_n.append(int(latest_question))
            misunderstandings_text.append(latest_phrase)

    start_date = start_conversation[0]['date']
    end_date = end_conversation[0]['date'] if did_finish else ""

    return render_template("report.html",
                           did_finish=did_finish,
                           questions=zip(answers_n, answers_parsed, scores_parsed),
                           start_date=start_date,
                           end_date=end_date,
                           final_score=final_score,
                           rephrases=zip(rephrase_questions_n, rephrase_parsed),
                           misunderstanding=zip(misunderstandings_n, misunderstandings_text)
                           )


if __name__ == "__main__":
    app.run(debug=True)
