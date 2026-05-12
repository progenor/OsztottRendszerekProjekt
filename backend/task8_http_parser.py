# TASK 8: Parse GET request and lock thread
import urllib.parse
import threading

# Dynamic dictionary to hold votes for any option
vote_counts = {}
vote_lock = threading.Lock()

def parse_http_request(client_socket):
    try:
        # Read the raw HTTP request from the socket
        request = client_socket.recv(1024).decode('utf-8')
        if not request: return

        # Extract the URL line (e.g., "GET /kijelzo/update?nev=Name&szavazat=Option_1 HTTP/1.1")
        first_line = request.split('\n')[0]
        url = first_line.split(' ')[1]

        # Check if it's the correct endpoint
        if "/kijelzo/update" in url:
            # Parse the URL parameters safely
            parsed_url = urllib.parse.urlparse(url)
            params = urllib.parse.parse_qs(parsed_url.query)
            chosen_answer = params.get('szavazat', [None])[0]

            if chosen_answer:
                # Use Mutex Lock to safely update the shared dictionary
                with vote_lock:
                    if chosen_answer not in vote_counts:
                        vote_counts[chosen_answer] = 0
                    vote_counts[chosen_answer] += 1

        # Send a standard HTTP 200 response back to the Flask server so it doesn't hang
        client_socket.sendall("HTTP/1.1 200 OK\n\nSuccess".encode('utf-8'))
    except Exception:
        pass
    finally:
        client_socket.close()