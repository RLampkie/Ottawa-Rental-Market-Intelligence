# Ottawa Rental Market Intelligence

Analyze Ottawa's rental market and macroeconomic drivers to produce a concise dashboard with insights. Built with Python 3.11, SQLite, and Tableau.

## Goals
- Consolidate rental (CMHC) and macro data (Bank of Canada, Statistics Canada)
- Clean, standardize, and merge into a single analysis-ready dataset
- Explore relationships between average rent, interest rates, and employment
- Publish 3–4 visuals and a one-page Tableau dashboard

## Data Sources
- CMHC Rental Market Survey (Ottawa): https://www.cmhc-schl.gc.ca/en/professionals/housing-markets-data-and-research
- Bank of Canada – Interest Rates: https://www.bankofcanada.ca/rates/interest-rates/
- Statistics Canada – Employment: https://www.statcan.gc.ca/en/start

## Structure
```
data/        # CSVs (raw and merged_data.csv)
notebooks/   # Jupyter notebooks
visuals/     # PNG charts and dashboard screenshot
sql/         # SQLite schema and queries
scripts/     # Project notes / helper scripts
tableau/     # Tableau workbook (.twb/.twbx) and notes
docs/        # Additional documentation
```

## Quickstart
1) Python 3.11 virtual env
```
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: . .venv/Scripts/Activate.ps1
pip install -r requirements.txt
```
2) Place CSVs in `data/` using names below (see `data/README.md`).
3) Open Jupyter to work with notebooks
```
jupyter lab
```

## Timeline (4-Day Fast-Track)
- Day 1: Setup repo, gather data
- Day 2: Clean + merge; export `data/merged_data.csv`
- Day 3: Analysis + visuals; save PNGs in `visuals/`
- Day 4: Tableau dashboard + finalize README

## Next Step (Day 1)
Download CSVs to `data/` using the naming conventions in `data/README.md`.

