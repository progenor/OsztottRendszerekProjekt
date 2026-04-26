from task4_db_router import get_db_connection

def get_question(game_pin):
    db = get_db_connection(game_pin)
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM questions WHERE game_pin = %s LIMIT 1", (game_pin,))
    question = cursor.fetchone()
    
    cursor.close()
    db.close()
    
    if question:
        question.pop('correct_answer', None) # Hide the answer from the client!
        
    return question