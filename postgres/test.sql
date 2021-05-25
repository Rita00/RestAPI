----------------------------------------------------------------------------------------
-- psql -h localhost -p 5432 -d bidyourauction_db -U bidyourauction -w bidyourauction
----------------------------------------------------------------------------------------
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
INSERT INTO feed_message (message_id, type, participant_person_id, auction_id, message_message, message_message_date)
VALUES (1, 'question', 14, 3, 'Teste detalhes leilão e mensagens', date('now'));
INSERT INTO feed_message (message_id, type, participant_person_id, auction_id, message_message, message_message_date)
VALUES (2, 'comment', 14, 3, 'Teste detalhes leilão e várias mensagens', date('now'));
INSERT INTO feed_message (message_id, type, participant_person_id, auction_id, message_message, message_message_date)
VALUES (3, 'clarification', 14, 3, 'Teste detalhes leilão e várias mensagens2', date('now'));
INSERT INTO feed_message (message_id, type, participant_person_id, auction_id, message_message, message_message_date)
VALUES (4, 'question', 14, 1, 'Teste detalhes leilão e várias mensagens3', date('now'));

SELECT id, end_date, description, message_id, message_message FROM auction, textual_description, feed_message WHERE auction.id = textual_description.auction_id AND feed_message.auction_id = auction.id;