
CREATE TABLE userdata (
   user_id varchar(128) PRIMARY KEY,
   email varchar(512),
   plan_type varchar(32) not null,
   plan_limit int DEFAULT 0,
);


CREATE TABLE payment (
   id bigserial PRIMARY KEY,
   user_id varchar(128) not null,
   created timestamp not null,
   email varchar(512),
   plan_type varchar(32),
   amount_total int,
   stripe_id text
);

CREATE TABLE conversation (
   conversation_id varchar(128) PRIMARY KEY,
   user_id varchar(128) not null,
   created timestamp not null,
   active int default 1,
   title VARCHAR(255)
);

CREATE TABLE message (
    message_id bigserial PRIMARY KEY,
    conversation_id varchar(128) not null,
    user_id varchar(128) not null,
    created timestamp not null,
    date date not null,
    role varchar(12) not null,
    content text
);

CREATE INDEX idx_user_id_date ON message (user_id, date);

CREATE TABLE messagefeedback (
   id bigserial PRIMARY KEY,
   user_id varchar(128) not null,
   message_id bigserial not null,
   created_at timestamp not null,
   feedback integer
);