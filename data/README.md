# Data Guide

Place the following CSVs in this folder. Recommended filenames:

- cmhc_rental_ottawa.csv
- boc_interest_rates.csv
- statcan_employment_ottawa.csv

Notes
- Prefer annual or quarterly aggregates with a `Year` or `Year`+`Quarter` column.
- Keep numeric columns clean (no `$`, `,`, or text). Use decimal `.`.
- Minimum columns suggested:
  - CMHC: `Year`, `Avg_Rent`, `Vacancy_Rate` (optional additional fields welcome)
  - BoC: `Year`, `Interest_Rate` (e.g., policy/overnight rate average by year)
  - StatCan: `Year`, `Employment_Rate` (and optional `Unemployment_Rate`)

Links
- CMHC Rental Market Survey (Ottawa): https://www.cmhc-schl.gc.ca/en/professionals/housing-markets-data-and-research
- Bank of Canada – Interest Rates: https://www.bankofcanada.ca/rates/interest-rates/
- Statistics Canada – Employment: https://www.statcan.gc.ca/en/start

Output
- Save the merged dataset as `merged_data.csv` in this folder (Day 2).

