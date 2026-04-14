from task4_db_router import get_connection

def save_vote_to_db(pin, question_id, player_name, chosen_answer):
    db = get_connection(pin)
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO votes (game_pin, question_id, player_name, chosen_answer) VALUES (%s, %s, %s, %s)",
        (pin, question_id, player_name, chosen_answer)
    )
    db.commit()
    db.close()