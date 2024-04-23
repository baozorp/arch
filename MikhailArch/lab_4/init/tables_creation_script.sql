DROP INDEX IF EXISTS user_id_index;
DROP INDEX IF EXISTS user_name_index;
DROP INDEX IF EXISTS first_name_index;
DROP INDEX IF EXISTS second_name_index;
DROP INDEX IF EXISTS chat_id_index;
DROP INDEX IF EXISTS is_group_index;
DROP INDEX IF EXISTS members_id_index;
DROP INDEX IF EXISTS chat_members_id_index;

DROP TABLE IF EXISTS chat_members;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS chats;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(255) UNIQUE,
    first_name VARCHAR(255),
    second_name VARCHAR(255),
    password VARCHAR(255)
);

-- CREATE INDEX user_id_index ON users (user_id);
-- CREATE INDEX user_name_index ON users (user_name);
-- CREATE INDEX first_name_index ON users (first_name);
-- CREATE INDEX second_name_index ON users (second_name);

-- CREATE TABLE chats (
--     chat_id SERIAL PRIMARY KEY,
--     chat_name VARCHAR(100) NOT NULL,
--     is_group BIT NOT NULL,
--     mongo_id VARCHAR(100) UNIQUE NOT NULL
-- );
-- CREATE INDEX chat_id_index ON chats (chat_id);
-- CREATE INDEX is_group_index ON chats (is_group);

-- CREATE TABLE chat_members (
--     id SERIAL PRIMARY KEY,
--     user_id INT REFERENCES users(user_id),
--     chat_id INT REFERENCES chats(chat_id),
--     UNIQUE (user_id, chat_id)
-- );
-- CREATE INDEX members_id_index ON chat_members (user_id);
-- CREATE INDEX chat_members_id_index ON chat_members (chat_id);