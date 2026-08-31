# KickCore Analytics - Player & Team Explorer

import html as html_module
import streamlit as st

from utils import (
    set_background, inject_css, sidebar_nav,
    get_flag_url, get_team_flag_url,
    get_wikipedia_image, load_players, load_teams,
    get_all_player_names
)

# Page setup
st.set_page_config(page_title="Explorer (KickCore)", page_icon="🔍", layout="wide")
set_background("assets/bg.png")
inject_css()
sidebar_nav()

st.markdown('<div class="section-title">Explorer</div>', unsafe_allow_html=True)
st.markdown("---")

# Create two main tabs
tab_player, tab_team = st.tabs(["⚽  Player Stats", "🌍  Team Stats"])

# Player explorer section
with tab_player:
    pdata = load_players()
    # Unified master player list from all datasets
    player_names = get_all_player_names()
    player_search = st.selectbox("Search Player", [""] + player_names, key="explorer_player_search")

    if not player_search:
        st.info("Select a player to view their profile and statistics.")
    else:
        # Try golden_boot first, fall back to physical if no scoring stats
        gb_row = pdata["golden_boot"][pdata["golden_boot"]["Name"] == player_search]
        if gb_row.empty:
            phys_row = pdata["physical"][pdata["physical"]["Name"] == player_search]
            if phys_row.empty:
                st.warning("Player not found in any dataset.")
                st.stop()
            phys_row = phys_row.iloc[0]
            nat = phys_row.get("Nationality", "")
            pos = phys_row.get("Position", "")
            goals = 0
            assists = 0
            minutes_played = 0
        else:
            gb_row = gb_row.iloc[0]
            nat = gb_row["Nationality"]
            pos = gb_row["Position"]
            goals = int(gb_row["Goals"])
            assists = int(gb_row["Assists"])
            minutes_played = int(gb_row["Minutes Played"])

        st.markdown("---")
        col_info, col_stats = st.columns([2.4, 3.8])

        with col_info:
            with st.spinner("Loading photo..."):
                img_url = get_wikipedia_image(player_search)
            flag_url = get_flag_url(nat)

            # Escape name, nationality and position for safe HTML
            safe_name = html_module.escape(player_search)
            safe_nat = html_module.escape(nat)
            safe_pos = html_module.escape(pos)

            # Build flag and player image HTML
            flag_html = (
                f'<img src="{flag_url}" width="70" style="border-radius:5px;margin-bottom:10px"><br>'
                if flag_url else ""
            )
            if img_url:
                img_html = f'<img src="{html_module.escape(img_url)}" style="width:150px;height:190px;object-fit:cover;object-position:center 15%;border-radius:12px;display:block;margin-bottom:0">'
            else:
                img_html = '<div style="width:150px;height:190px;background:rgba(26,58,92,0.9);border:2px solid rgba(232,200,74,0.3);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:4rem">&#128100;</div>'

            # Render player profile card
            st.markdown(f"""
            <div style="display:flex;gap:16px;align-items:stretch">
                <div style="flex-shrink:0">{img_html}</div>
                <div style="background:rgba(10,25,55,0.97);border:1px solid rgba(232,200,74,0.3);
                    border-radius:14px;padding:18px 20px;flex:1">
                    {flag_html}
                    <div style="color:#e8c84a;font-size:1.35rem;font-weight:800;margin-bottom:10px">{safe_name}</div>
                    <div style="color:#a8c8e8;font-size:1rem;margin-top:6px">🌍 &nbsp;<strong style="color:white">{safe_nat}</strong></div>
                    <div style="color:#a8c8e8;font-size:1rem;margin-top:6px">🎽 &nbsp;<strong style="color:white">{safe_pos}</strong></div>
                    <div style="color:#a8c8e8;font-size:1rem;margin-top:6px">⚽ Goals: <strong style="color:#e8c84a">{goals}</strong></div>
                    <div style="color:#a8c8e8;font-size:1rem;margin-top:6px">🎯 Assists: <strong style="color:#e8c84a">{assists}</strong></div>
                    <div style="color:#a8c8e8;font-size:1rem;margin-top:6px">⏱️ Minutes: <strong style="color:white">{minutes_played}</strong></div>
                </div>
            </div>""", unsafe_allow_html=True)

        with col_stats:
            # Category buttons for player stats
            p_tab_labels = ["Golden Boot", "Attacking", "Distribution", "Defending",
                            "Discipline", "Goalkeeping", "Movement", "Physical"]
            p_tab_keys = ["golden_boot", "attacking", "distribution", "defending",
                            "discipline", "goalkeeping", "movement", "physical"]

            r1 = st.columns(4)
            for i, label in enumerate(p_tab_labels[:4]):
                if r1[i].button(label, key=f"pbtn_{i}", use_container_width=True):
                    st.session_state["p_active_tab"] = i
            r2 = st.columns(4)
            for i, label in enumerate(p_tab_labels[4:], start=4):
                if r2[i - 4].button(label, key=f"pbtn_{i}", use_container_width=True):
                    st.session_state["p_active_tab"] = i

            # Show selected category stats
            active = st.session_state.get("p_active_tab", 0)
            key = p_tab_keys[active]
            df = pdata[key]
            row = df[df["Name"] == player_search]
            st.markdown(f"<div style='color:#e8c84a;font-size:1rem;font-weight:700;margin:10px 0 4px'>📂 {html_module.escape(p_tab_labels[active])}</div>", unsafe_allow_html=True)
            if row.empty:
                st.info("No data available for this player in this category.")
            else:
                row = row.iloc[0]
                # Filter out non-stat columns
                stat_cols = [c for c in df.columns if c not in ["Rank", "Name", "Nationality", "Position"]]
                n = len(stat_cols)
                # Decide how many cards per row
                per_row = 5 if n >= 10 else 4 if n >= 7 else 3 if n >= 4 else n
                for i in range(0, n, per_row):
                    chunk = stat_cols[i:i + per_row]
                    cells = ""
                    for col_name in chunk:
                        val = html_module.escape(str(row[col_name]))
                        safe_col = html_module.escape(col_name)
                        cells += f"""<div style="flex:1;min-width:0;background:rgba(10,25,55,0.97);
                            border:1px solid rgba(168,200,232,0.22);border-radius:12px;
                            padding:16px 18px;display:flex;flex-direction:column;justify-content:space-between;min-height:105px">
                            <div style="color:#a8c8e8;font-size:0.88rem;line-height:1.4;margin-bottom:6px">{safe_col}</div>
                            <div style="color:#e8c84a;font-size:1.5rem;font-weight:800">{val}</div>
                        </div>"""
                    st.markdown(f"""<div style="display:flex;gap:12px;margin-bottom:12px">{cells}</div>""", unsafe_allow_html=True)

