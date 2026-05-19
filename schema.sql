CREATE TABLE T_USUARIO (
    id_usuario SERIAL PRIMARY KEY,
    nm_usuario VARCHAR(20) UNIQUE NOT NULL,
    cd_hash TEXT NOT NULL,
    qt_dinheiro NUMERIC NOT NULL DEFAULT 10000
);

CREATE TABLE T_TRANSACAO (
    id_transacao SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    nm_crypto TEXT NOT NULL,
    qt_crypto NUMERIC NOT NULL,
    vl_unitario_usd NUMERIC NOT NULL,
    tp_transacao TEXT NOT NULL CHECK (tp_transacao IN ('BUY', 'SELL')),
    dt_transacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_usuario)
        REFERENCES T_USUARIO(id_usuario)
);