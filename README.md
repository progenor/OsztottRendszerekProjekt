# OsztottRendszerekProjekt (Kahoot Clone)

## Development Workflow

- **Branching:** Create descriptive branches (`feature/`, `bugfix/`, `docs/`) off `main`. Never commit directly to `main`.
- **Merging:** Open a Pull Request (PR) for review before merging into `main`. Delete branches after merging.

## Local Environment Setup

We use Docker to run the database (MySQL 8.0) and phpMyAdmin.

### Prerequisites
1. Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).
2. Create a `.env` file in the project root:
   ```env
   DB_ROOT_PASSWORD=your_root_password
   DB_USER=your_user_name
   DB_PASSWORD=your_user_password
   ```

### Managing the Database

- **Start services:** `docker-compose up -d` (Includes dummy data on first run!)
- **Stop services:** `docker-compose down`
- **Full Reset (Deletes all data!):** `docker-compose down -v`

**Note:** On the very first startup (or after a reset), the database is automatically populated with dummy data for testing purposes from `database/seed.sql`.

### Accessing phpMyAdmin

Once running, access the database UI at: **http://localhost:8080**

- **Login:** Use `root` or your configured `DB_USER` and `DB_PASSWORD` from the `.env` file.
- **Purpose:** View tables, execute SQL queries, and manage data for `kahoot_clone_a` and `kahoot_clone_b`.

---

## Task 10 - Text File Database over Socket

For the alternative database task (no MySQL), a TCP socket server stores and returns votes from text files.

### Files

- `WebRPC/task10_textdb_server.py`: Threaded TCP server (one thread/client).
- `WebRPC/task10_textdb_client.py`: Simple client helper for write/read calls.
- `WebRPC/votes_data/*.jsonl`: One file per poll (`poll_id`).

### Why multiple files?

Each poll is stored in its own file (`<poll_id>.jsonl`), so different polls are naturally separated and easier to query.

### Concurrency

- The server handles clients concurrently using `socketserver.ThreadingMixIn`.
- File writes/reads are protected with per-poll locks (`threading.Lock`) to avoid race conditions.

### Protocol (newline-delimited JSON)

Request example:

```json
{"action":"submit_vote","data":{"poll_id":"quiz_1","question_id":1,"client_id":"Janos","answer":"igen"}}
```

Response example:

```json
{"status":"ok","data":{"saved":{"poll_id":"quiz_1","question_id":1,"client_id":"Janos","answer":"igen","sent_at":"..."}}}
```

Supported actions:

- `ping`
- `submit_vote`
- `get_votes`
- `get_results`
- `list_polls`

### Run

1. Start server:
   ```bash
   python WebRPC/task10_textdb_server.py
   ```
2. In another terminal run client demo:
   ```bash
   python WebRPC/task10_textdb_client.py
   ```

The demo inserts two votes and prints aggregated results.
