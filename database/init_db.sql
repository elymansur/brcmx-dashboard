
DROP TABLE IF EXISTS movimentacoes;

CREATE TABLE movimentacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ano INTEGER,
    mes INTEGER,
    tipo_fluxo TEXT,
    ncm TEXT,
    descricao_ncm TEXT,
    uf TEXT,
    pais_id INTEGER,
    pais TEXT,
    peso_liquido REAL,
    valor_fob REAL
);
