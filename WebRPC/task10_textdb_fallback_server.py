import json
import socket
import threading
from datetime import datetime, timezone
from pathlib import Path


HOST = "0.0.0.0"
PORT = 5001
DB_FILE = Path(__file__).parent / "adatok.txt"

_INITIAL_DB = {
    "users": [],
    "quizzes": [],
    "questions": [],
    "options": [],
    "sessions": [],
    "session_players": [],
    "answers": [],
}

file_lock = threading.Lock()


def _ensure_db_file():
    if not DB_FILE.exists():
        with DB_FILE.open("w", encoding="utf-8") as fp:
            json.dump(_INITIAL_DB, fp, ensure_ascii=False, indent=2)


def _load_db_unlocked():
    with DB_FILE.open("r", encoding="utf-8") as fp:
        data = json.load(fp)
    for key in _INITIAL_DB:
        data.setdefault(key, [])
    return data


def _save_db_unlocked(data):
    with DB_FILE.open("w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)


def _recv_line(conn):
    chunks = []
    while True:
        chunk = conn.recv(4096)
        if not chunk:
            break
        chunks.append(chunk)
        if b"\n" in chunk:
            break
    if not chunks:
        return ""
    data = b"".join(chunks)
    return data.split(b"\n", 1)[0].decode("utf-8", errors="replace")


def _send_json(conn, payload):
    conn.sendall((json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8"))


def _handle_insert_answer(data):
    session_id = data.get("session_id")
    question_id = data.get("question_id")
    player_name = data.get("player_name")
    chosen_answer = data.get("chosen_answer")

    if not session_id:
        raise ValueError("session_id is required")
    if question_id is None:
        raise ValueError("question_id is required")
    if not player_name:
        raise ValueError("player_name is required")
    if chosen_answer is None or str(chosen_answer).strip() == "":
        raise ValueError("chosen_answer is required")

    record = {
        "session_id": session_id,
        "question_id": question_id,
        "player_name": player_name,
        "chosen_answer": str(chosen_answer),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    with file_lock:
        db = _load_db_unlocked()
        db["answers"].append(record)
        _save_db_unlocked(db)

    return {"saved": record}


def _handle_get_answers(data):
    session_id = data.get("session_id")
    question_id = data.get("question_id")

    with file_lock:
        db = _load_db_unlocked()
        answers = list(db["answers"])

    if session_id is not None:
        answers = [a for a in answers if a.get("session_id") == session_id]
    if question_id is not None:
        answers = [a for a in answers if a.get("question_id") == question_id]

    return {"answers": answers}


def _handle_get_results(data):
    payload = _handle_get_answers(data)
    answers = payload["answers"]

    by_answer = {}
    for answer in answers:
        key = str(answer.get("chosen_answer", ""))
        by_answer[key] = by_answer.get(key, 0) + 1

    return {
        "total_votes": len(answers),
        "by_answer": by_answer,
    }


def _dispatch(request):
    action = request.get("action")
    data = request.get("data", {})

    if action == "ping":
        return {"message": "pong"}
    if action == "insert_answer":
        return _handle_insert_answer(data)
    if action == "get_answers":
        return _handle_get_answers(data)
    if action == "get_results":
        return _handle_get_results(data)

    raise ValueError("unknown action")


def _client_thread(conn, addr):
    try:
        raw = _recv_line(conn)
        if not raw:
            return

        try:
            request = json.loads(raw)
        except json.JSONDecodeError:
            _send_json(conn, {"status": "error", "error": "invalid json"})
            return

        try:
            result = _dispatch(request)
            _send_json(conn, {"status": "ok", "data": result})
        except Exception as exc:
            _send_json(conn, {"status": "error", "error": str(exc)})
    finally:
        conn.close()


def start_txt_db():
    _ensure_db_file()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(20)

    print(f"Task 10 (Text DB fallback) listening on {HOST}:{PORT}")
    print(f"Storage file: {DB_FILE}")

    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=_client_thread, args=(client, addr), daemon=True)
        thread.start()


if __name__ == "__main__":
    start_txt_db()
