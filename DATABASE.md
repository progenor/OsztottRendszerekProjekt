# Database Architecture and Logical Design

The project uses a distributed architecture with two identical databases (**`kahoot_clone_a`** and **`kahoot_clone_b`**) to ensure load balancing and redundancy.

---

## 1. Core Database Tables

The game's state and data are stored in a system of interconnected tables:

*   **Users**: Registered users (admins, players, hosts) and their login credentials (hashed passwords, salts).
*   **Quizzes**: The main container for quizzes, created by a host.
*   **Questions**: The specific questions belonging to a given quiz.
*   **Options**: Stores the possible answer choices (and the correct answers) for the questions.
*   **Sessions**: A live, active game instance of a quiz, accessible to players via a unique `Game_PIN`.
*   **Session_Players**: Tracks which users have joined an active game and their current scores.
*   **Answers**: The actual votes/answers submitted by players during a live game.

---

## 2. Dynamic Question Handling

The system's greatest strength is its ability to handle different question types within a single, unified database schema. This is controlled by the `Question_type` **ENUM** field in the `Questions` table:

| Question Type | Description |
| :--- | :--- |
| **`SINGLE_CHOICE`** | Only one correct answer can be selected. |
| **`MULTIPLE_CHOICE`** | Multiple correct answers can be selected by the user. |
| **`TRUE_FALSE`** | A specialized choice question with only two options. |
| **`OPEN_TEXT`** | The player can freely type a text-based answer. |

---

## 3. Data Storage Logic

The table structure flexibly adapts depending on whether the player is selecting a predefined option or typing custom text.

### A. Choice-Based Questions (`SINGLE`, `MULTIPLE`, `TRUE_FALSE`)
*   **How options are stored (`Options` table):** Every possible choice is a separate row. The `Is_correct` field (**TRUE/FALSE**) marks the right answer(s).
*   **What is saved upon answering (`Answers` table):** We store the specific `Option_ID` of the selected choice. Since there is no typed text, the `Answer_text` field remains `NULL`.

### B. Open Text Questions (`OPEN_TEXT`)
*   **How options are stored (`Options` table):** The correct answer(s) are still recorded here for automated grading purposes.
*   **What is saved upon answering (`Answers` table):** Because the player doesn't select a pre-existing option, the `Option_ID` field remains `NULL`. The raw text typed by the user is saved directly into the `Answer_text` field.

---

## 4. Answer Evaluation (Backend Logic)

Score calculation (on the server side) differs based on the question type:

> [!TIP]
> **Choice-Based:** The system checks the `Option_ID` submitted in the `Answers` table and verifies if the corresponding row in the `Options` table has `Is_correct = TRUE`.

> [!TIP]
> **Open Text:** The system compares the content of the `Answer_text` submitted by the player against the `Option_text` values marked as correct in the database (usually in a case-insensitive manner).
