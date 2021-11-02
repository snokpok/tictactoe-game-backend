DROP TABLE IF EXISTS defaultdb.public.games CASCADE;
DROP TABLE IF EXISTS defaultdb.public.moves CASCADE;

CREATE TABLE defaultdb.public.games (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    players STRING[] NOT NULL,
    winner STRING DEFAULT NULL
);

CREATE TABLE defaultdb.public.moves (
    game UUID NOT NULL REFERENCES games(id) ON DELETE NO ACTION,
    number INTEGER NOT NULL,
    coord INT[] NOT NULL,
    player STRING NOT NULL
);
