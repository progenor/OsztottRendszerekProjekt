# TASK 7: Socket server listening logic
import socket
import threading
from task8_http_parser import parse_http_request
from task15_auto_update import display_loop

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 5000))
    server.listen(5)
    print("Display Server listening on port 5000...")

    threading.Thread(target=display_loop, daemon=True).start()

    while True:
        client_socket, _ = server.accept()
        threading.Thread(target=parse_http_request, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()