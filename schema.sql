-- Digital Twin Türkiye — PostgreSQL Şema v0.1

CREATE TABLE IF NOT EXISTS macro_states (
    id            SERIAL PRIMARY KEY,
    simulation_id UUID NOT NULL,
    year          INTEGER NOT NULL,

    gdp              NUMERIC(15, 2),
    inflation        NUMERIC(6, 2),
    interest_rate    NUMERIC(6, 2),
    unemployment     NUMERIC(6, 2),
    currency_usd_try NUMERIC(10, 4),
    consumption      NUMERIC(15, 2),
    investment       NUMERIC(15, 2),

    created_at    TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_macro_states_simulation ON macro_states(simulation_id, year);

-- Gerçek veri snapshot'ları (TCMB + TÜİK)
CREATE TABLE IF NOT EXISTS real_data_snapshots (
    id            SERIAL PRIMARY KEY,
    period        CHAR(7) NOT NULL,  -- 'YYYY-QN' formatı, örn: '2023-Q4'
    source        VARCHAR(50),

    gdp              NUMERIC(15, 2),
    inflation        NUMERIC(6, 2),
    interest_rate    NUMERIC(6, 2),
    unemployment     NUMERIC(6, 2),
    currency_usd_try NUMERIC(10, 4),
    consumption      NUMERIC(15, 2),
    investment       NUMERIC(15, 2),

    fetched_at    TIMESTAMP DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_real_data_period ON real_data_snapshots(period, source);
