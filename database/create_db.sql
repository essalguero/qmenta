CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA users_schema;

CREATE SEQUENCE users_schema.user_id_seq START 1;

CREATE TABLE IF NOT EXISTS users_schema.user (
    id INT PRIMARY KEY NOT NULL DEFAULT nextval('users_schema.user_id_seq'),
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL);

INSERT INTO users_schema.user (username, password) VALUES (
  'johndoe@mail.com', 
  crypt('johnspassword', gen_salt('bf')) 
);

INSERT INTO users_schema.user (username, password) VALUES (
  'tim@qmenta.com', 
  crypt('tim@qmenta.com', gen_salt('bf')) 
);

INSERT INTO users_schema.user (username, password) VALUES (
  'essalguero@yahoo.es', 
  crypt('essalguero@yahoo.es', gen_salt('bf')) 
);
