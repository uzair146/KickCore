# KickCore Analytics - FIFA World Cup 2026
# Statistical analysis using Pandas and NumPy
import os
import numpy as np
import pandas as pd
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
cleaned_player_dir = str(BASE_DIR / "data" / "cleaned" / "player_stats")
cleaned_team_dir = str(BASE_DIR / "data" / "cleaned" / "team_stats")
analysis_dir = str(BASE_DIR / "data" / "analysis")

# Load a single cleaned CSV file
def load(folder, fname):
    return pd.read_csv(os.path.join(folder, fname))

# Save a dataframe to analysis folder
def save(df, fname):
    os.makedirs(analysis_dir, exist_ok=True)
    fp = os.path.join(analysis_dir, fname)
    df.to_csv(fp, index=False, encoding="utf-8-sig")
    print(f"  Saved: {fname} ({len(df)} rows)")

# NumPy summary stats for numeric columns
def summary_stats(df, identity_cols):
    numeric_cols = [c for c in df.columns if c not in identity_cols]
    rows = []
    for col in numeric_cols:
        arr = pd.to_numeric(df[col], errors="coerce").dropna().values
        if len(arr) == 0:
            continue
        rows.append({
            "Stat": col,
            "Mean": round(np.mean(arr), 2),
            "Median": round(np.median(arr), 2),
            "Std": round(np.std(arr), 2),
            "Min": round(np.min(arr), 2),
            "Max": round(np.max(arr), 2),
            "25th Percentile": round(np.percentile(arr, 25), 2),
            "75th Percentile": round(np.percentile(arr, 75), 2),
            "90th Percentile": round(np.percentile(arr, 90), 2),
        })
    return pd.DataFrame(rows)

# Get top N players by a column
def top_players(df, col, n=20):
    base_cols = [c for c in ["Rank", "Name", "Nationality", "Position"] if c in df.columns]
    cols = base_cols + [col]
    return df[cols].sort_values(col, ascending=False).head(n).reset_index(drop=True)

# Get top N teams by a column
def top_teams(df, col, n=10):
    base_cols = [c for c in ["Rank", "Team"] if c in df.columns]
    cols = base_cols + [col]
    return df[cols].sort_values(col, ascending=False).head(n).reset_index(drop=True)

def main():
    print("KickCore Analytics - Statistical Analysis")
    print()

    # Load cleaned player files
    golden_boot = load(cleaned_player_dir, "player_golden_boot.csv")
    attacking = load(cleaned_player_dir, "player_attacking.csv")
    discipline = load(cleaned_player_dir, "player_discipline.csv")
    goalkeeping = load(cleaned_player_dir, "player_goalkeeping.csv")
    physical = load(cleaned_player_dir, "player_physical.csv")

    # Load cleaned team files
    team_attacking = load(cleaned_team_dir, "team_attacking.csv")
    team_defending = load(cleaned_team_dir, "team_defending.csv")
    team_discipline = load(cleaned_team_dir, "team_discipline.csv")

    print("Player Analysis:")
    # Top scorers
    save(top_players(golden_boot, "Goals"), "top_scorers.csv")
    # Top assisters
    save(top_players(golden_boot, "Assists"), "top_assisters.csv")
    # Top yellow cards
    save(top_players(discipline, "Yellow Cards"), "top_yellow_cards.csv")
    # Top red cards
    save(top_players(discipline, "Red Cards"), "top_red_cards.csv")
    # Top saves
    save(top_players(goalkeeping, "Goalkeeper Saves"), "top_saves.csv")
    # Top speed
    save(top_players(physical, "Top Speed (km/h)"), "top_speed.csv")
    # Top distance
    save(top_players(physical, "Total Distance (m)"), "top_distance.csv")
    # Top sprints
    save(top_players(physical, "Sprints"), "top_sprints.csv")
    # Player stats summary (NumPy)
    save(summary_stats(golden_boot, ["Rank", "Name", "Nationality", "Position"]), "player_stats_summary.csv")

    print("\nTeam Analysis:")
    # Top teams by goals
    df_teams_goals = team_attacking.nlargest(10, "Goals")[["Rank", "Team", "Goals", "Assists"]].reset_index(drop=True)
    save(df_teams_goals, "top_teams_goals.csv")
    # Top teams by assists
    save(top_teams(team_attacking, "Assists"), "top_assists_teams.csv")
    # Top teams defense (forced turnovers)
    save(top_teams(team_defending, "Forced Turnovers"), "top_teams_defense.csv")
    # Top teams discipline (least fouls)
    df_disc = team_discipline.sort_values("Fouls For", ascending=True).head(10).reset_index(drop=True)
    save(df_disc[["Rank", "Team", "Yellow Cards", "Red Cards", "Fouls For", "Fouls Against"]], "top_teams_discipline.csv")
    # Team stats summary (NumPy)
    save(summary_stats(team_attacking, ["Rank", "Team"]), "team_stats_summary.csv")

    print("\nGroupby Analysis:")
    # Nationality summary
    nat = golden_boot.groupby("Nationality").agg(
        Players=("Name", "count"),
        Total_Goals=("Goals", "sum"),
        Avg_Goals=("Goals", "mean"),
        Total_Assists=("Assists", "sum"),
        Avg_Assists=("Assists", "mean"),
    ).reset_index()
    nat["Avg_Goals"] = nat["Avg_Goals"].round(2)
    nat["Avg_Assists"] = nat["Avg_Assists"].round(2)
    nat = nat.sort_values("Total_Goals", ascending=False).reset_index(drop=True)
    save(nat, "nationality_summary.csv")

    # Position summary
    pos = golden_boot.groupby("Position").agg(
        Players=("Name", "count"),
        Total_Goals=("Goals", "sum"),
        Avg_Goals=("Goals", "mean"),
        Total_Assists=("Assists", "sum"),
        Avg_Assists=("Assists", "mean"),
        Max_Goals=("Goals", "max"),
    ).reset_index()
    pos["Avg_Goals"] = pos["Avg_Goals"].round(2)
    pos["Avg_Assists"] = pos["Avg_Assists"].round(2)
    pos = pos.sort_values("Total_Goals", ascending=False).reset_index(drop=True)
    save(pos, "position_summary.csv")

    print("\nAnalysis complete!")
    print(f"  All files saved to: {analysis_dir}/")

if __name__ == "__main__":
    main()