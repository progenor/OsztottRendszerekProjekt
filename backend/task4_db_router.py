# TASK 4: Server side multiple database handling based on key
import pymysql
import json
import os

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '', # Add your password here if needed
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_connection(db_type):
    """Csatlakozik a megfelelő adatbázishoz (a vagy b)."""
    db_name = f"kahoot_clone_{db_type}"
    return pymysql.connect(database=db_name, **DB_CONFIG)

def read_from_txt():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'adatok.txt')
    if not os.path.exists(file_path):
         return {"users": [], "quizzes": [], "questions": [], "options": [], "sessions": [], "session_players": [], "answers": []}
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)