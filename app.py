# KickCore Analytics - FIFA World Cup 2026 — Home Page

import streamlit as st
import pandas as pd
from utils import (
    set_background, inject_css, sidebar_nav,
    load_players, load_teams, format_scorer_name
)

# Page setup
st.set_page_config(
    page_title="KickCore Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

set_background("assets/bg.png")
inject_css()
sidebar_nav()

# Hero banner
st.markdown("""
<div style="text-align:center;padding:1rem 0 0.5rem">
    <div style="font-size:3rem;font-weight:800;color:#e8c84a;
        letter-spacing:2px;text-shadow:0 2px 20px rgba(232,200,74,0.4);
        background:#060e1f;display:inline-block;padding:10px 36px;
        border-radius:14px;border:1px solid rgba(232,200,74,0.35)">
        KickCore Analytics
    </div>
    <br><br>
    <div style="font-size:1.15rem;color:#a8c8e8;font-style:italic;
        background:#060e1f;display:inline-block;padding:6px 22px;
        border-radius:8px;border:1px solid rgba(168,200,232,0.2)">
        FIFA World Cup 2026 — Player &amp; Team Statistics
    </div>
    <div style="margin-top:14px">
        <span style="background:#060e1f;border:1px solid #e8c84a;
            color:#e8c84a;padding:7px 22px;border-radius:50px;
            font-size:0.9rem;font-weight:600;letter-spacing:1px">
            CANADA · MEXICO · USA 2026
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Load and compute home page stats
@st.cache_data(show_spinner=False)
def get_home_stats():
    pdata = load_players()
    tdata = load_teams()

    gb = pdata["golden_boot"]
    disc = pdata["discipline"]
    team = tdata["attacking"]
    gk = pdata["goalkeeping"]

    # Count unique players across all player stat files
    all_names = set()
    for df in pdata.values():
        if "Name" in df.columns:
            all_names.update(df["Name"].dropna().tolist())

    total_players = len(all_names)
    total_teams = len(team)
    total_goals = int(gb["Goals"].sum())
    total_assists = int(gb["Assists"].sum())

    # Top scorer — safe against empty dataframe
    if gb.empty or gb["Goals"].max() == 0:
        top_scorer = "N/A"
        top_goals = 0
    else:
        top_scorer = gb.loc[gb["Goals"].idxmax(), "Name"]
        top_goals = int(gb["Goals"].max())

    total_yc = int(disc["Yellow Cards"].sum())
    total_rc = int(disc["Red Cards"].sum())

    # Top scoring team
    top_team_row = team.sort_values(["Goals", "Assists"], ascending=False).iloc[0]
    top_team_name = top_team_row["Team"]

    # Top goalkeeper
    if gk.empty or gk["Goalkeeper Saves"].max() == 0:
        top_gk_name = "N/A"
        top_gk_saves = 0
    else:
        top_gk_row = gk.loc[gk["Goalkeeper Saves"].idxmax()]
        top_gk_name = top_gk_row["Name"]
        top_gk_saves = int(top_gk_row["Goalkeeper Saves"])

    return (total_players, total_teams, total_goals, total_assists,
            top_scorer, top_goals, total_yc, total_rc,
            top_team_name, top_gk_name, top_gk_saves, gb)

(total_players, total_teams, total_goals, total_assists,
 top_scorer, top_goals, total_yc, total_rc,
 top_team_name, top_gk_name, top_gk_saves, gb) = get_home_stats()

# Format display names
top_scorer_display = format_scorer_name(top_scorer)
top_gk_display = format_scorer_name(top_gk_name)

# Metrics row 1
st.markdown('<div class="section-title">Tournament at a Glance</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<div class="metric-card"><div class="metric-value">{total_players:,}</div><div class="metric-label">Total Players</div></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="metric-card"><div class="metric-value">{total_teams}</div><div class="metric-label">Nations</div></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="metric-card"><div class="metric-value">{total_goals}</div><div class="metric-label">Total Goals</div></div>', unsafe_allow_html=True)
c4.markdown(f'<div class="metric-card"><div class="metric-value">{total_assists}</div><div class="metric-label">Total Assists</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Metrics row 2
c5, c6, c7, c8 = st.columns(4)
c5.markdown(f'<div class="metric-card"><div class="metric-value" style="font-size:1.3rem">{top_scorer_display}</div><div class="metric-label">Golden Boot Leader</div></div>', unsafe_allow_html=True)
c6.markdown(f'<div class="metric-card"><div class="metric-value" style="font-size:1.3rem">{top_team_name}</div><div class="metric-label">Top Scoring Team</div></div>', unsafe_allow_html=True)
c7.markdown(f'<div class="metric-card"><div class="metric-value" style="font-size:1.4rem">{total_yc} / {total_rc}</div><div class="metric-label">Yellow / Red Cards</div></div>', unsafe_allow_html=True)
c8.markdown(f'<div class="metric-card"><div class="metric-value" style="font-size:1.25rem">{top_gk_display}</div><div class="metric-label">Top GK ({top_gk_saves} Saves)</div></div>', unsafe_allow_html=True)

st.markdown("---")

# Top 5 scorers table
st.markdown('<div class="section-title">Top 5 Scorers</div>', unsafe_allow_html=True)
top5 = gb.nlargest(5, "Goals")[["Rank", "Name", "Nationality", "Position", "Goals", "Assists", "Minutes Played"]].reset_index(drop=True)
st.dataframe(top5, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown('<div style="text-align:center;color:#a8c8e8;font-size:0.95rem;padding:6px 24px;background:#060e1f;border-radius:8px;display:inline-block;width:fit-content;margin:0 auto;position:relative;left:50%;transform:translateX(-50%)">KickCore Analytics &nbsp;|&nbsp; FIFA World Cup 2026</div>', unsafe_allow_html=True)