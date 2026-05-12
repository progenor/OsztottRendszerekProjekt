# OsztottRendszerekProjekt (Kahoot Clone)

This project is a real-time quiz game platform, similar to Kahoot, built with a distributed systems approach. It is designed to handle multiple concurrent users and ensure high availability through a microservices architecture and load balancing.

For detailed documentation, please see the `docs` folder.

## Getting Started

### Prerequisites

1. Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).
2. Create a `.env` file in the project root:
   ```env
   DB_ROOT_PASSWORD=your_root_password
   DB_USER=your_user_name
   DB_PASSWORD=your_user_password
   ```

### Running the Project

1.  **Start the services**:
    ```bash
    docker-compose up -d
    ```
2.  **Run the backend servers**:
    Open three separate terminals and run the following commands:
    ```bash
    python backend/task1_web_server.py
    ```
    ```bash
    python backend/task7_socket_server.py
    ```
    ```bash
    python backend/task10_txt_db.py
    ```
3.  **Open the frontend**:
    Open `frontend/index.html` in your web browser.

## FAQ

**Q: Why are there two database instances?**
**A:** The two database instances are used for load balancing. The system distributes the load evenly between them based on the game PIN.

**Q: What is the purpose of the `task10_txt_db.py` service?**
**A:** This service provides a fallback database using a simple text file. It ensures that the system can continue to function even if the MySQL databases are unavailable.

**Q: How can I access the databases directly?**
**A:** You can use phpMyAdmin, which is available at `http://localhost:8081` when the Docker services are running.

## Development Workflow

- **Branching:** Create descriptive branches (`feature/`, `bugfix/`, `docs/`) off `main`. Never commit directly to `main`.
- **Merging:** Open a Pull Request (PR) for review before merging into `main`. Delete branches after merging.
