----------------------------------------------------------------------------------------
-- psql -h localhost -p 5432 -d bidyourauction_db -U bidyourauction -w bidyourauction
----------------------------------------------------------------------------------------
-- SignUp
INSERT INTO participant (person_username,person_email,person_password,person_token)
VALUES ('dylan','dylan@email.com','12345','qwertzuiopasdfghjklyxcvbnm');