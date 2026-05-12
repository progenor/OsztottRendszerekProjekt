# Component Breakdown

This section provides a detailed description of each file in the project, explaining its purpose and functionality.

## Backend

- **`task1_web_server.py`**: The main entry point of the backend application. It initializes the Flask web server and registers the API routes.
- **`task2_vote_receiver.py`**: Handles incoming votes from the users. It validates the votes and passes them to the `task3_db_write.py` service.
- **`task3_db_write.py`**: Writes the votes to the appropriate database instance.
- **`task4_db_router.py`**: A crucial component that routes database connections to the correct instance based on the game PIN.
- **`task5_db_read.py`**: Reads data from the databases, such as quiz questions and leaderboard information.
- **`task6_notify_display.py`**: Notifies the frontend when a new vote is cast, enabling real-time updates.
- **`task7_socket_server.py`**: A TCP socket server that manages the connection with the host's display.
- **`task8_http_parser.py`**: Parses HTTP requests received by the socket server.
- **`task10_txt_db.py`**: A fallback database that uses a simple text file for storage. This ensures that the system can continue to function even if the MySQL databases are unavailable.
- **`task12_results.js`**: A client-side script that handles the display of results.
- **`task14_login.js`**: Manages the user login process.
- **`task15_auto_update.py`**: A script that automatically updates the host's display with the latest voting results.

## Frontend

- **`index.html`**: The main HTML file that structures the user interface.
- **`task11_gameUi.js`**: This script is responsible for dynamically building the game's user interface.
- **`task13_styles.css`**: Contains all the CSS styles for the application, including the glassmorphism theme.

## Database

- **`db_init.sh`**: A shell script that initializes the two MySQL database instances.
- **`seed.sql`**: Contains the initial data for the databases, including sample quizzes and users.
