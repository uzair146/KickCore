# KickCore Analytics - FIFA World Cup 2026
# Data visualization using Matplotlib and Seaborn
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
cleaned_player_dir = str(BASE_DIR / "data" / "cleaned" / "player_stats")
cleaned_team_dir = str(BASE_DIR / "data" / "cleaned" / "team_stats")
analysis_dir = str(BASE_DIR / "data" / "analysis")
charts_dir = str(BASE_DIR / "charts")

# Theme and font setup
sns.set_theme(style="whitegrid")
plt.rcParams.update({"font.family": "DejaVu Sans"})

# Colour palette used across all charts
C_GOLD = "#e8c84a"
C_NAVY = "#1a3a5c"
C_RED = "#e84a5f"
C_GREEN = "#2ecc71"
C_ORANGE = "#f39c12"
POS_PALETTE = {"FW": C_NAVY, "MF": C_RED, "DF": C_GOLD, "GK": C_GREEN}

# Load a CSV file
def load(folder, fname):
    return pd.read_csv(os.path.join(folder, fname))

# Save chart to charts folder
def save_chart(fname):
    os.makedirs(charts_dir, exist_ok=True)
    plt.savefig(os.path.join(charts_dir, fname), dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {fname}")

# Vertical bar chart for top 10 scorers
def chart_top_scorers():
    df = load(analysis_dir, "top_scorers.csv")
    df = df.sort_values("Goals", ascending=False).head(10).copy()
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = [C_GOLD if i == 0 else C_NAVY for i in range(len(df))]
    ax.bar(df["Name"], df["Goals"], color=colors, edgecolor="white", linewidth=0.8, width=0.6)
    labels = []
    for name in df["Name"]:
        parts = name.split()
        if len(parts) >= 2:
            labels.append(f"{parts[0]}\n{parts[-1]}")
        else:
            labels.append(name)
    ax.set_xticklabels(labels, fontsize=9, ha='center')
    ax.set_title("Top 10 Scorers (FIFA World Cup 2026)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Player", fontsize=11)
    ax.set_ylabel("Goals", fontsize=11)
    plt.xticks(rotation=0)
    plt.tight_layout()
    save_chart("01_top_scorers.png")

# Horizontal bar chart for top 10 assisters
def chart_top_assisters():
    df = load(analysis_dir, "top_assisters.csv")
    df = df.sort_values("Assists", ascending=False).head(10).copy()
    df = df.sort_values("Assists", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = [C_GOLD if i == len(df) - 1 else C_RED for i in range(len(df))]
    ax.barh(df["Name"], df["Assists"], color=colors, edgecolor="white", linewidth=0.8, height=0.6)
    ax.set_title("Top 10 Assisters (FIFA World Cup 2026)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Assists", fontsize=11)
    ax.set_ylabel("Player", fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.xaxis.grid(True, linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)
    plt.tight_layout()
    save_chart("02_top_assisters.png")

# Pie chart for position distribution
def chart_position_distribution():
    df = load(analysis_dir, "position_summary.csv")
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        df["Players"], labels=df["Position"],
        autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100 * df["Players"].sum())})',
        colors=[C_GOLD, C_NAVY, C_RED, C_GREEN],
        startangle=140, textprops={"fontsize": 12, "fontweight": "bold"},
        wedgeprops={"edgecolor": "white", "linewidth": 2}, pctdistance=0.7)
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontsize(10)
        autotext.set_fontweight("bold")
    ax.set_title("Player Distribution by Position", fontsize=14, fontweight="bold", pad=20)
    plt.tight_layout()
    save_chart("03_position_distribution.png")

# Histogram for goals distribution
def chart_goals_histogram():
    df = load(cleaned_player_dir, "player_golden_boot.csv")
    df = df[df["Goals"] > 0]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df["Goals"], bins=range(1, int(df["Goals"].max()) + 2), color=C_NAVY, edgecolor="white", linewidth=0.8, align="left")
    ax.axvline(df["Goals"].mean(), color=C_RED, linestyle="--", linewidth=2, label=f"Mean: {df['Goals'].mean():.1f}")
    ax.axvline(df["Goals"].median(), color=C_GOLD, linestyle="--", linewidth=2, label=f"Median: {df['Goals'].median():.0f}")
    ax.set_title("Goals Distribution (Players with at Least 1 Goal)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Goals", fontsize=11)
    ax.set_ylabel("Number of Players", fontsize=11)
    ax.set_xticks(range(1, int(df["Goals"].max()) + 1))
    ax.legend(fontsize=11)
    plt.tight_layout()
    save_chart("04_goals_histogram.png")

