import argparse
import sys
from pathlib import Path
import pandas as pd


def _require_cols(df: pd.DataFrame, required: list[str], label: str):
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing columns in {label}: {missing}. Found: {list(df.columns)}.\n"
            "Tip: Use CLI flags to set column names to match your CSVs."
        )


def clean_and_merge(
    cmhc_path: Path,
    boc_path: Path,
    statcan_path: Path,
    out_path: Path,
    cmhc_year_col: str = "Year",
    cmhc_rent_col: str = "Avg_Rent",
    cmhc_vacancy_col: str | None = "Vacancy_Rate",
    boc_year_col: str = "Year",
    boc_rate_col: str = "Interest_Rate",
    statcan_year_col: str = "Year",
    statcan_emp_col: str = "Employment_Rate",
    statcan_unemp_col: str | None = "Unemployment_Rate",
) -> pd.DataFrame:
    """Load source CSVs, standardize columns, merge by Year, and compute metrics."""

    # CMHC
    cmhc = pd.read_csv(cmhc_path)
    _require_cols(cmhc, [cmhc_year_col, cmhc_rent_col], "CMHC (rents)")
    cmhc_renamed = cmhc[[cmhc_year_col, cmhc_rent_col] + ([cmhc_vacancy_col] if cmhc_vacancy_col and cmhc_vacancy_col in cmhc.columns else [])].rename(
        columns={
            cmhc_year_col: "Year",
            cmhc_rent_col: "Avg_Rent",
            (cmhc_vacancy_col if cmhc_vacancy_col in cmhc.columns else "__x__"): "Vacancy_Rate",
        }
    )
    # Remove placeholder if vacancy not present
    if "__x__" in cmhc_renamed.columns:
        cmhc_renamed = cmhc_renamed.drop(columns=["__x__"])

    # BoC
    boc = pd.read_csv(boc_path)
    _require_cols(boc, [boc_year_col, boc_rate_col], "BoC (interest rates)")
    boc_renamed = boc[[boc_year_col, boc_rate_col]].rename(columns={boc_year_col: "Year", boc_rate_col: "Interest_Rate"})

    # StatCan
    stat = pd.read_csv(statcan_path)
    _require_cols(stat, [statcan_year_col, statcan_emp_col], "StatCan (employment)")
    pick = [statcan_year_col, statcan_emp_col]
    if statcan_unemp_col and statcan_unemp_col in stat.columns:
        pick.append(statcan_unemp_col)
    stat_renamed = stat[pick].rename(
        columns={
            statcan_year_col: "Year",
            statcan_emp_col: "Employment_Rate",
            (statcan_unemp_col if statcan_unemp_col in stat.columns else "__y__"): "Unemployment_Rate",
        }
    )
    if "__y__" in stat_renamed.columns:
        stat_renamed = stat_renamed.drop(columns=["__y__"])

    # Ensure types
    for df in (cmhc_renamed, boc_renamed, stat_renamed):
        if df["Year"].dtype.kind not in ("i", "u"):
            # Try parse to int from strings/dates
            df["Year"] = pd.to_datetime(df["Year"], errors="coerce").dt.year.fillna(pd.NA)
            df["Year"] = df["Year"].astype("Int64")
        # Coerce numeric columns
        for col in df.columns:
            if col == "Year":
                continue
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Merge
    merged = (
        cmhc_renamed.merge(boc_renamed, on="Year", how="left")
        .merge(stat_renamed, on="Year", how="left")
        .sort_values("Year")
        .reset_index(drop=True)
    )

    # Derived metrics
    merged["Rent_YoY_Pct"] = merged["Avg_Rent"].pct_change() * 100
    if "Employment_Rate" in merged.columns:
        merged["Employment_YoY_Pp"] = merged["Employment_Rate"].diff()
        merged["Employment_YoY_Pct"] = merged["Employment_Rate"].pct_change() * 100

    # Save
    out_path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(out_path, index=False)

    return merged


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Clean and merge Ottawa rental + macro data by year.")
    p.add_argument("--cmhc", dest="cmhc", type=Path, default=Path("data/cmhc_rental_ottawa.csv"))
    p.add_argument("--boc", dest="boc", type=Path, default=Path("data/boc_interest_rates.csv"))
    p.add_argument("--statcan", dest="statcan", type=Path, default=Path("data/statcan_employment_ottawa.csv"))
    p.add_argument("--out", dest="out", type=Path, default=Path("data/merged_data.csv"))

    # Column overrides
    p.add_argument("--cmhc-year-col", default="Year")
    p.add_argument("--cmhc-rent-col", default="Avg_Rent")
    p.add_argument("--cmhc-vacancy-col", default="Vacancy_Rate")

    p.add_argument("--boc-year-col", default="Year")
    p.add_argument("--boc-rate-col", default="Interest_Rate")

    p.add_argument("--statcan-year-col", default="Year")
    p.add_argument("--statcan-emp-col", default="Employment_Rate")
    p.add_argument("--statcan-unemp-col", default="Unemployment_Rate")
    return p


def main(argv: list[str] | None = None):
    args = build_arg_parser().parse_args(argv)

    merged = clean_and_merge(
        cmhc_path=args.cmhc,
        boc_path=args.boc,
        statcan_path=args.statcan,
        out_path=args.out,
        cmhc_year_col=args.cmhc_year_col,
        cmhc_rent_col=args.cmhc_rent_col,
        cmhc_vacancy_col=args.cmhc_vacancy_col,
        boc_year_col=args.boc_year_col,
        boc_rate_col=args.boc_rate_col,
        statcan_year_col=args.statcan_year_col,
        statcan_emp_col=args.statcan_emp_col,
        statcan_unemp_col=args.statcan_unemp_col,
    )

    print(f"Saved merged dataset: {args.out} ({len(merged)} rows)")
    print("Columns:", ", ".join(merged.columns))


if __name__ == "__main__":
    main()

