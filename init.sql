CREATE TABLE users (
    telegram_id BIGINT NOT NULL UNIQUE,
    timezone    VARCHAR(64)
);
INSERT INTO users VALUES (359667541, 'Europe/Moscow');

CREATE TABLE list (
    user_id             INTEGER REFERENCES users (telegram_id),
    list_name           VARCHAR(64) NOT NULL,
    item                VARCHAR(64),
    item_description    VARCHAR(256)
);

CREATE TYPE status_type AS ENUM ('Active', 'Paused', 'Disabled');
CREATE TABLE reminder (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES users (telegram_id),
    add_job_params  JSONB,
    content         VARCHAR(256),
    status          status_type
);
