# TASK 2: Controller for submitting votes
from flask import jsonify
from task3_db_write import save_vote_to_db
from task6_notify_display import notify_display

def handle_vote(db_type, data):
    session_id = data.get('session_id')
    user_id = data.get('user_id')
    question_id = data.get('question_id')
    option_id = data.get('option_id')
    answer_text = data.get('answer_text')
    user_name = data.get('user_name', 'Ismeretlen')

    # Task 3
    save_vote_to_db(db_type, session_id, user_id, question_id, option_id, answer_text)
    
    # Task 6
    vote_val = answer_text if answer_text else f"Option_{option_id}"
    notify_display(user_name, vote_val)
    
    return jsonify({"status": "Vote recorded"}), 200