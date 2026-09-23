# KickCore Analytics - Visualizations Page
import os
import streamlit as st
from utils import set_background, inject_css, sidebar_nav, BASE_DIR

# Page setup
st.set_page_config(page_title="Visualizations — KickCore", page_icon="📈", layout="wide")
set_background("assets/bg.png")
inject_css()
sidebar_nav()

st.markdown('<div class="section-title">Visualizations</div>', unsafe_allow_html=True)

st.markdown("---")

# Charts directory path
charts_dir = BASE_DIR / "charts"

# Matplotlib chart list
matplotlib_charts = [
    ("01_top_scorers.png", "Top 10 Scorers"),
    ("02_top_assisters.png", "Top 10 Assisters"),
    ("03_position_distribution.png", "Position Distribution"),
    ("04_goals_histogram.png", "Goals Histogram"),
    ("05_goals_vs_assists.png", "Goals vs Assists"),
    ("06_rank_vs_goals.png", "Rank vs Goals"),
    ("07_team_goals_assists.png", "Team Goals & Assists"),
    ("08_cumulative_goals.png", "Cumulative Goals"),
    ("09_goals_vs_xg.png", "Goals vs xG"),
    ("10_team_cards.png", "Team Cards"),
]

# Seaborn chart list
seaborn_charts = [
    ("11_player_correlation_heatmap.png", "Player Correlation Heatmap"),
    ("12_goals_by_position_boxplot.png", "Goals by Position"),
    ("13_speed_by_position_violin.png", "Speed by Position"),
    ("14_players_per_nationality.png", "Players per Nationality"),
    ("15_pair_plot.png", "Pair Plot"),
    ("16_goals_kde.png", "Goals KDE"),
    ("17_goals_xg_regression.png", "Goals vs xG Regression"),
    ("18_team_correlation_heatmap.png", "Team Correlation Heatmap"),
]

# Create main tabs
tab1, tab2 = st.tabs(["📊  Matplotlib Charts", "🎨  Seaborn Charts"])

# Display charts if they exist
def show_charts(charts):
    any_shown = False
    for fname, title in charts:
        path = charts_dir / fname
        if path.exists():
            any_shown = True
            st.markdown(f'<div class="chart-title">{title}</div>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1.5, 6, 1.5])
            with col2:
                st.image(str(path), use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)
        else:
            # Show warning if chart file is missing
            st.warning(f"⚠️ Chart not generated yet: **{title}** (`{fname}`)")

    if not any_shown:
        st.info(
            "No charts found. Run `visualization.py` to generate them:\n"
            "```\npython visualization.py\n```"
        )

# Matplotlib charts tab
with tab1:
    show_charts(matplotlib_charts)

# Seaborn charts tab
with tab2:
    show_charts(seaborn_charts)