# Scatter plot for goals vs assists by position
def chart_goals_vs_assists():
    df = load(cleaned_player_dir, "player_golden_boot.csv")
    df = df[(df["Goals"] > 0) | (df["Assists"] > 0)]
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.scatter(df[df["Position"] == "FW"]["Goals"], df[df["Position"] == "FW"]["Assists"], label="FW", color=C_NAVY, alpha=0.75, s=70, edgecolors="white", linewidth=0.5)
    ax.scatter(df[df["Position"] == "MF"]["Goals"], df[df["Position"] == "MF"]["Assists"], label="MF", color=C_RED, alpha=0.75, s=70, edgecolors="white", linewidth=0.5)
    ax.scatter(df[df["Position"] == "DF"]["Goals"], df[df["Position"] == "DF"]["Assists"], label="DF", color=C_ORANGE, alpha=0.75, s=70, edgecolors="white", linewidth=0.5)
    ax.scatter(df[df["Position"] == "GK"]["Goals"], df[df["Position"] == "GK"]["Assists"], label="GK", color=C_GREEN, alpha=0.75, s=70, edgecolors="white", linewidth=0.5)
    for _, row in df.nlargest(5, "Goals").iterrows():
        ax.annotate(row["Name"].split()[-1], (row["Goals"], row["Assists"]), xytext=(0, 10), textcoords="offset points", ha='center', fontsize=9, fontweight="bold")
    ax.set_title("Goals vs Assists by Position", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Goals", fontsize=11)
    ax.set_ylabel("Assists", fontsize=11)
    ax.legend(title="Position", fontsize=10)
    plt.tight_layout()
    save_chart("05_goals_vs_assists.png")

# Line plot for rank vs goals (top 20)
def chart_rank_vs_goals():
    df = load(analysis_dir, "top_scorers.csv").head(20).reset_index(drop=True)
    df["Rank_Num"] = df.index + 1
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(df["Rank_Num"], df["Goals"], color=C_NAVY, linewidth=2.5, marker="o", markersize=6, markerfacecolor=C_GOLD, markeredgecolor=C_NAVY)
    for _, row in df.iterrows():
        ax.annotate(row["Name"].split()[-1], (row["Rank_Num"], row["Goals"]),
                    textcoords="offset points", xytext=(4.5, 8),
                    fontsize=8.5, ha='left', va='center')
    ax.set_title("Goals by Rank (Top 20 Scorers)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Rank", fontsize=11)
    ax.set_ylabel("Goals", fontsize=11)
    ax.set_xticks(df["Rank_Num"])
    ax.set_xlim(0.5, 21.5)
    plt.tight_layout()
    save_chart("06_rank_vs_goals.png")

# Stacked bar for team goals + assists
def chart_team_goals_assists():
    df = load(analysis_dir, "top_teams_goals.csv").head(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(df))
    ax.bar(x, df["Goals"], label="Goals", color=C_NAVY, edgecolor="white", linewidth=0.8)
    ax.bar(x, df["Assists"], bottom=df["Goals"], label="Assists", color=C_RED, edgecolor="white", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(df["Team"], rotation=0, ha="center", fontsize=9)
    ax.set_title("Top 10 Teams (Goals + Assists)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Teams", fontsize=11)
    ax.set_ylabel("Count", fontsize=11)
    ax.legend(fontsize=11)
    plt.tight_layout()
    save_chart("07_team_goals_assists.png")

# Area chart for cumulative goals
def chart_cumulative_goals():
    df = load(analysis_dir, "top_scorers.csv").head(20).reset_index(drop=True)
    df["Cumulative"] = df["Goals"].cumsum()
    df["Short"] = df["Name"].apply(lambda x: x.split()[-1])
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.fill_between(range(1, len(df)+1), df["Cumulative"], alpha=0.3, color=C_NAVY)
    ax.plot(range(1, len(df)+1), df["Cumulative"], color=C_NAVY, linewidth=2.5, marker="o", markersize=7, markerfacecolor=C_GOLD, markeredgecolor=C_NAVY)
    for i, row in df.iterrows():
        ax.axvline(x=i+1, ymin=0, ymax=row["Cumulative"]/max(df["Cumulative"]), color=C_NAVY, linestyle="--", linewidth=0.5, alpha=0.3)
        ax.text(i+1, -2, row["Short"],
                rotation=0, ha='center', va='top', fontsize=7)
    ax.set_ylim(-4, max(df["Cumulative"]) * 1.1)
    ax.set_title("Cumulative Goals (Top 20 Scorers)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Player Rank", fontsize=11)
    ax.set_ylabel("Cumulative Goals", fontsize=11)
    ax.set_xticks(range(1, len(df)+1))
    ax.set_xticklabels([])
    plt.tight_layout()
    save_chart("08_cumulative_goals.png")

# Bubble chart for goals vs xG
def chart_goals_vs_xg():
    gb = load(cleaned_player_dir, "player_golden_boot.csv")
    att = load(cleaned_player_dir, "player_attacking.csv")[["Name", "Nationality", "xG"]]
    df = pd.merge(gb, att, on=["Name", "Nationality"], how="inner")
    df = df[df["Goals"] > 0].nlargest(30, "Goals")
    fig, ax = plt.subplots(figsize=(11, 7))
    scatter = ax.scatter(df["xG"], df["Goals"], s=df["Minutes Played"] / 5, c=df["Goals"], cmap="Blues", alpha=0.75, edgecolors=C_NAVY, linewidth=0.8)
    max_val = max(df["xG"].max(), df["Goals"].max()) + 1
    ax.plot([0, max_val], [0, max_val], "--", color=C_RED, linewidth=1.5, label="Goals = xG")
    for _, row in df[df["Goals"] >= 5].iterrows():
        ax.annotate(row["Name"].split()[-1], (row["xG"], row["Goals"]), textcoords="offset points", xytext=(0, 8), fontsize=8, ha='center', fontweight="bold")
    plt.colorbar(scatter, ax=ax, label="Goals")
    ax.set_title("Goals vs xG (Bubble Size = Minutes Played)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Expected Goals (xG)", fontsize=11)
    ax.set_ylabel("Actual Goals", fontsize=11)
    ax.legend(fontsize=10)
    plt.tight_layout()
    save_chart("09_goals_vs_xg.png")

# Double bar chart for yellow vs red cards
def chart_team_cards():
    df = load(cleaned_team_dir, "team_discipline.csv").nlargest(10, "Yellow Cards")
    x = np.arange(len(df))
    width = 0.35
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width/2, df["Yellow Cards"], width, label="Yellow Cards", color=C_GOLD, edgecolor="white")
    ax.bar(x + width/2, df["Red Cards"], width, label="Red Cards", color=C_RED, edgecolor="white")
    ax.set_xticks(x)
    ax.set_xticklabels(df["Team"], rotation=0, ha="center", fontsize=9)
    ax.set_title("Yellow vs Red Cards — Top 10 Teams", fontsize=14, fontweight="bold", pad=15)
    ax.set_ylabel("Cards", fontsize=11)
    ax.legend(fontsize=11)
    plt.tight_layout()
    save_chart("10_team_cards.png")

# Heatmap for player stats correlation
def chart_player_correlation():
    df = load(cleaned_player_dir, "player_golden_boot.csv")
    corr = df[["Goals", "Assists", "Minutes Played"]].corr()
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", linewidths=1, ax=ax, annot_kws={"size": 13}, vmin=-1, vmax=1)
    ax.set_title("Player Stats Correlation", fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    save_chart("11_player_correlation_heatmap.png")

# Box plot for goals by position
def chart_goals_by_position():
    df = load(cleaned_player_dir, "player_golden_boot.csv")
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.boxplot(data=df, x="Position", y="Goals", hue="Position", palette=POS_PALETTE,
                order=["FW", "MF", "DF", "GK"], ax=ax, linewidth=1.5, legend=False)
    ax.set_title("Goals Distribution by Position", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Position", fontsize=11)
    ax.set_ylabel("Goals", fontsize=11)
    plt.tight_layout()
    save_chart("12_goals_by_position_boxplot.png")

# Violin plot for speed by position
def chart_speed_by_position():
    df = load(cleaned_player_dir, "player_physical.csv")
    df = df[df["Top Speed (km/h)"] > 0]
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.violinplot(data=df, x="Position", y="Top Speed (km/h)", hue="Position", palette=POS_PALETTE,
                   order=["FW", "MF", "DF", "GK"], ax=ax, linewidth=1.2, legend=False)
    ax.set_title("Top Speed Distribution by Position", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Position", fontsize=11)
    ax.set_ylabel("Top Speed (km/h)", fontsize=11)
    plt.tight_layout()
    save_chart("13_speed_by_position_violin.png")

# Bar plot for players per nationality
def chart_players_per_nationality():
    df = load(analysis_dir, "nationality_summary.csv").head(15)
    fig, ax = plt.subplots(figsize=(13, 6))
    colors = [C_GOLD if v == df["Players"].max() else C_NAVY for v in df["Players"]]
    bars = ax.bar(df["Nationality"], df["Players"], color=colors, edgecolor="white", linewidth=0.8)
    for bar, val in zip(bars, df["Players"]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, str(int(val)), ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_title("Players per Nationality (Top 15 Nations)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Nationality", fontsize=11)
    ax.set_ylabel("Number of Players", fontsize=11)
    plt.tight_layout()
    save_chart("14_players_per_nationality.png")

# Pair plot for goals, assists, minutes by position
def chart_pair_plot():
    df = load(cleaned_player_dir, "player_golden_boot.csv")
    df_pair = df[["Goals", "Assists", "Minutes Played", "Position"]].copy()
    g = sns.pairplot(df_pair, hue="Position", palette=POS_PALETTE,
                     plot_kws={"alpha": 0.5, "s": 25}, diag_kind="kde")
    g.fig.suptitle("Pair Plot (Goals, Assists, Minutes)", y=1.02, fontsize=14, fontweight="bold")
    os.makedirs(charts_dir, exist_ok=True)
    g.fig.savefig(os.path.join(charts_dir, "15_pair_plot.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  Saved: 15_pair_plot.png")

# KDE plot for goals density by position
def chart_goals_kde():
    df = load(cleaned_player_dir, "player_golden_boot.csv")
    df = df[df["Goals"] > 0]
    fig, ax = plt.subplots(figsize=(10, 6))
    for pos, col in {"FW": C_NAVY, "MF": C_RED, "DF": C_GOLD}.items():
        subset = df[df["Position"] == pos]["Goals"]
        if len(subset) > 0:
            sns.kdeplot(subset, ax=ax, label=pos, linewidth=2.5, fill=True, alpha=0.2, color=col)
    ax.set_title("Goals Density by Position (Players with at Least 1 Goal)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Goals", fontsize=11)
    ax.set_ylabel("Density", fontsize=11)
    ax.legend(title="Position", fontsize=10)
    plt.tight_layout()
    save_chart("16_goals_kde.png")

# Regression plot for goals vs xG
def chart_goals_regression():
    gb = load(cleaned_player_dir, "player_golden_boot.csv")
    att = load(cleaned_player_dir, "player_attacking.csv")[["Name", "Nationality", "xG"]]
    df = pd.merge(gb, att, on=["Name", "Nationality"], how="inner")
    df = df[df["xG"] > 0]
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.regplot(data=df, x="xG", y="Goals", ax=ax, scatter_kws={"alpha": 0.5, "color": C_NAVY, "s": 50, "edgecolors": "white"},
                line_kws={"color": C_RED, "linewidth": 2.5})
    for _, row in df.nlargest(5, "Goals").iterrows():
        ax.annotate(row["Name"].split()[-1], (row["xG"], row["Goals"]), textcoords="offset points", xytext=(0, 10), fontsize=9, ha='center', fontweight='bold')
    ax.set_title("Goals vs xG with Regression Line", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Expected Goals (xG)", fontsize=11)
    ax.set_ylabel("Actual Goals", fontsize=11)
    plt.tight_layout()
    save_chart("17_goals_xg_regression.png")

# Heatmap for team stats correlation
def chart_team_correlation():
    df = load(cleaned_team_dir, "team_attacking.csv")
    cols = ["Goals", "Assists", "Attempts At Goal", "Attempts On Target", "xG", "Possession Control (%)"]
    corr = df[cols].corr()
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="YlOrRd", linewidths=0.8, ax=ax, annot_kws={"size": 10}, vmin=-1, vmax=1)
    ax.set_title("Team Stats Correlation", fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    save_chart("18_team_correlation_heatmap.png")

def main():
    print("KickCore Analytics - Visualization")
    print()
    os.makedirs(charts_dir, exist_ok=True)
    print("Matplotlib Charts:")
    chart_top_scorers()
    chart_top_assisters()
    chart_position_distribution()
    chart_goals_histogram()
    chart_goals_vs_assists()
    chart_rank_vs_goals()
    chart_team_goals_assists()
    chart_cumulative_goals()
    chart_goals_vs_xg()
    chart_team_cards()
    print("\nSeaborn Charts:")
    chart_player_correlation()
    chart_goals_by_position()
    chart_speed_by_position()
    chart_players_per_nationality()
    chart_pair_plot()
    chart_goals_kde()
    chart_goals_regression()
    chart_team_correlation()
    print(f"\nVisualization complete! 18 charts saved to: {charts_dir}/")

if __name__ == "__main__":
    main()