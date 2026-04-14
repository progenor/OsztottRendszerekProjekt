from flask import Flask, jsonify, request
import pymysql
import json
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = Flask(__name__)

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': os.environ.get('DB_ROOT_PASSWORD', ''),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


def get_connection(db_name):
    """Létrehoz egy kapcsolatot a választott adatbázishoz."""
    return pymysql.connect(database=db_name, **DB_CONFIG)

def read_from_txt():
    """Beolvassa a teljes adatbázist szimuláló JSON fájlt."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'adatok.txt')
    
    if not os.path.exists(file_path):
        return {
            "users": [], "quizzes": [], "questions": [],
            "options": [], "sessions": [], "session_players": [], "answers": []
        }

    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


# Lekérdezések---Users

@app.route('/<db_type>/users', methods=['GET'])
def get_users(db_type):
    """Az összes felhasználó listázása (jelszavak nélkül)."""
    if db_type == 'txt':
        return jsonify(read_from_txt().get('users', []))

    db_name = f"kahoot_clone_{db_type}"
    conn = get_connection(db_name)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT User_ID, Role, Email, UserName, Created_at FROM Users")
            return jsonify(cursor.fetchall())
    finally:
        conn.close()


@app.route('/<db_type>/users/<int:user_id>', methods=['GET'])
def get_single_user(db_type, user_id):
    """Egy adott felhasználó adatainak lekérése ID alapján."""
    if db_type == 'txt':
        users = read_from_txt().get('users', [])
        user = next((u for u in users if u.get('User_ID') == user_id), None)
        return jsonify(user) if user else (jsonify({"error": "Felhasználó nem található"}), 404)

    db_name = f"kahoot_clone_{db_type}"
    conn = get_connection(db_name)
    try:
        with conn.cursor() as cursor:
            sql = "SELECT User_ID, Role, Email, UserName, Created_at FROM Users WHERE User_ID = %s"
            cursor.execute(sql, (user_id,))
            user = cursor.fetchone()
            return jsonify(user) if user else (jsonify({"error": "Felhasználó nem található"}), 404)
    finally:
        conn.close()


@app.route('/<db_type>/users/<int:user_id>/quizzes', methods=['GET'])
def get_user_created_quizzes(db_type, user_id):
    """Egy adott felhasználó által készített kvízek listázása."""
    if db_type == 'txt':
        quizzes = read_from_txt().get('quizzes', [])
        user_quizzes = [q for q in quizzes if q.get('Creator_ID') == user_id]
        return jsonify(user_quizzes)

    db_name = f"kahoot_clone_{db_type}"
    conn = get_connection(db_name)
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM Quizzes WHERE Creator_ID = %s"
            cursor.execute(sql, (user_id,))
            return jsonify(cursor.fetchall())
    finally:
        conn.close()


@app.route('/<db_type>/users/<int:user_id>/hosted_sessions', methods=['GET'])
def get_user_hosted_sessions(db_type, user_id):
    """Azoknak a játékmeneteknek a lekérése, amit az adott user indított (hostolt)."""
    if db_type == 'txt':
        sessions = read_from_txt().get('sessions', [])
        hosted = [s for s in sessions if s.get('Host_ID') == user_id]
        return jsonify(hosted)

    db_name = f"kahoot_clone_{db_type}"
    conn = get_connection(db_name)
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM Sessions WHERE Host_ID = %s"
            cursor.execute(sql, (user_id,))
            return jsonify(cursor.fetchall())
    finally:
        conn.close()


@app.route('/<db_type>/users/<int:user_id>/played_sessions', methods=['GET'])
def get_user_played_sessions(db_type, user_id):
    """Azon játékmenetek listázása, amelyekhez a felhasználó játékosként csatlakozott."""
    if db_type == 'txt':
        data = read_from_txt()
        s_players = [sp for sp in data.get('session_players', []) if sp.get('User_ID') == user_id]
        result = []
        for sp in s_players:
            session = next((s for s in data.get('sessions', []) if s.get('Session_ID') == sp.get('Session_ID')), {})
            result.append({
                "Session_name": session.get('Session_name'),
                "Start_time": session.get('Start_time'),
                "Score": sp.get('Score')
            })
        return jsonify(result)

    db_name = f"kahoot_clone_{db_type}"
    conn = get_connection(db_name)
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT s.Session_name, s.Start_time, sp.Score 
                FROM Session_Players sp
                JOIN Sessions s ON sp.Session_ID = s.Session_ID
                WHERE sp.User_ID = %s
            """
            cursor.execute(sql, (user_id,))
            return jsonify(cursor.fetchall())
    finally:
        conn.close()


# Lekérdezések---Quiz

