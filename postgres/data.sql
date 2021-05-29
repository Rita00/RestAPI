DROP TABLE IF EXISTS auction CASCADE;
DROP TABLE IF EXISTS bid CASCADE;
DROP TABLE IF EXISTS notification CASCADE;
DROP TABLE IF EXISTS feed_message CASCADE;
DROP TABLE IF EXISTS admin CASCADE;
DROP TABLE IF EXISTS participant CASCADE;
DROP TABLE IF EXISTS textual_description CASCADE;
DROP TABLE IF EXISTS admin_auction CASCADE;
DROP TABLE IF EXISTS admin_user CASCADE;

--TABELAS===========================================
CREATE TABLE auction
(
    id                    SERIAL,
    code                  BIGINT    NOT NULL,
    min_price             FLOAT(8)  NOT NULL,
    begin_date            TIMESTAMP NOT NULL,
    end_date              TIMESTAMP NOT NULL,
    iscancelled           BOOL      NOT NULL DEFAULT false,
    isactive              BOOL      NOT NULL DEFAULT true,
    participant_person_id INTEGER   NOT NULL,
    maxbid                FLOAT(8),
    winner                VARCHAR(512),
    PRIMARY KEY (id)
);

CREATE TABLE bid
(
    id                    SERIAL,
    bid_date              TIMESTAMP NOT NULL,
    price                 FLOAT(8)  NOT NULL,
    isinvalided           BOOL      NOT NULL DEFAULT false,
    participant_person_id INTEGER   NOT NULL,
    auction_id            INTEGER   NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE notification
(
    participant_person_id INTEGER      NOT NULL,
    message_id            SERIAL,
    message_message       VARCHAR(512) NOT NULL,
    message_message_date  TIMESTAMP    NOT NULL,
    PRIMARY KEY (message_id)
);

CREATE TABLE feed_message
(
    type                  VARCHAR(512) NOT NULL,
    participant_person_id INTEGER      NOT NULL,
    auction_id            INTEGER      NOT NULL,
    message_id            SERIAL,
    message_message       VARCHAR(512) NOT NULL,
    message_message_date  TIMESTAMP    NOT NULL,
    PRIMARY KEY (message_id)
);

CREATE TABLE admin
(
    person_id       SERIAL,
    person_username VARCHAR(512) UNIQUE NOT NULL,
    person_email    VARCHAR(512) UNIQUE NOT NULL,
    person_password VARCHAR(512)        NOT NULL,
    person_token    VARCHAR(512) UNIQUE,
    PRIMARY KEY (person_id)
);

CREATE TABLE participant
(
    isbanned        BOOL                NOT NULL DEFAULT false,
    person_id       SERIAL,
    person_username VARCHAR(512) UNIQUE NOT NULL,
    person_email    VARCHAR(512) UNIQUE NOT NULL,
    person_password VARCHAR(512)        NOT NULL,
    person_token    VARCHAR(512) UNIQUE,
    PRIMARY KEY (person_id)
);

CREATE TABLE textual_description
(
    version         INTEGER NOT NULL,
    title           VARCHAR(512),
    description     VARCHAR(512),
    alteration_date TIMESTAMP,
    auction_id      INTEGER,
    PRIMARY KEY (version, auction_id)
);

CREATE TABLE admin_auction
(
    admin_person_id INTEGER NOT NULL,
    auction_id      INTEGER,
    PRIMARY KEY (auction_id)
);

CREATE TABLE admin_participant
(
    admin_person_id       INTEGER NOT NULL,
    participant_person_id INTEGER,
    PRIMARY KEY (participant_person_id)
);


ALTER TABLE auction
    ADD CONSTRAINT dates CHECK (end_date > now());
ALTER TABLE auction
    ADD CONSTRAINT auction_fk1 FOREIGN KEY (participant_person_id) REFERENCES participant (person_id);
ALTER TABLE bid
    ADD CONSTRAINT bid_fk1 FOREIGN KEY (participant_person_id) REFERENCES participant (person_id);
ALTER TABLE bid
    ADD CONSTRAINT bid_fk2 FOREIGN KEY (auction_id) REFERENCES auction (id);
ALTER TABLE notification
    ADD CONSTRAINT notification_fk1 FOREIGN KEY (participant_person_id) REFERENCES participant (person_id);
ALTER TABLE feed_message
    ADD CONSTRAINT feed_message_fk1 FOREIGN KEY (participant_person_id) REFERENCES participant (person_id);
ALTER TABLE feed_message
    ADD CONSTRAINT feed_message_fk2 FOREIGN KEY (auction_id) REFERENCES auction (id);
ALTER TABLE feed_message
    ADD CONSTRAINT type CHECK (type in ('comment', 'question', 'clarification'));
ALTER TABLE textual_description
    ADD CONSTRAINT textual_description_fk1 FOREIGN KEY (auction_id) REFERENCES auction (id);
ALTER TABLE admin_auction
    ADD CONSTRAINT admin_auction_fk1 FOREIGN KEY (admin_person_id) REFERENCES admin (person_id);
ALTER TABLE admin_auction
    ADD CONSTRAINT admin_auction_fk2 FOREIGN KEY (auction_id) REFERENCES auction (id);
ALTER TABLE admin_participant
    ADD CONSTRAINT admin_participant_fk1 FOREIGN KEY (admin_person_id) REFERENCES admin (person_id);
ALTER TABLE admin_participant
    ADD CONSTRAINT admin_participant_fk2 FOREIGN KEY (participant_person_id) REFERENCES participant (person_id);

--TRIGGERS=========================================
--drop
DROP TRIGGER IF EXISTS t_ban ON admin_participant;
DROP FUNCTION IF EXISTS  participant_banned() CASCADE;

--participant banned
CREATE OR REPLACE FUNCTION participant_banned()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- ban participant
    UPDATE participant SET isbanned=True WHERE new.participant_person_id=person_id;
    -- cancel participant auctions
    UPDATE auction SET iscancelled=True WHERE new.participant_person_id=participant_person_id;
    -- invalids participant bids
    UPDATE bid SET isinvalided=True WHERE new.participant_person_id=participant_person_id;
    -- invalids greaters bids
    UPDATE bid
    SET isinvalided=True
    FROM (
        SELECT MAX(price) maxprice_invalidated, auction_id aid
        FROM bid
        WHERE new.participant_person_id=participant_person_id
        GROUP BY auction_id
    ) AS subquery
    WHERE price > subquery.maxprice_invalidated AND auction_id=subquery.aid;
    -- sets the greater bid to the max price of banned user bid
    UPDATE bid
    SET price = subquery.maxprice,
        auction_id = subquery.aid
    FROM (
        SELECT MAX(price) maxprice,auction_id aid
        FROM bid
        WHERE new.participant_person_id=participant_person_id
        GROUP BY aid
    ) AS subquery
    WHERE (price,auction_id) IN (
        SELECT MAX(price), auction_id aid
        FROM bid
        WHERE new.participant_person_id!=participant_person_id
        GROUP BY aid
    );
    -- laments the incomodo
    -- TODO
    RETURN new;
END;
$$;
CREATE TRIGGER tai_ban
    AFTER INSERT
    ON admin_participant
    FOR EACH ROW
    EXECUTE PROCEDURE participant_banned();


--finished auctions
CREATE OR REPLACE PROCEDURE public.finish_auctions()
    LANGUAGE plpgsql as
$$
DECLARE
    c1 cursor for
        SELECT *
        FROM auction
        WHERE isactive = True AND end_date < now()
            for update;

BEGIN
    for r in c1
        loop
            UPDATE auction SET isactive = false, winner = (SELECT person_username
                          FROM bid,
                               participant
                          WHERE bid.participant_person_id = participant.person_id and auction_id = r.id
                          ORDER BY price desc
                          limit 1), maxbid = (SELECT max(price) FROM bid WHERE auction_id = r.id) WHERE id = r.id;
        end loop;
END;
$$;
--DADOS TESTE===========================================
--Pessoas teste
INSERT INTO participant (person_id, person_username, person_email, person_password)
VALUES (-1, 'dylanperdigao', 'dylanperdigao@email.com', 'password');
INSERT INTO participant (person_id, person_username, person_email, person_password)
VALUES (-2, 'brunofaria', 'brunofaria@email.com', 'password');
INSERT INTO participant (person_id, person_username, person_email, person_password)
VALUES (-3, 'ritarodrigues', 'ritarodrigues@email.com', 'password');
INSERT INTO admin (person_id, person_username, person_email, person_password)
VALUES (-4, 'dylanadmin', 'dylanadmin@email.com', 'password');
INSERT INTO participant (person_id, person_username, person_email, person_password)
VALUES (-5, 'dylantoban', 'dylantoban@email.com', 'password');

--Leiloes teste
INSERT INTO auction (id, code, min_price, begin_date, end_date, participant_person_id)
VALUES (-1, 111111111, 10.00, NOW(), '2022-12-30T23:59:59', -1);
INSERT INTO textual_description (version, title, description, alteration_date, auction_id)
VALUES (1, 'Leilao -1', 'Desc v1', '2021-01-01T00:00:00', -1);
INSERT INTO textual_description (version, title, description, alteration_date, auction_id)
VALUES (2, 'Leilao -1', 'Desc v2', NOW(), -1);
--
INSERT INTO auction (id, code, min_price, begin_date, end_date, participant_person_id)
VALUES (-2, 111111112, 20.00, NOW(), '2022-12-30T23:59:59', -1);
INSERT INTO textual_description (version, title, description, alteration_date, auction_id)
VALUES (1, 'Leilao -2', 'Desc v1', '2021-05-24', -2);

--Licitacoes teste
INSERT INTO bid(bid_date, price, participant_person_id, auction_id)
VALUES (now(), 30.00, -1, -1);
INSERT INTO bid(bid_date, price, participant_person_id, auction_id)
VALUES (now(), 40.00, -1, -1);
INSERT INTO bid(bid_date, price, participant_person_id, auction_id)
VALUES (now(), 40.00, -1, -2);