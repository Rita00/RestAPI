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

SELECT DISTINCT a.id, t.description
FROM auction a, textual_description t, bid b, participant p
WHERE b.participant_person_id=p.person_id and a.id=b.auction_id and a.id=t.auction_id and t.version=(
    SELECT MAX(t.version)
    FROM auction a, textual_description t
    WHERE a.id=t.auction_id and a.id=4
);


