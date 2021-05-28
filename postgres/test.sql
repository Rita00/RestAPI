-- SignUp
INSERT INTO participant (person_username,person_email,person_password,person_token)
VALUES ('dylan','dylan@email.com','12345','qwertzuiopasdfghjklyxcvbnm');

--- Simular Leilões
SELECT * FROM auction;
SELECT * FROM textual_description;
INSERT INTO auction (code, min_price, begin_date, end_date, participant_person_id)
VALUES (123456789, 12.30, '2021-04-12', '2021-06-08', 1);
INSERT INTO textual_description (version, title, description, alteration_date, auction_id)
VALUES (1, 'teste', 'Isto é um teste para pesquisa por leilões', '2021-05-24', 1);

INSERT INTO auction (code, min_price, begin_date, end_date, participant_person_id)
VALUES (111111111, 12.30, '2021-04-12', '2021-06-08', 1);
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
VALUES (111111111, 10.00, '2021-01-01T00:00:00', '2022-12-30T23:59:59', 15);
INSERT INTO textual_description (version, title, description, alteration_date, auction_id)
VALUES (1, 'Leilao4', 'Teste mostrar leiloes em que um utilizador tenha atividade v1', '2021-01-01T00:00:00', 4);
INSERT INTO textual_description (version, title, description, alteration_date, auction_id)
VALUES (2, 'Leilao4', 'Teste mostrar leiloes em que um utilizador tenha atividade v2', NOW(), 4);
INSERT INTO auction (code, min_price, begin_date, end_date, participant_person_id)
VALUES (111111112, 20.00, '2021-01-01T00:00:00', '2022-12-30T23:59:59', 15);
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

