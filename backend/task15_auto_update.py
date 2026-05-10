# TASK 15: Infinite loop to auto-refresh display
import time
from task8_http_parser import vote_counts, vote_lock

def display_loop():
    while True:
        print("\033[H\033[J", end="") # Clear terminal
        print("===================================")
        print("   KAHOOT LIVE RESULTS SCREEN      ")
        print("===================================")
        
        with vote_lock:
            for option, count in vote_counts.items():
                bar = "█" * count
                print(f"{option:<15} | {count} votes | {bar}")
                
        print("===================================")
        time.sleep(1)