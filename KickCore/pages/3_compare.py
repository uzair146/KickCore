# KickCore Analytics - Comparison Page
import html as html_module
import streamlit as st
from utils import (
    set_background, inject_css, sidebar_nav,
    get_flag_url, fetch_images_parallel,
    load_players, load_teams, get_all_player_names
)

# Page setup
st.set_page_config(page_title="Comparison — KickCore", page_icon="⚔️", layout="wide")
set_background("assets/bg.png")
inject_css()
sidebar_nav()

st.markdown('<div class="section-title">Comparison Tool</div>', unsafe_allow_html=True)
st.markdown("---")

# Build comparison table with winner highlighted
def stat_table(headers, rows_data):
    header_html = "".join(
        f'<th style="padding:8px 14px;color:#e8c84a;font-weight:700;text-align:center">{html_module.escape(h)}</th>'
        for h in headers
    )
    table_html = f"""
    <div style="background:rgba(10,25,55,0.97);border:1px solid rgba(232,200,74,0.25);
        border-radius:12px;padding:1rem;margin-top:0.5rem;overflow-x:auto">
    <table style="width:100%;border-collapse:collapse">
    <thead><tr style="border-bottom:1px solid rgba(232,200,74,0.3)">
        <th style="padding:8px 14px;color:#e8c84a;font-weight:700;text-align:left">Stat</th>
        {header_html}
    </tr></thead><tbody>"""

    for stat, vals, winner_idx in rows_data:
        cells = ""
        for i, val in enumerate(vals):
            color = "#2ecc71" if i == winner_idx else "#e0e8f0"
            weight = "800" if i == winner_idx else "400"
            cells += f'<td style="padding:8px 14px;color:{color};font-weight:{weight};text-align:center">{html_module.escape(str(val))}</td>'
        table_html += (
            f'<tr style="border-bottom:1px solid rgba(255,255,255,0.05)">'
            f'<td style="padding:8px 14px;color:#a8c8e8">{html_module.escape(stat)}</td>{cells}</tr>'
        )

    table_html += "</tbody></table></div>"
    st.markdown(table_html, unsafe_allow_html=True)

# Create main tabs
tab_player, tab_team = st.tabs(["⚽  Player Comparison", "🌍  Team Comparison"])

