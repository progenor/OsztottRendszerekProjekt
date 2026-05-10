# TASK 6: Web RPC to display application
import requests

def notify_display(user_name, chosen_answer):
    url = f"http://localhost:5000/kijelzo/update?nev={user_name}&szavazat={chosen_answer}"
    try:
        requests.get(url, timeout=1)
    except Exception:
        pass # Ignore if display app is offline