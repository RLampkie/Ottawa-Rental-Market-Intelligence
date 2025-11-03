import argparse
import sqlite3
from pathlib import Path
import pandas as pd


def load_schema(conn: sqlite3.Connection, schema_path: Path):
    if schema_path and schema_path.exists():
        sql = schema_path.read_text(encoding="utf-8")
        conn.executescript(sql)


def main():
    parser = argparse.ArgumentParser(description="Load merged_data.csv into SQLite and (optionally) apply schema.sql")
    parser.add_argument("--db", type=Path, default=Path("data/ottawa_rental.sqlite"))
    parser.add_argument("--csv", type=Path, default=Path("data/merged_data.csv"))
    parser.add_argument("--schema", type=Path, default=Path("sql/schema.sql"))
    args = parser.parse_args()

    args.db.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.csv)

    with sqlite3.connect(args.db) as conn:
        load_schema(conn, args.schema)
        df.to_sql("merged_data", conn, if_exists="replace", index=False)
        cur = conn.execute("SELECT COUNT(*) FROM merged_data")
        n = cur.fetchone()[0]
        print(f"Loaded merged_data into {args.db} with {n} rows.")


if __name__ == "__main__":
    main()