@app.route('/<db_type>/quizzes', methods=['GET'])
def get_quizzes(db_type):
    """Az összes elérhető kvíz listázása a készítő nevével együtt."""
    if db_type == 'txt':
        data = read_from_txt()
        quizzes = data.get('quizzes', [])
        users = data.get('users', [])
        for q in quizzes:
            creator = next((u for u in users if u.get('User_ID') == q.get('Creator_ID')), {})
            q['CreatorName'] = creator.get('UserName', 'Unknown')
        return jsonify(quizzes)

    db_name = f"kahoot_clone_{db_type}"
    conn = get_connection(db_name)
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT q.*, u.UserName as CreatorName 
                FROM Quizzes q 
                JOIN Users u ON q.Creator_ID = u.User_ID
            """
            cursor.execute(sql)
            return jsonify(cursor.fetchall())
    finally:
        conn.close()


@app.route('/<db_type>/quizzes/<int:quiz_id>', methods=['GET'])
def get_single_quiz(db_type, quiz_id):
    """Egy adott kvíz alapinformációinak lekérése ID alapján."""
    if db_type == 'txt':
        quizzes = read_from_txt().get('quizzes', [])
        quiz = next((q for q in quizzes if q.get('Quiz_ID') == quiz_id), None)
        return jsonify(quiz) if quiz else (jsonify({"error": "Kvíz nem található"}), 404)

    db_name = f"kahoot_clone_{db_type}"
    conn = get_connection(db_name)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Quizzes WHERE Quiz_ID = %s", (quiz_id,))
            quiz = cursor.fetchone()
            return jsonify(quiz) if quiz else (jsonify({"error": "Kvíz nem található"}), 404)
    finally:
        conn.close()


@app.route('/<db_type>/quizzes/<int:quiz_id>/full', methods=['GET'])
def get_full_quiz(db_type, quiz_id):
    """Egy konkrét kvíz lekérése az összes kérdéssel és válaszlehetőséggel együtt."""
    if db_type == 'txt':
        data = read_from_txt()
        questions = [q for q in data.get('questions', []) if q.get('Quiz_ID') == quiz_id]
        options = data.get('options', [])
        for q in questions:
            q['options'] = [o for o in options if o.get('Question_ID') == q.get('Question_ID')]
        return jsonify(questions)

    db_name = f"kahoot_clone_{db_type}"
    conn = get_connection(db_name)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Questions WHERE Quiz_ID = %s", (quiz_id,))
            questions = cursor.fetchall()
            for q in questions:
                cursor.execute("SELECT Option_ID, Option_text, Is_correct FROM Options WHERE Question_ID = %s",
                               (q['Question_ID'],))
                q['options'] = cursor.fetchall()
            return jsonify(questions)
    finally:
        conn.close()


@app.route('/<db_type>/questions/<int:question_id>', methods=['GET'])
def get_single_question(db_type, question_id):
    """Egy specifikus kérdés lekérése a hozzá tartozó opciókkal."""
    if db_type == 'txt':
        data = read_from_txt()
        question = next((q for q in data.get('questions', []) if q.get('Question_ID') == question_id), None)
        if not question:
            return jsonify({"error": "Kérdés nem található"}), 404
        question['options'] = [o for o in data.get('options', []) if o.get('Question_ID') == question_id]
        return jsonify(question)

    db_name = f"kahoot_clone_{db_type}"
    conn = get_connection(db_name)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Questions WHERE Question_ID = %s", (question_id,))
            question = cursor.fetchone()
            if not question:
                return jsonify({"error": "Kérdés nem található"}), 404
            cursor.execute("SELECT Option_ID, Option_text, Is_correct FROM Options WHERE Question_ID = %s",
                           (question_id,))
            question['options'] = cursor.fetchall()
            return jsonify(question)
    finally:
        conn.close()


# Lekérdezések---Játékmenet

@app.route('/<db_type>/sessions/active', methods=['GET'])
def get_active_sessions(db_type):
    """Csak az éppen aktív (Is_active=True) játékmenetek listázása."""
    if db_type == 'txt':
        sessions = read_from_txt().get('sessions', [])
        active = [s for s in sessions if s.get('Is_active') is True]
        return jsonify(active)

    db_name = f"kahoot_clone_{db_type}"
    conn = get_connection(db_name)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Sessions WHERE Is_active = TRUE")
            return jsonify(cursor.fetchall())
    finally:
        conn.close()


@app.route('/<db_type>/sessions/pin/<game_pin>', methods=['GET'])
def get_session_by_pin(db_type, game_pin):
    """Játékmenet adatainak lekérése Game_PIN alapján (ezzel csatlakoznak a játékosok)."""
    if db_type == 'txt':
        sessions = read_from_txt().get('sessions', [])
        session = next((s for s in sessions if str(s.get('Game_PIN')) == str(game_pin)), None)
        return jsonify(session) if session else (jsonify({"error": "Nincs ilyen Game PIN"}), 404)

    db_name = f"kahoot_clone_{db_type}"
    conn = get_connection(db_name)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Sessions WHERE Game_PIN = %s", (game_pin,))
            session = cursor.fetchone()
            return jsonify(session) if session else (jsonify({"error": "Nincs ilyen Game PIN"}), 404)
    finally:
        conn.close()


@app.route('/<db_type>/sessions/<int:session_id>/leaderboard', methods=['GET'])
def get_leaderboard(db_type, session_id):
    """Ranglista lekérése: kik vannak a sessionben és mennyi a pontjuk."""
    if db_type == 'txt':
        data = read_from_txt()
        s_players = [sp for sp in data.get('session_players', []) if sp.get('Session_ID') == session_id]

        # Sorbarendezés pontszám alapján csökkenőbe
        s_players.sort(key=lambda x: x.get('Score', 0), reverse=True)

        result = []
        for sp in s_players:
            user = next((u for u in data.get('users', []) if u.get('User_ID') == sp.get('User_ID')), {})
            result.append({
                "UserName": user.get('UserName', 'Ismeretlen'),
                "Score": sp.get('Score'),
                "Joined_at": sp.get('Joined_at')
            })
        return jsonify(result)

    db_name = f"kahoot_clone_{db_type}"
    conn = get_connection(db_name)
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT u.UserName, sp.Score, sp.Joined_at 
                FROM Session_Players sp
                JOIN Users u ON sp.User_ID = u.User_ID
                WHERE sp.Session_ID = %s
                ORDER BY sp.Score DESC
            """
            cursor.execute(sql, (session_id,))
            return jsonify(cursor.fetchall())
    finally:
        conn.close()


