CREATE DATABASE IF NOT EXISTS userdb;
USE userdb;

-- Crea la tabella se non esiste
CREATE TABLE IF NOT EXISTS users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255),
  password VARCHAR(256)
);

-- $2b$12$jizAKAAoD1Fi7J8yx06gKuPhFGyq1fkAOlyKEkP0QL2h0KY18ITSO -> password123
-- $2b$12$UQPnIjwpm7KQFdJCzvawuuoivoA9ztGBboWTHGwRtRmFT/v7NZqMi -> newpassword

-- Inserisci utenti solo se la tabella è vuota
INSERT INTO users (name, email, password)
SELECT * FROM (
  SELECT 'Mario Rossi', 'mario.rossi@example.com', '$2b$12$jizAKAAoD1Fi7J8yx06gKuPhFGyq1fkAOlyKEkP0QL2h0KY18ITSO'
  UNION ALL
  SELECT 'Luca Bianchi', 'luca.bianchi@example.com', '$2b$12$UQPnIjwpm7KQFdJCzvawuuoivoA9ztGBboWTHGwRtRmFT/v7NZqMi'
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM users);