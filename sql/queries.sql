-- Example analysis queries for SQLite

-- Year-over-year rent change
WITH rents_yoy AS (
  SELECT
    year,
    avg_rent,
    LAG(avg_rent) OVER (ORDER BY year) AS prev_avg_rent
  FROM rents
)
SELECT
  year,
  avg_rent,
  ROUND((avg_rent - prev_avg_rent) / prev_avg_rent * 100.0, 2) AS yoy_rent_change_pct
FROM rents_yoy;

-- Join rents with interest rates and employment
SELECT
  m.year,
  m.avg_rent,
  m.vacancy_rate,
  m.interest_rate,
  m.employment_rate,
  m.unemployment_rate
FROM merged_metrics m
ORDER BY m.year;

