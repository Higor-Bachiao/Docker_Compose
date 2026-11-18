-- Seed proprio (turma ficticia) - executado na 1a inicializacao do volume
INSERT INTO alunos (nome, ra, periodo) VALUES
    ('Marina Tavares',  '2023101', 8),
    ('Otávio Rezende',  '2023102', 8),
    ('Letícia Campos',  '2023103', 7),
    ('Rafael Nogueira', '2023104', 8)
ON CONFLICT (ra) DO NOTHING;
