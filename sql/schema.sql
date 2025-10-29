-- SQLite schema for rental + macro datasets

CREATE TABLE IF NOT EXISTS rents (
    year INTEGER PRIMARY KEY,
    avg_rent REAL,
    vacancy_rate REAL,
    source TEXT DEFAULT 'CMHC'
);

CREATE TABLE IF NOT EXISTS interest_rates (
    year INTEGER PRIMARY KEY,
    interest_rate REAL,
    source TEXT DEFAULT 'BoC'
);

CREATE TABLE IF NOT EXISTS employment (
    year INTEGER PRIMARY KEY,
    employment_rate REAL,
    unemployment_rate REAL,
    source TEXT DEFAULT 'StatCan'
);

-- Optional merged view (by year)
CREATE VIEW IF NOT EXISTS merged_metrics AS
SELECT
    r.year,
    r.avg_rent,
    r.vacancy_rate,
    i.interest_rate,
    e.employment_rate,
    e.unemployment_rate
FROM rents r
LEFT JOIN interest_rates i USING (year)
LEFT JOIN employment e USING (year);

