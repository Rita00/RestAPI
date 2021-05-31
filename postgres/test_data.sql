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
VALUES (now(), 50.00, -5, -1);
INSERT INTO bid(bid_date, price, participant_person_id, auction_id)
VALUES (now(), 50.00, -5, -1);
INSERT INTO bid(bid_date, price, participant_person_id, auction_id)
VALUES (now(), 50.00, -5, -2);