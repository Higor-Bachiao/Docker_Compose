-- DESAFIO P09: indice explicito na coluna ra.
-- Obs.: a constraint UNIQUE de 01-schema.sql ja cria um indice implicito
-- (alunos_ra_key). Este aqui e didatico; em producao seria redundante.
CREATE INDEX IF NOT EXISTS idx_alunos_ra ON alunos (ra);
