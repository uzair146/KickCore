# KickCore Analytics - Download Page
import streamlit as st
import pandas as pd
from utils import set_background, inject_css, sidebar_nav

# Page setup
st.set_page_config(page_title="Download — KickCore", page_icon="💾", layout="wide")
set_background("assets/bg.png")
inject_css()
sidebar_nav()

st.markdown('<div class="section-title">Downloads</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div class="page-desc">Download any cleaned dataset as CSV file.</div>', unsafe_allow_html=True)
st.markdown("---")

# Player stats file list
player_files = [
    ("Golden Boot", "data/cleaned/player_stats/player_golden_boot.csv"),
    ("Attacking", "data/cleaned/player_stats/player_attacking.csv"),
    ("Distribution", "data/cleaned/player_stats/player_distribution.csv"),
    ("Defending", "data/cleaned/player_stats/player_defending.csv"),
    ("Discipline", "data/cleaned/player_stats/player_discipline.csv"),
    ("Goalkeeping", "data/cleaned/player_stats/player_goalkeeping.csv"),
    ("Movement", "data/cleaned/player_stats/player_movement.csv"),
    ("Physical", "data/cleaned/player_stats/player_physical.csv"),
]

# Team stats file list
team_files = [
    ("Team Attacking", "data/cleaned/team_stats/team_attacking.csv"),
    ("Team Distribution", "data/cleaned/team_stats/team_distribution.csv"),
    ("Team Defending", "data/cleaned/team_stats/team_defending.csv"),
    ("Team Discipline", "data/cleaned/team_stats/team_discipline.csv"),
    ("Team Goalkeeping", "data/cleaned/team_stats/team_goalkeeping.csv"),
    ("Team Movement", "data/cleaned/team_stats/team_movement.csv"),
    ("Team Physical", "data/cleaned/team_stats/team_physical.csv"),
]

# Render download buttons in a 2-column grid
def render_download_section(files: list, key_prefix: str):
    """Render download buttons in a 2-column grid — handles any number of files."""
    from pathlib import Path
    from utils import BASE_DIR
    for i in range(0, len(files), 2):
        c1, c2 = st.columns(2)
        for col, idx in [(c1, i), (c2, i + 1)]:
            if idx < len(files):
                name, rel_path = files[idx]
                full_path = BASE_DIR / rel_path
                if not full_path.exists():
                    col.warning(f"File not found: {rel_path}")
                    continue
                df = pd.read_csv(full_path)
                col.download_button(
                    label=f"⬇  Download {name}",
                    data=df.to_csv(index=False).encode("utf-8"),
                    file_name=f"kickcore_{name.lower().replace(' ', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key=f"{key_prefix}_{idx}",
                )

# Create main tabs
tab_player, tab_team = st.tabs(["⚽  Player Stats", "🌍  Team Stats"])
st.markdown("---")

# Player stats download tab
with tab_player:
    st.markdown('<div class="section-heading">Player Stats</div>', unsafe_allow_html=True)
    render_download_section(player_files, "player")

# Team stats download tab
with tab_team:
    st.markdown('<div class="section-heading">Team Stats</div>', unsafe_allow_html=True)
    render_download_section(team_files, "team")