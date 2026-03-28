USE kahoot_clone_a;

-- Insert Users
INSERT INTO Users (Role, Email, Password_Salt, Password_Hash, UserName) VALUES
('admin', 'admin@example.com', 'salt1', 'hash1', 'AdminUser'),
('host', 'host@example.com', 'salt2', 'hash2', 'HostUser'),
('player', 'player1@example.com', 'salt3', 'hash3', 'PlayerOne'),
('player', 'player2@example.com', 'salt4', 'hash4', 'PlayerTwo'),
('player', 'player3@example.com', 'salt5', 'hash5', 'PlayerThree');

-- Insert Quizzes
INSERT INTO Quizzes (Creator_ID, Title, Description) VALUES
(2, 'General Knowledge Quiz', 'A fun quiz to test your general knowledge.'),
(2, 'Tech Trivia', 'Questions about programming and technology.');

-- Insert Questions
INSERT INTO Questions (Quiz_ID, Question_type, Question_text, Points, Time_limit) VALUES
-- Quiz 1 Questions
(1, 'SINGLE_CHOICE', 'What is the capital of France?', 100, 30),
(1, 'TRUE_FALSE', 'The Earth is flat.', 100, 20),
(1, 'OPEN_TEXT', 'Which planet is known as the Red Planet?', 200, 60),
-- Quiz 2 Questions
(2, 'MULTIPLE_CHOICE', 'Which of these are programming languages?', 150, 45),
(2, 'SINGLE_CHOICE', 'What does HTML stand for?', 100, 30);

-- Insert Options
INSERT INTO Options (Question_ID, Option_text, Is_correct) VALUES
-- Options for Q1 (Capital of France)
(1, 'London', FALSE),
(1, 'Berlin', FALSE),
(1, 'Paris', TRUE),
(1, 'Madrid', FALSE),
-- Options for Q2 (Earth is flat)
(2, 'True', FALSE),
(2, 'False', TRUE),
-- Options for Q3 (Red Planet - OPEN_TEXT, we store the correct answer here)
(3, 'Mars', TRUE),
-- Options for Q4 (Programming languages)
(4, 'Python', TRUE),
(4, 'Banana', FALSE),
(4, 'Java', TRUE),
(4, 'C++', TRUE),
-- Options for Q5 (HTML)
(5, 'Hyper Text Markup Language', TRUE),
(5, 'High Tech Machine Learning', FALSE),
(5, 'Hyperlinks and Text Markup Language', FALSE),
(5, 'Home Tool Markup Language', FALSE);

-- Insert Sessions
INSERT INTO Sessions (Quiz_ID, Host_ID, Game_PIN, Session_name, Start_time, Is_active) VALUES
(1, 2, '123456', 'Friday Night Trivia', NOW(), TRUE),
(2, 2, '654321', 'Tech Geeks Unite', NOW(), FALSE);

-- Insert Session Players
INSERT INTO Session_Players (Session_ID, User_ID, Score) VALUES
(1, 3, 100), -- PlayerOne in Session 1
(1, 4, 0),   -- PlayerTwo in Session 1
(1, 5, 300); -- PlayerThree in Session 1

-- Insert Answers (For Session 1)
INSERT INTO Answers (Session_ID, User_ID, Question_ID, Option_ID, Answer_text) VALUES
-- PlayerOne answers Q1 correctly
(1, 3, 1, 3, NULL),
-- PlayerTwo answers Q1 incorrectly
(1, 4, 1, 1, NULL),
-- PlayerThree answers Q3 correctly (Open text)
(1, 5, 3, NULL, 'Mars');


USE kahoot_clone_b;

-- Insert Users
INSERT INTO Users (Role, Email, Password_Salt, Password_Hash, UserName) VALUES
('admin', 'admin_b@example.com', 'salt1', 'hash1', 'AdminUserB'),
('host', 'host_b@example.com', 'salt2', 'hash2', 'HostUserB'),
('player', 'player1_b@example.com', 'salt3', 'hash3', 'PlayerOneB');

-- Insert Quizzes
INSERT INTO Quizzes (Creator_ID, Title, Description) VALUES
(2, 'Science Quiz', 'Test your science knowledge.');

-- Insert Questions
INSERT INTO Questions (Quiz_ID, Question_type, Question_text, Points, Time_limit) VALUES
(1, 'SINGLE_CHOICE', 'What is the chemical symbol for water?', 100, 30);

-- Insert Options
INSERT INTO Options (Question_ID, Option_text, Is_correct) VALUES
(1, 'H2O', TRUE),
(1, 'CO2', FALSE),
(1, 'O2', FALSE),
(1, 'NaCl', FALSE);

-- Insert Sessions
INSERT INTO Sessions (Quiz_ID, Host_ID, Game_PIN, Session_name, Start_time, Is_active) VALUES
(1, 2, '999999', 'Science Fair Prep', NOW(), TRUE);

-- Insert Session Players
INSERT INTO Session_Players (Session_ID, User_ID, Score) VALUES
(1, 3, 100);

-- Insert Answers
INSERT INTO Answers (Session_ID, User_ID, Question_ID, Option_ID, Answer_text) VALUES
(1, 3, 1, 1, NULL);