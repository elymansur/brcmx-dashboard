DROP TABLE IF EXISTS movimentacoes;

CREATE TABLE movimentacoes (
    ano INTEGER,
    mes INTEGER,
    ncm TEXT,
    descricao_ncm TEXT,
    uf TEXT,
    pais_id INTEGER,
    pais TEXT,
    peso_liquido REAL,
    valor_fob REAL,
    tipo_fluxo TEXT
);