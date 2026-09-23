# KickCore Analytics - Statistics Page

import streamlit as st
import pandas as pd
from utils import set_background, inject_css, sidebar_nav, load_teams, BASE_DIR, _csv

# Page setup
st.set_page_config(page_title="Statistics — KickCore", page_icon="📊", layout="wide")
set_background("assets/bg.png")
inject_css()
sidebar_nav()

st.markdown('<div class="section-title">Statistics Dashboard</div>', unsafe_allow_html=True)

# Load all analysis CSVs with caching
@st.cache_data(show_spinner=False)
def load_analysis():
    base = "data/analysis"
    return {
        "top_scorers": _csv(f"{base}/top_scorers.csv"),
        "top_assisters": _csv(f"{base}/top_assisters.csv"),
        "top_saves": _csv(f"{base}/top_saves.csv"),
        "top_speed": _csv(f"{base}/top_speed.csv"),
        "top_distance": _csv(f"{base}/top_distance.csv"),
        "top_sprints": _csv(f"{base}/top_sprints.csv"),
        "top_yellow_cards": _csv(f"{base}/top_yellow_cards.csv"),
        "top_red_cards": _csv(f"{base}/top_red_cards.csv"),
        "position_summary": _csv(f"{base}/position_summary.csv"),
        "nationality_summary": _csv(f"{base}/nationality_summary.csv"),
        "player_stats_summary": _csv(f"{base}/player_stats_summary.csv"),
    }

data = load_analysis()
tdata = load_teams()

# Create main tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Top Performers", "Physical", "Discipline", "Position Analysis", "NumPy Summary", "🌍 Team Leaderboards"
])

