-- SignUp
INSERT INTO participant (person_id, person_username,person_email,person_password)
VALUES (17, 'teste','teste@email.com','12345');

--- Simular Leilões
SELECT * FROM auction;
SELECT * FROM textual_description;
INSERT INTO auction (code, min_price, begin_date, end_date, participant_person_id)
VALUES (123456789, 12.30, '2021-04-12', '2021-06-08', -1);
INSERT INTO textual_description (version, title, description, alteration_date, auction_id)
VALUES (1, 'teste', 'Isto é um teste para pesquisa por leilões', '2021-05-24', 2);

INSERT INTO auction (code, min_price, begin_date, end_date, participant_person_id)
VALUES (111111111, 12.30, '2021-04-12', '2021-06-08', -1);
INSERT INTO textual_description (version, title, description, alteration_date, auction_id)
VALUES (1, 'teste', 'Isto é um teste para pesquisa2 por leilões', '2021-05-24', 3);

SELECT id, description FROM auction, textual_description
        WHERE auction.id = textual_description.auction_id
        AND (auction.code::text = '%pesquisa%' OR textual_description.description like '%pesquisa%');

--- Criar mensagens
SELECT * from feed_message;
INSERT INTO feed_message (type, participant_person_id, auction_id, message_message, message_message_date)
VALUES ('question', 14, 3, 'Teste detalhes leilão e mensagens', date('now'));
INSERT INTO feed_message (type, participant_person_id, auction_id, message_message, message_message_date)
VALUES ('comment', 14, 3, 'Teste detalhes leilão e várias mensagens', date('now'));
INSERT INTO feed_message (type, participant_person_id, auction_id, message_message, message_message_date)
VALUES ('clarification', 14, 3, 'Teste detalhes leilão e várias mensagens2', date('now'));
INSERT INTO feed_message (type, participant_person_id, auction_id, message_message, message_message_date)
VALUES ('question', 14, 1, 'Teste detalhes leilão e várias mensagens3', date('now'));
INSERT INTO feed_message (type, participant_person_id, auction_id, message_message, message_message_date)
VALUES ('question', 14, 1, 'Teste detalhes leilão e mensagens', date('now'));

INSERT INTO bid(bid_date, price, participant_person_id, auction_id)
VALUES(now(),30.00,17,1);
INSERT INTO bid(bid_date, price, participant_person_id, auction_id)
VALUES(now(),30.50,17,1);

SELECT id, end_date, description, message_id, message_message FROM auction, textual_description, feed_message WHERE auction.id = textual_description.auction_id AND feed_message.auction_id = auction.id;
SELECT id, person_username FROM bid, participant WHERE bid.participant_person_id = participant.person_id;
SELECT message_id, message_message FROM feed_message WHERE auction_id = '1';
SELECT * FROM bid;
SELECT id, person_username FROM bid, participant WHERE bid.participant_person_id = participant.person_id AND auction_id = 1;

-- Mostrar leiloes em que um utilizador tenha atividade
INSERT INTO auction (code, min_price, begin_date, end_date, participant_person_id)
VALUES (111111111, 10.00, '2021-01-01T00:00:00', '2022-12-30T23:59:59', -2);
INSERT INTO textual_description (version, title, description, alteration_date, auction_id)
VALUES (1, 'Leilao4', 'Teste mostrar leiloes em que um utilizador tenha atividade v1', '2021-01-01T00:00:00', 4);
INSERT INTO textual_description (version, title, description, alteration_date, auction_id)
VALUES (2, 'Leilao4', 'Teste mostrar leiloes em que um utilizador tenha atividade v2', NOW(), 4);
INSERT INTO auction (code, min_price, begin_date, end_date, participant_person_id)
VALUES (111111112, 20.00, '2021-01-01T00:00:00', '2022-12-30T23:59:59', -2);
INSERT INTO textual_description (version, title, description, alteration_date, auction_id)
VALUES (1, 'Leilao5', 'Teste mostrar leiloes em que um utilizador tenha atividade v1', '2021-05-24', 5);
INSERT INTO bid(bid_date, price, participant_person_id, auction_id)
VALUES(now(),30.00,17,4);
INSERT INTO bid(bid_date, price, participant_person_id, auction_id)
VALUES(now(),40.00,17,4);
INSERT INTO bid(bid_date, price, participant_person_id, auction_id)
VALUES(now(),40.00,17,5);

SELECT t.auction_id, t.description
FROM textual_description t
WHERE (t.auction_id,t.version) IN (
    SELECT DISTINCT a.id, MAX(t.version)
    FROM auction a,
         textual_description t
    WHERE a.id = t.auction_id
    GROUP BY a.id
    HAVING a.id IN (
        SELECT b.auction_id
        FROM bid b
        WHERE b.participant_person_id IN (
            SELECT p.person_id
            FROM participant p
            WHERE p.person_username LIKE 'dylan2'
        )
    )
);

SELECT b.id, person_username
FROM bid b, participant p
WHERE b.participant_person_id=p.person_id
ORDER BY b.bid_date DESC;

SELECT * FROM participant WHERE person_username = 'Rita' AND person_password = 'rita.lapao00@mail.com';
select * from participant;
SELECT isbanned FROM participant WHERE person_username = 'username';

SELECT id, code, min_price, begin_date, end_date, person_username, title, description
FROM auction, participant, textual_description
WHERE auction.participant_person_id = participant.person_id AND auction.id = textual_description.auction_id AND auction.id = 1;

SELECT * FROM auction JOIN participant on auction.participant_person_id = participant.person_id AND participant.person_username = 'username' AND auction.id = 1;

