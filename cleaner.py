# KickCore Analytics - FIFA World Cup 2026
# Data cleaning using Pandas
import os
import pandas as pd
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
raw_player_dir = str(BASE_DIR / "data" / "raw" / "player_stats")
raw_team_dir = str(BASE_DIR / "data" / "raw" / "team_stats")
cleaned_player_dir = str(BASE_DIR / "data" / "cleaned" / "player_stats")
cleaned_team_dir = str(BASE_DIR / "data" / "cleaned" / "team_stats")

# File lists
player_files = [
    "player_golden_boot.csv", "player_attacking.csv",
    "player_distribution.csv", "player_defending.csv",
    "player_discipline.csv", "player_goalkeeping.csv",
    "player_movement.csv", "player_physical.csv",
]
team_files = [
    "team_attacking.csv", "team_distribution.csv",
    "team_defending.csv", "team_discipline.csv",
    "team_goalkeeping.csv", "team_movement.csv",
    "team_physical.csv",
]

# Identity columns to skip during type conversion
player_id_cols = ["Rank", "Name", "Nationality", "Position"]
team_id_cols = ["Rank", "Team"]

# Remove "x" suffix from xG Efficiency column and convert to float
def clean_xg_efficiency(df):
    for col in df.columns:
        if "efficiency" in col.lower():
            df[col] = (
                df[col].astype(str)
                .str.replace("x", "", regex=False)
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    return df

# Keywords for count/event columns that should fill missing with 0
ZERO_FILL_KEYWORDS = [
    "goal", "assist", "card", "save", "foul", "sprint", "corner",
    "attempt", "tackle", "interception", "clearance", "block",
    "turnover", "cross", "pass", "duel", "offside", "shot",
]

def _is_count_col(col_name):
    """Returns True if the column is a count/event stat (fill with 0).
    Returns False if it is a rate or physical measurement (fill with median)."""
    lower = col_name.lower()
    return any(kw in lower for kw in ZERO_FILL_KEYWORDS)

# Convert non-identity columns to numeric
# Counts fill with 0, measurements fill with median
def fix_dtypes(df, identity_cols):
    coercion_issues = []
    for col in df.columns:
        if col not in identity_cols and df[col].dtype == object:
            converted = pd.to_numeric(df[col], errors="coerce")
            n_bad = converted.isnull().sum()
            if n_bad > 0:
                coercion_issues.append(f"{col}: {n_bad} non-numeric value(s) replaced")
            if _is_count_col(col):
                df[col] = converted.fillna(0)
            else:
                median_val = converted.median()
                df[col] = converted.fillna(median_val)
    if coercion_issues:
        print(f"    Warning - Coercion issues found:")
        for msg in coercion_issues:
            print(f"      - {msg}")
    return df

# Load from raw, clean, and save to cleaned folder
def clean_file(raw_dir, cleaned_dir, fname, identity_cols):
    raw_path = os.path.join(raw_dir, fname)
    cleaned_path = os.path.join(cleaned_dir, fname)
    os.makedirs(cleaned_dir, exist_ok=True)
    df = pd.read_csv(raw_path)
    df = clean_xg_efficiency(df)
    df = fix_dtypes(df, identity_cols)
    df.to_csv(cleaned_path, index=False, encoding="utf-8-sig")
    nulls = df.isnull().sum().sum()
    status = "OK" if nulls == 0 else f"{nulls} nulls"
    print(f"  {fname:<35} {len(df):>5} rows  [{status}]")

def main():
    print("KickCore Analytics - Data Cleaning")
    print()
    print("Player Files:")
    for fname in player_files:
        clean_file(raw_player_dir, cleaned_player_dir, fname, player_id_cols)
    print("\nTeam Files:")
    for fname in team_files:
        clean_file(raw_team_dir, cleaned_team_dir, fname, team_id_cols)
    print("\nCleaning complete!")

if __name__ == "__main__":
    main()