# Top performers tab
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Top 10 Scorers**")
        st.dataframe(data["top_scorers"].head(10), use_container_width=True, hide_index=True)
    with c2:
        st.markdown("**Top 10 Assisters**")
        st.dataframe(data["top_assisters"].head(10), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("**Top 10 Goalkeepers — Saves**")
    st.dataframe(data["top_saves"].head(10), use_container_width=True, hide_index=True)

# Physical stats tab
with tab2:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Top Speed (km/h)**")
        st.dataframe(data["top_speed"].head(10), use_container_width=True, hide_index=True)
    with c2:
        st.markdown("**Most Distance Covered**")
        st.dataframe(data["top_distance"].head(10), use_container_width=True, hide_index=True)
    with c3:
        st.markdown("**Most Sprints**")
        st.dataframe(data["top_sprints"].head(10), use_container_width=True, hide_index=True)

# Discipline tab
with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Most Yellow Cards**")
        st.dataframe(data["top_yellow_cards"].head(10), use_container_width=True, hide_index=True)
    with c2:
        st.markdown("**Most Red Cards**")
        st.dataframe(data["top_red_cards"].head(10), use_container_width=True, hide_index=True)

# Position and nationality analysis tab
with tab4:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Goals by Position**")
        st.dataframe(data["position_summary"], use_container_width=True, hide_index=True)
    with c2:
        st.markdown("**Top Nationalities**")
        st.dataframe(data["nationality_summary"].head(15), use_container_width=True, hide_index=True)

# NumPy statistical summary tab
with tab5:
    st.markdown("**Player Stats — NumPy Statistical Summary**")
    st.dataframe(data["player_stats_summary"], use_container_width=True, hide_index=True)

# Team leaderboards tab
with tab6:
    st.markdown("### 🌍 Team Leaderboards")
    st.caption("Live rankings from cleaned team data — all 48 nations, 7 categories.")
    st.markdown("---")

    # Attacking leaderboards
    st.markdown("#### ⚽ Attacking")
    atk = tdata["attacking"].sort_values("Goals", ascending=False)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Top 10 — Goals**")
        st.dataframe(atk[["Team", "Goals", "Assists", "xG"]].head(10),
                     use_container_width=True, hide_index=True)
    with c2:
        st.markdown("**Top 10 — Attempts On Target**")
        st.dataframe(
            atk[["Team", "Attempts On Target", "Attempts At Goal", "Attempts At Goal Conv.Rate (%)"]]\
               .sort_values("Attempts On Target", ascending=False).head(10),
            use_container_width=True, hide_index=True)
    with c3:
        st.markdown("**Top 10 — Possession Control (%)**")
        st.dataframe(
            atk[["Team", "Possession Control (%)", "Corners"]]\
               .sort_values("Possession Control (%)", ascending=False).head(10),
            use_container_width=True, hide_index=True)

    st.markdown("---")

    # Defending and goalkeeping leaderboards
    st.markdown("#### 🛡️ Defending & Goalkeeping")
    defend = tdata["defending"].sort_values("Goals Conceded", ascending=True)
    gk = tdata["goalkeeping"].sort_values("Clean Sheets", ascending=False)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Best Defence — Fewest Goals Conceded**")
        st.dataframe(defend[["Team", "Goals Conceded", "Forced Turnovers"]].head(10),
                     use_container_width=True, hide_index=True)
    with c2:
        st.markdown("**Top Goalkeepers — Clean Sheets**")
        st.dataframe(gk[["Team", "Clean Sheets", "Goalkeeper Saves", "Goals Conceded"]].head(10),
                     use_container_width=True, hide_index=True)
    with c3:
        st.markdown("**Defensive Pressure Applied**")
        st.dataframe(
            tdata["defending"][["Team", "Defensive Pressure Applied", "Defensive Pressure Directly Applied",
                                "Ball Recovery Time (s)"]]\
                .sort_values("Defensive Pressure Applied", ascending=False).head(10),
            use_container_width=True, hide_index=True)

    st.markdown("---")

    # Distribution and physical leaderboards
    st.markdown("#### 🎯 Distribution & Physical")
    dist = tdata["distribution"].sort_values("Passing Accuracy (%)", ascending=False)
    phys = tdata["physical"].sort_values("Total Distance (m)", ascending=False)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Top 10 — Passing Accuracy (%)**")
        st.dataframe(dist[["Team", "Passing Accuracy (%)", "Passes Completed"]].head(10),
                     use_container_width=True, hide_index=True)
    with c2:
        st.markdown("**Top 10 — Total Distance Covered**")
        st.dataframe(phys[["Team", "Total Distance (m)", "Sprints", "High Speed Running"]].head(10),
                     use_container_width=True, hide_index=True)
    with c3:
        st.markdown("**Top 10 — Take-Ons Completed**")
        st.dataframe(
            tdata["distribution"][["Team", "Take-Ons Completed", "Crosses", "Crossing Accuracy (%)"]]\
                .sort_values("Take-Ons Completed", ascending=False).head(10),
            use_container_width=True, hide_index=True)

    st.markdown("---")

    # Discipline and movement leaderboards
    st.markdown("#### 🟨 Discipline & Movement")
    disc = tdata["discipline"]
    move = tdata["movement"].sort_values("Offers To Receive", ascending=False)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Most Disciplined — Fewest Fouls**")
        st.dataframe(
            disc[["Team", "Fouls For", "Yellow Cards", "Red Cards"]]\
                .sort_values("Fouls For", ascending=True).head(10),
            use_container_width=True, hide_index=True)
    with c2:
        st.markdown("**Most Bookings — Yellow Cards**")
        st.dataframe(
            disc[["Team", "Yellow Cards", "Red Cards", "Fouls For"]]\
                .sort_values("Yellow Cards", ascending=False).head(10),
            use_container_width=True, hide_index=True)
    with c3:
        st.markdown("**Top 10 — Offers To Receive**")
        st.dataframe(
            move[["Team", "Offers To Receive", "Receptions Under Pressure", "Player Involvement"]]\
                .head(10) if "Player Involvement" in move.columns
                else move[["Team", "Offers To Receive", "Receptions Under Pressure"]].head(10),
            use_container_width=True, hide_index=True)