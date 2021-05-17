-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS article;
DROP TABLE IF EXISTS INTERACTION_USER;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE article (
  article_id INTEGER PRIMARY KEY AUTOINCREMENT,
  category_id INTEGER NOT NULL,
  created_at_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  publisher_id INTEGER NOT NULL,
  words_count INTEGER NOT NULL
);

CREATE TABLE INTERACTION_USER (
  session_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  session_start TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  session_size INTEGER NOT NULL,
  click_article_id INTEGER NOT NULL,
  click_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  click_environment INTEGER NOT NULL,
  click_deviceGroup INTEGER NOT NULL,
  click_os INTEGER NOT NULL,
  click_country INTEGER NOT NULL,
  click_region INTEGER NOT NULL,
  click_referrer_type INTEGER NOT NULL,
  FOREIGN KEY (click_article_id) REFERENCES article (article_id)
);