INSERT INTO textual_description(version, title, description, alteration_date, auction_id) VALUES(2, 'ola', 'olaaa', now(), 1);
SELECT id, code, min_price, begin_date, end_date, person_username, title, description FROM auction, participant, textual_description WHERE auction.participant_person_id = participant.person_id AND auction.id = textual_description.auction_id AND auction.id = 1;

UPDATE auction SET isactive = false WHERE end_date < now();

SELECT person_username FROM bid, participant WHERE bid.participant_person_id = participant.person_id AND auction_id = 1 ORDER BY price desc limit 1;

SELECT 'now()';

call finish_auctions();
SELECT *
        FROM auction
        WHERE isactive = True AND end_date < now();

UPDATE auction SET isactive = false WHERE id = 3;

rollback;

select * from auction;
select relation::regclass, * from pg_locks where not granted;
vacuum analyse;
SELECT person_username FROM bid, participant
                          WHERE bid.participant_person_id = participant.person_id and auction_id = 1
                          ORDER BY price desc
                          limit 1;

SELECT id, description FROM auction, textual_description WHERE auction.id = textual_description.auction_id AND (auction.code::text = 'pesquisa' OR textual_description.description like '%pesquisa%') AND isactive = true

SELECT t.auction_id, t.description
FROM textual_description t
WHERE (t.auction_id,t.version)
        IN (SELECT DISTINCT a.id, MAX(t.version)
        FROM auction a, textual_description t
        WHERE a.id = t.auction_id
        GROUP BY a.id
        HAVING a.id IN (
        SELECT b.auction_id
        FROM bid b
        WHERE b.participant_person_id IN (
        SELECT p.person_id
        FROM participant p
        WHERE p.person_username LIKE 'dylan'
                                )
                            )
                        )

SELECT distinct on (auction.id) auction.id, description, version
FROM auction
    left join  bid on auction.id = bid.auction_id
    join textual_description on auction.id = textual_description.auction_id
WHERE (bid.participant_person_id = -1 or auction.participant_person_id = -1)
ORDER BY auction.id, version desc;

select * from bid;
select * from textual_description;


Select p.person_username,count(*) From bid b, participant p where b.participant_person_id=p.person_id group by p.person_username order by count(*) desc limit 10;

Select winner,count(*) From auction where winner IS NOT NULL group by winner order by count(*) desc limit 10;

select count(*) from auction where begin_date > current_date - interval '10' day;

SELECT id
FROM auction
WHERE code= 111111111 ORDER BY begin_date desc

UPDATE auction SET iscancelled = true, isactive = false WHERE id = 5;

SELECT person_id, id FROM participant, auction WHERE auction.participant_person_id = participant.person_id AND auction.id = 5;

select participant_person_id from auction where id = 4;

select participant_person_id, id from bid where auction_id = -1 union select participant_person_id, id from auction where id = -1;


SELECT DISTINCT b.participant_person_id
FROM bid b, auction a
WHERE b.auction_id IN (
    SELECT DISTINCT auction.id
    FROM auction,bid
    WHERE -1=bid.participant_person_id AND bid.auction_id=auction.id
    );
SELECT distinct on (auction.id) auction.id, description
        FROM auction, textual_description WHERE auction.id = textual_description.auction_id and (auction.code::text = 'v1' OR textual_description.description like '%v1%') AND isactive = true ORDER BY auction.id, version desc;

select * from textual_description where auction_id = 4;
select distinct auction_id from auction, textual_description WHERE auction.id = textual_description.auction_id and (auction.code::text = 'v1' OR textual_description.description like '%v1%') AND isactive = true;

SELECT distinct on (auction.id) auction.id, description FROM auction, textual_description WHERE auction.id = textual_description.auction_id AND auction_id = 4 ORDER BY auction.id, version desc;

SELECT isactive FROM auction WHERE id = 1;

SELECT max(price) as price FROM bid WHERE auction_id = 4;

SELECT count(*) FROM textual_description WHERE auction_id = -1;

SELECT * from auction WHERE id = 2;

SELECT participant_person_id
	INTO outbids_author
	FROM bid
	WHERE auction_id = 5 AND id != 5 AND participant_person_id != -1
	ORDER BY bid_date DESC
	LIMIT 1

SELECT person_id
                        FROM participant
                        WHERE person_username='dylanadmin';

SELECT * FROM auction
        WHERE isactive = True AND end_date < now();

select participant_person_id from bid, participant WHERE bid.participant_person_id = participant.person_id and auction_id = 4 ORDER BY price desc
                    limit 1;

select person_username FROM participant WHERE person_id = 2 and isbanned != False

select * from auction where isactive = true and end_date < now();
update auction set isactive = false WHERE id = 4;
UPDATE auction SET isactive = false WHERE isactive = true and end_date < now();

select participant_person_id
        from bid,
             participant
        WHERE bid.participant_person_id = participant.person_id
          and auction_id = 2
        ORDER BY price desc
        limit 1;

select person_username
        FROM participant
        WHERE person_id = -1
          and isbanned = False;

UPDATE auction SET winner = 'dylanperdigao' WHERE id = 2;

select max(price) as price from bid WHERE auction_id = 2 AND bid.isinvalided = false;

SELECT distinct a.id
        FROM bid b left join
             auction a on b.auction_id = a.id where (-5 = b.participant_person_id or -5 = a.participant_person_id);

SELECT distinct auction.id
FROM auction
    left join  bid on auction.id = bid.auction_id
WHERE (bid.participant_person_id = -5 or auction.participant_person_id = -5)