# Player comparison section
with tab_player:
    pdata = load_players()
    # Unified player list so all players are findable
    player_names = get_all_player_names()

    st.markdown("**Select up to 4 players:**")
    cols = st.columns(4)
    selected = []
    for i, col in enumerate(cols):
        options = [""] + [p for p in player_names if p not in selected]
        p = col.selectbox(f"Player {i+1}", options, key=f"cmp_p{i}")
        if p:
            selected.append(p)

    if len(selected) < 2:
        st.info("Select at least 2 players to compare.")
    else:
        st.markdown("---")

        # Fetch all Wikipedia images in parallel
        with st.spinner("Loading player photos..."):
            images = fetch_images_parallel(selected)

        # Render player profile cards
        card_cols = st.columns(len(selected))
        for col, name in zip(card_cols, selected):
            with col:
                row = pdata["golden_boot"][pdata["golden_boot"]["Name"] == name]
                # Fall back to physical dataset if not in golden_boot
                if row.empty:
                    row = pdata["physical"][pdata["physical"]["Name"] == name]
                if row.empty:
                    continue
                row = row.iloc[0]
                nat = row.get("Nationality", "")
                pos = row.get("Position", "")

                img = images.get(name)
                flag = get_flag_url(nat)
                safe_name = html_module.escape(name)
                safe_nat = html_module.escape(nat)
                safe_pos = html_module.escape(pos)

                if img:
                    media_html = f'<img src="{html_module.escape(img)}" style="width:120px;height:150px;object-fit:cover;object-position:center 20%;border-radius:10px;display:block">'
                else:
                    media_html = '<div style="width:120px;height:150px;background:rgba(26,58,92,0.9);border:2px solid rgba(232,200,74,0.3);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:3rem">&#128100;</div>'
                if flag:
                    flag_tag = f'<img src="{flag}" style="width:44px;height:auto;border-radius:3px;margin-top:8px">'
                else:
                    flag_tag = '<div style="height:28px;margin-top:8px"></div>'

                st.markdown(f"""
                <div style="display:flex;flex-direction:column;align-items:flex-start">
                    {media_html}
                    {flag_tag}
                    <div style="background:rgba(10,25,55,0.97);border:1px solid rgba(232,200,74,0.3);border-radius:10px;padding:8px 10px;margin-top:8px;width:100%;box-sizing:border-box">
                        <div style="color:#e8c84a;font-weight:800;font-size:0.95rem">{safe_name}</div>
                        <div style="color:#a8c8e8;font-size:0.82rem;margin-top:3px">{safe_nat} · {safe_pos}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # Merge player datasets for comparison
        gb = pdata["golden_boot"]
        atk = pdata["attacking"][["Name", "Nationality", "xG", "Attempts On Target"]]
        phys = pdata["physical"][["Name", "Nationality", "Top Speed (km/h)", "Sprints"]]
        dist = pdata["distribution"][["Name", "Nationality", "Passing Accuracy (%)",
                                      "Take-Ons Completed", "Crossing Accuracy (%)", "Passes Completed"]]
        gk = pdata["goalkeeping"][["Name", "Nationality", "Goalkeeper Saves",
                                     "Goalkeeper Actions Inside Penalty Area",
                                     "Goalkeeper Actions Outside Penalty Area"]]
        merged = (gb
                  .merge(atk, on=["Name", "Nationality"], how="left")
                  .merge(phys, on=["Name", "Nationality"], how="left")
                  .merge(dist, on=["Name", "Nationality"], how="left")
                  .merge(gk, on=["Name", "Nationality"], how="left"))

        # Stat profiles for player comparison tabs
        PROFILES = {
            "⚽ Scoring & Attacking": [
                ("Goals", "Goals"),
                ("Assists", "Assists"),
                ("xG", "xG"),
                ("Attempts On Target", "On Target"),
                ("Top Speed (km/h)", "Top Speed"),
                ("Sprints", "Sprints"),
            ],
            "🎯 Distribution": [
                ("Passing Accuracy (%)", "Pass Acc (%)"),
                ("Passes Completed", "Passes"),
                ("Take-Ons Completed", "Take-Ons"),
                ("Crossing Accuracy (%)", "Cross Acc (%)"),
                ("Assists", "Assists"),
            ],
            "🥅 Goalkeeping": [
                ("Goalkeeper Saves", "Saves"),
                ("Goalkeeper Actions Inside Penalty Area", "Actions In Box"),
                ("Goalkeeper Actions Outside Penalty Area", "Actions Out Box"),
            ],
        }

        # Render comparison tables per profile
        rtabs = st.tabs(list(PROFILES.keys()))
        for rtab, (profile_name, stat_pairs) in zip(rtabs, PROFILES.items()):
            with rtab:
                rows_data = []
                for col_key, label in stat_pairs:
                    vals = []
                    for name in selected:
                        r = merged[merged["Name"] == name]
                        v = float(r.iloc[0][col_key]) if (not r.empty and col_key in r.columns and not r.iloc[0][col_key] != r.iloc[0][col_key]) else 0.0
                        vals.append(v)
                    winner = vals.index(max(vals)) if max(vals) > 0 else -1
                    rows_data.append((label, [round(v, 2) for v in vals], winner))
                # Show full name in headers
                stat_table(selected, rows_data)

# Team comparison section
with tab_team:
    tdata = load_teams()
    all_teams = sorted(tdata["attacking"]["Team"].tolist())

    st.markdown("**Select up to 4 teams:**")
    cols = st.columns(4)
    t_selected = []
    for i, col in enumerate(cols):
        options = [""] + [t for t in all_teams if t not in t_selected]
        t = col.selectbox(f"Team {i+1}", options, key=f"cmp_t{i}")
        if t:
            t_selected.append(t)

    if len(t_selected) < 2:
        st.info("Select at least 2 teams to compare.")
    else:
        st.markdown("---")
        # Merge team datasets for comparison
        atk = tdata["attacking"]
        defend = tdata["defending"][["Team", "Goals Conceded", "Forced Turnovers",
                                     "Defensive Pressure Applied", "Ball Recovery Time (s)"]]
        phys = tdata["physical"][["Team", "Total Distance (m)", "Sprints",
                                    "High Speed Running", "Average Speed (km/h)"]]
        dist = tdata["distribution"][["Team", "Passing Accuracy (%)",
                                        "Take-Ons Completed", "Passes Completed"]]
        merged_t = (atk
                    .merge(defend, on="Team", how="left")
                    .merge(phys, on="Team", how="left")
                    .merge(dist, on="Team", how="left"))

        # Stat profiles for team comparison tabs
        TEAM_PROFILES = {
            "⚽ Attacking": {
                "stats": [
                    ("Goals", "Goals"),
                    ("Assists", "Assists"),
                    ("Attempts On Target", "On Target"),
                    ("xG", "xG"),
                    ("Possession Control (%)", "Possession (%)"),
                    ("Attempts At Goal", "Attempts"),
                ],
                "invert": [],
            },
            "🛡️ Defending": {
                "stats": [
                    ("Forced Turnovers", "Turnovers"),
                    ("Defensive Pressure Applied", "Def Pressure"),
                    ("Ball Recovery Time (s)", "Recovery Time (s)"),
                    ("Goals Conceded", "Goals Conceded"),
                ],
                "invert": ["Goals Conceded", "Ball Recovery Time (s)"],
            },
            "🏃 Physical": {
                "stats": [
                    ("Total Distance (m)", "Distance (m)"),
                    ("Sprints", "Sprints"),
                    ("High Speed Running", "Hi-Speed Run"),
                    ("Average Speed (km/h)", "Avg Speed"),
                    ("Take-Ons Completed", "Take-Ons"),
                ],
                "invert": [],
            },
        }

        # Render comparison tables per profile
        rtabs = st.tabs(list(TEAM_PROFILES.keys()))
        for rtab, (profile_name, profile) in zip(rtabs, TEAM_PROFILES.items()):
            with rtab:
                invert_cols = profile["invert"]
                rows_data = []
                for col_key, label in profile["stats"]:
                    vals = []
                    for team in t_selected:
                        r = merged_t[merged_t["Team"] == team]
                        v = float(r.iloc[0][col_key]) if (not r.empty and col_key in r.columns) else 0.0
                        vals.append(v)
                    # Lower is better for inverted stats
                    if col_key in invert_cols:
                        non_zero = [v for v in vals if v > 0]
                        winner = vals.index(min(non_zero)) if non_zero else -1
                    else:
                        winner = vals.index(max(vals)) if max(vals) > 0 else -1
                    rows_data.append((label, [round(v, 2) for v in vals], winner))
                stat_table(t_selected, rows_data)