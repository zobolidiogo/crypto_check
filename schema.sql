CREATE TABLE T_USUARIO (
    id_usuario SERIAL PRIMARY KEY,

    nm_display VARCHAR(20) NOT NULL,

    nm_usuario VARCHAR(20) UNIQUE NOT NULL,

    ds_email VARCHAR(255) UNIQUE NOT NULL,

    st_email_verificado BOOLEAN NOT NULL DEFAULT FALSE,

    cd_hash TEXT NOT NULL,

    qt_dinheiro NUMERIC NOT NULL DEFAULT 10000,

    dt_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE T_TRANSACAO (
    id_transacao SERIAL PRIMARY KEY,

    id_usuario INTEGER NOT NULL,

    nm_crypto TEXT NOT NULL,

    qt_crypto NUMERIC NOT NULL,

    vl_unitario_usd NUMERIC NOT NULL,

    tp_transacao TEXT NOT NULL
        CHECK (tp_transacao IN ('BUY', 'SELL')),

    dt_transacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_usuario)
        REFERENCES T_USUARIO(id_usuario)
        ON DELETE CASCADE
);

CREATE TABLE T_CODIGO_EMAIL (
    id_codigo SERIAL PRIMARY KEY,

    id_usuario INTEGER NOT NULL,

    cd_codigo VARCHAR(6) NOT NULL,

    tp_codigo VARCHAR(20) NOT NULL
        CHECK (
            tp_codigo IN (
                'VERIFY_EMAIL',
                'RESET_PASSWORD'
            )
        ),

    dt_expiracao TIMESTAMP NOT NULL,

    st_utilizado BOOLEAN NOT NULL DEFAULT FALSE,

    FOREIGN KEY (id_usuario)
        REFERENCES T_USUARIO(id_usuario)
        ON DELETE CASCADE
);