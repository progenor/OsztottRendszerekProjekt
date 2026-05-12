# TASK 3: Web RPC writes to database
from task4_db_router import get_connection
import mysql.connector

def save_vote_to_db(db_type, session_id, user_id, question_id, option_id=None, answer_text=None):
    conn = get_connection(db_type)
    try:
        with conn.cursor(dictionary=True) as cursor:
            sql = """
                INSERT INTO Answers (Session_ID, User_ID, Question_ID, Option_ID, Answer_text) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (session_id, user_id, question_id, option_id, answer_text))
            conn.commit()
            return True  # Vote was successfully saved
            
    except mysql.connector.IntegrityError:
        # This catches the duplicate vote! (User already voted for this question)
        print(f"Duplicate vote blocked: User {user_id} already voted on Question {question_id}.")
        conn.rollback()  # Clears the failed transaction safely
        return False
        
    except Exception as e:
        # Catches any other random database errors to prevent a total crash
        print(f"Unexpected database error in save_vote_to_db: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()