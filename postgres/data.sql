DROP TABLE IF EXISTS auction CASCADE;
DROP TABLE IF EXISTS bid CASCADE;
DROP TABLE IF EXISTS notification CASCADE;
DROP TABLE IF EXISTS feed_message CASCADE;
DROP TABLE IF EXISTS admin CASCADE;
DROP TABLE IF EXISTS participant CASCADE;
DROP TABLE IF EXISTS textual_description CASCADE;
DROP TABLE IF EXISTS admin_auction CASCADE;
DROP TABLE IF EXISTS admin_user CASCADE;

CREATE TABLE auction (
	id 						SERIAL,
	code 					BIGINT NOT NULL,
	min_price 				FLOAT(8) NOT NULL,
	begin_date 				TIMESTAMP NOT NULL,
	end_date 				TIMESTAMP NOT NULL,
	iscancelled 			BOOL NOT NULL DEFAULT false,
	isactive 				BOOL NOT NULL DEFAULT true,
	participant_person_id 	INTEGER NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE bid (
	id 							SERIAL,
	bid_date 					TIMESTAMP NOT NULL,
	price 						FLOAT(8) NOT NULL,
	isinvalided 				BOOL NOT NULL DEFAULT false,
	participant_person_id 		INTEGER NOT NULL,
	auction_id 					INTEGER NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE notification (
	bid_id 						INTEGER NOT NULL,
	message_id 					INTEGER,
	message_message 			VARCHAR(512) NOT NULL,
	message_message_date 		TIMESTAMP NOT NULL,
	PRIMARY KEY(message_id)
);

CREATE TABLE feed_message (
	category 					VARCHAR(512) NOT NULL,
	participant_person_id 		INTEGER NOT NULL,
	auction_id 					INTEGER NOT NULL,
	message_id 					INTEGER,
	message_message 			VARCHAR(512) NOT NULL,
	message_message_date 		TIMESTAMP NOT NULL,
	PRIMARY KEY(message_id)
);

CREATE TABLE admin (
	person_id	 			SERIAL,
	person_username 		VARCHAR(512) UNIQUE NOT NULL,
	person_email	 		VARCHAR(512) UNIQUE NOT NULL,
	person_password 		VARCHAR(512) NOT NULL,
	person_token			VARCHAR(512) UNIQUE,
	PRIMARY KEY(person_id)
);

CREATE TABLE participant (
	person_id	 		SERIAL,
	person_username 	VARCHAR(512) UNIQUE NOT NULL,
	person_email	 	VARCHAR(512) UNIQUE NOT NULL,
	person_password 	VARCHAR(512) NOT NULL,
	person_token		VARCHAR(512) UNIQUE,
	isbanned	 		BOOL NOT NULL DEFAULT false,
	PRIMARY KEY(person_id)
);

CREATE TABLE textual_description (
	v	 				INTEGER NOT NULL,
	title		 		VARCHAR(512),
	description_text	VARCHAR(512),
	alteration_date 	TIMESTAMP,
	auction_id	 		INTEGER,
	PRIMARY KEY(v,auction_id)
);

CREATE TABLE admin_auction (
	admin_person_id 	INTEGER NOT NULL,
	auction_id	 		INTEGER,
	PRIMARY KEY(auction_id)
);

CREATE TABLE admin_participant (
	admin_person_id	 		INTEGER NOT NULL,
	participant_person_id 	INTEGER,
	PRIMARY KEY(participant_person_id)
);

ALTER TABLE auction ADD CONSTRAINT auction_fk1 FOREIGN KEY (participant_person_id) REFERENCES participant(person_id);
ALTER TABLE bid ADD CONSTRAINT bid_fk1 FOREIGN KEY (participant_person_id) REFERENCES participant(person_id);
ALTER TABLE bid ADD CONSTRAINT bid_fk2 FOREIGN KEY (auction_id) REFERENCES auction(id);
ALTER TABLE notification ADD CONSTRAINT notification_fk1 FOREIGN KEY (bid_id) REFERENCES bid(id);
ALTER TABLE feed_message ADD CONSTRAINT feed_message_fk1 FOREIGN KEY (participant_person_id) REFERENCES participant(person_id);
ALTER TABLE feed_message ADD CONSTRAINT feed_message_fk2 FOREIGN KEY (auction_id) REFERENCES auction(id);
ALTER TABLE feed_message ADD CONSTRAINT category CHECK (category in ('comment', 'question','clarification'));
ALTER TABLE textual_description ADD CONSTRAINT textual_description_fk1 FOREIGN KEY (auction_id) REFERENCES auction(id);
ALTER TABLE admin_auction ADD CONSTRAINT admin_auction_fk1 FOREIGN KEY (admin_person_id) REFERENCES admin(person_id);
ALTER TABLE admin_auction ADD CONSTRAINT admin_auction_fk2 FOREIGN KEY (auction_id) REFERENCES auction(id);
ALTER TABLE admin_participant ADD CONSTRAINT admin_participant_fk1 FOREIGN KEY (admin_person_id) REFERENCES admin(person_id);
ALTER TABLE admin_participant ADD CONSTRAINT admin_participant_fk2 FOREIGN KEY (participant_person_id) REFERENCES participant(person_id);