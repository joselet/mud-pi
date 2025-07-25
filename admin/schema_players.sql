drop table if exists players;
CREATE TABLE IF NOT EXISTS players (
    name TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    nivel INTEGER DEFAULT 0,
    clon INTEGER DEFAULT 1,
    pv INTEGER DEFAULT 100,
    e INTEGER DEFAULT 100,
    f INTEGER DEFAULT 10,
    r INTEGER DEFAULT 10,
    a INTEGER DEFAULT 10,
    d INTEGER DEFAULT 10,
    p INTEGER DEFAULT 10,
    c INTEGER DEFAULT 10,
    tm INTEGER DEFAULT 10,
    pm INTEGER DEFAULT 10,
    servicio TEXT,
    sociedad_secreta TEXT,
    sector TEXT,
    room TEXT DEFAULT 'inicio'
);
