# TASK 1: The main Web Server
from flask import Flask, request
from flask_cors import CORS
from task2_vote_receiver import handle_vote
from task5_db_read import setup_read_routes

app = Flask(__name__)
CORS(app)

# Initialize all the routes from Task 5
setup_read_routes(app)

# Initialize the POST route from Task 2
@app.route('/<db_type>/vote', methods=['POST'])
def api_vote(db_type):
    return handle_vote(db_type, request.json)

if __name__ == '__main__':
    print("Main Web Server running on port 8080...")
    app.run(host='0.0.0.0', port=8080, debug=True)