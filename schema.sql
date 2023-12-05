CREATE TABLE users (id SERIAL PRIMARY KEY, first_name TEXT, username TEXT, password TEXT, is_admin BOOLEAN);
CREATE TABLE secure_users (id SERIAL PRIMARY KEY, first_name TEXT, username TEXT, password TEXT, is_admin BOOLEAN);
CREATE TABLE messages (id SERIAL PRIMARY KEY, message TEXT, user_id INTEGER REFERENCES users, sent_at TIMESTAMP, visibility BOOLEAN);