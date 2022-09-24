DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS scores;
DROP TABLE IF EXISTS uXq;
DROP TABLE IF EXISTS messages;

CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT, password TEXT, admin BOOLEAN);
CREATE TABLE questions (id SERIAL PRIMARY KEY, question TEXT, choice1 TEXT, choice2 TEXT, choice3 TEXT, choice4 TEXT, answer INTEGER, keywords TEXT, userid INTEGER, flag BOOLEAN);
CREATE TABLE scores (id SERIAL PRIMARY KEY, questionid INTEGER, userid INTEGER, correct BOOLEAN);
CREATE TABLE uXq (id SERIAL PRIMARY KEY, questionid INTEGER, userid INTEGER);
CREATE TABLE messages (id SERIAL PRIMARY KEY, fromid INTEGER, toid INTEGER, content TEXT);
