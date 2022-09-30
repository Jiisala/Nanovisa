DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS questions CASCADE;
DROP TABLE IF EXISTS answers_given;
DROP TABLE IF EXISTS users_x_questions;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS flagged_questions;


CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    name TEXT UNIQUE, 
    password TEXT, 
    admin BOOLEAN
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY, 
    question TEXT UNIQUE, 
    choice1 TEXT, 
    choice2 TEXT, 
    choice3 TEXT, 
    choice4 TEXT, 
    answer INTEGER, 
    keywords TEXT, 
    user_id INTEGER REFERENCES users ON DELETE CASCADE 
);

CREATE TABLE flagged_questions (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES questions ON DELETE CASCADE,
    flagger_id INTEGER REFERENCES users,
    reason TEXT
);
--For highscores, also used to calculate the relative hardesss of the question
CREATE TABLE answers_given (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES questions ON DELETE CASCADE, 
    user_id INTEGER REFERENCES users ON DELETE CASCADE, 
    correct BOOLEAN
);
--Collects together the questions added by each user
--Mainly used for convinience when needed 
--On further thought on the subject might be totally useless and get deleted soon
CREATE TABLE users_x_questions (
    id SERIAL PRIMARY KEY, 
    question_id INTEGER REFERENCES questions ON DELETE CASCADE, 
    user_id INTEGER REFERENCES users ON DELETE CASCADE 
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    from_id INTEGER REFERENCES users ON DELETE CASCADE,
    to_id INTEGER REFERENCES users ON DELETE CASCADE,
    content TEXT
);