# Lekérdezések---Válaszok

@app.route('/<db_type>/sessions/<int:session_id>/answers', methods=['GET'])
def get_session_answers(db_type, session_id):
    """Az összes leadott válasz listázása egy adott játékmeneten belül."""
    if db_type == 'txt':
        data = read_from_txt()
        answers = [a for a in data.get('answers', []) if a.get('Session_ID') == session_id]

        # Adatok kibővítése UserName-el és Question_text-el (JOIN szimulálása)
        for a in answers:
            user = next((u for u in data.get('users', []) if u.get('User_ID') == a.get('User_ID')), {})
            question = next((q for q in data.get('questions', []) if q.get('Question_ID') == a.get('Question_ID')), {})
            a['UserName'] = user.get('UserName', 'Ismeretlen')
            a['Question_text'] = question.get('Question_text', 'Ismeretlen kérdés')
        return jsonify(answers)

    db_name = f"kahoot_clone_{db_type}"
    conn = get_connection(db_name)
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT a.*, u.UserName, q.Question_text
                FROM Answers a
                JOIN Users u ON a.User_ID = u.User_ID
                JOIN Questions q ON a.Question_ID = q.Question_ID
                WHERE a.Session_ID = %s
            """
            cursor.execute(sql, (session_id,))
            return jsonify(cursor.fetchall())
    finally:
        conn.close()


@app.route('/<db_type>/sessions/<int:session_id>/players/<int:user_id>/answers', methods=['GET'])
def get_player_answers_in_session(db_type, session_id, user_id):
    """Egy adott játékos által leadott válaszok lekérése egy konkrét játékmenetben."""
    if db_type == 'txt':
        data = read_from_txt()
        answers = [a for a in data.get('answers', []) if
                   a.get('Session_ID') == session_id and a.get('User_ID') == user_id]
        return jsonify(answers)

    db_name = f"kahoot_clone_{db_type}"
    conn = get_connection(db_name)
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT a.Question_ID, a.Option_ID, a.Answer_text, a.Created_at 
                FROM Answers a
                WHERE a.Session_ID = %s AND a.User_ID = %s
            """
            cursor.execute(sql, (session_id, user_id))
            return jsonify(cursor.fetchall())
    finally:
        conn.close()


@app.route('/<db_type>/sessions/<int:session_id>/questions/<int:question_id>/stats', methods=['GET'])
def get_question_stats(db_type, session_id, question_id):
    """
    Megszámolja, hogy egy adott kérdésre melyik opcióra hány szavazat érkezett.
    """
    if db_type == 'txt':
        data = read_from_txt()
        options = [o for o in data.get('options', []) if o.get('Question_ID') == question_id]
        answers = [a for a in data.get('answers', [])
                   if a.get('Session_ID') == session_id and a.get('Question_ID') == question_id]

        stats = []
        for opt in options:
            count = sum(1 for a in answers if a.get('Option_ID') == opt.get('Option_ID'))
            stats.append({
                "Option_text": opt.get('Option_text'),
                "VoteCount": count
            })
        return jsonify(stats)

    db_name = f"kahoot_clone_{db_type}"
    conn = get_connection(db_name)
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT o.Option_text, COUNT(a.Answer_ID) as VoteCount
                FROM Options o
                LEFT JOIN Answers a ON o.Option_ID = a.Option_ID AND a.Session_ID = %s
                WHERE o.Question_ID = %s
                GROUP BY o.Option_ID
            """
            cursor.execute(sql, (session_id, question_id))
            return jsonify(cursor.fetchall())
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)