# Team explorer section
with tab_team:
    tdata = load_teams()
    all_teams = sorted(tdata["attacking"]["Team"].tolist())
    team_search = st.selectbox("Search Team", [""] + all_teams, key="explorer_team_search")

    if not team_search:
        st.info("Select a team to view their statistics.")
    else:
        st.markdown("---")
        col_flag, col_stats = st.columns([1.4, 3.8])

        with col_flag:
            # Get team flag and basic attacking stats
            flag_url = get_team_flag_url(team_search)
            atk = tdata["attacking"][tdata["attacking"]["Team"] == team_search]
            safe_team = html_module.escape(team_search)
            flag_html = (
                f'<img src="{flag_url}" width="90" style="border-radius:5px;margin-bottom:12px"><br>'
                if flag_url else ""
            )
            if not atk.empty:
                row = atk.iloc[0]
                # Render team profile card
                st.markdown(f"""
                <div style="background:rgba(10,25,55,0.97);border:1px solid rgba(232,200,74,0.3);
                    border-radius:14px;padding:22px 24px;margin-top:4px">
                    {flag_html}
                    <div style="color:#e8c84a;font-size:1.55rem;font-weight:800;margin-bottom:14px">{safe_team}</div>
                    <div style="color:#a8c8e8;font-size:1.05rem;margin-top:8px">⚽ Goals: <strong style="color:#e8c84a;font-size:1.15rem">{int(row['Goals'])}</strong></div>
                    <div style="color:#a8c8e8;font-size:1.05rem;margin-top:8px">🎯 Assists: <strong style="color:#e8c84a;font-size:1.15rem">{int(row['Assists'])}</strong></div>
                    <div style="color:#a8c8e8;font-size:1.05rem;margin-top:8px">📊 xG: <strong style="color:white;font-size:1.15rem">{row['xG']}</strong></div>
                    <div style="color:#a8c8e8;font-size:1.05rem;margin-top:8px">🔵 Possession: <strong style="color:white;font-size:1.15rem">{row['Possession Control (%)']}</strong></div>
                </div>""", unsafe_allow_html=True)

        with col_stats:
            # Category buttons for team stats
            t_tab_labels = ["Attacking", "Distribution", "Defending", "Discipline",
                            "Goalkeeping", "Movement", "Physical"]
            t_tab_keys = ["attacking", "distribution", "defending", "discipline",
                            "goalkeeping", "movement", "physical"]

            tr1 = st.columns(4)
            for i, label in enumerate(t_tab_labels[:4]):
                if tr1[i].button(label, key=f"tbtn_{i}", use_container_width=True):
                    st.session_state["t_active_tab"] = i
            tr2 = st.columns(4)
            for i, label in enumerate(t_tab_labels[4:], start=4):
                if tr2[i - 4].button(label, key=f"tbtn_{i}", use_container_width=True):
                    st.session_state["t_active_tab"] = i

            # Show selected category stats
            active = st.session_state.get("t_active_tab", 0)
            key = t_tab_keys[active]
            df = tdata[key]
            row = df[df["Team"] == team_search]
            st.markdown(f"<div style='color:#e8c84a;font-size:1rem;font-weight:700;margin:10px 0 4px'>📂 {html_module.escape(t_tab_labels[active])}</div>", unsafe_allow_html=True)
            if row.empty:
                st.info("No data available for this team in this category.")
            else:
                row = row.iloc[0]
                # Filter out non-stat columns
                stat_cols = [c for c in df.columns if c not in ["Rank", "Team"]]
                n = len(stat_cols)
                # Decide how many cards per row
                per_row = 5 if n >= 10 else 4 if n >= 7 else 3 if n >= 4 else n
                for i in range(0, n, per_row):
                    chunk = stat_cols[i:i + per_row]
                    cells = ""
                    for col_name in chunk:
                        val = html_module.escape(str(row[col_name]))
                        safe_col = html_module.escape(col_name)
                        cells += f"""<div style="flex:1;min-width:0;background:rgba(10,25,55,0.97);
                            border:1px solid rgba(168,200,232,0.22);border-radius:12px;
                            padding:16px 18px;display:flex;flex-direction:column;justify-content:space-between;min-height:105px">
                            <div style="color:#a8c8e8;font-size:0.88rem;line-height:1.4;margin-bottom:6px">{safe_col}</div>
                            <div style="color:#e8c84a;font-size:1.5rem;font-weight:800">{val}</div>
                        </div>"""
                    st.markdown(f"""<div style="display:flex;gap:12px;margin-bottom:12px">{cells}</div>""", unsafe_allow_html=True)