# KickCore Analytics - Team Stats Page

import html as html_module
import streamlit as st
from utils import set_background, inject_css, sidebar_nav, get_flag_url, load_teams

# Page setup
st.set_page_config(page_title="Team Stats — KickCore", page_icon="🌍", layout="wide")
set_background("assets/bg.png")
inject_css()
sidebar_nav()

# Page title banner
st.markdown("""
<div style="text-align:center;padding:1rem 0 0.5rem">
    <div style="display:inline-block;background:rgba(10,25,50,0.97);
        border:1px solid rgba(232,200,74,0.3);border-radius:12px;padding:14px 40px;">
        <div style="font-size:2rem;font-weight:800;color:#e8c84a;letter-spacing:2px">
            Team Stats
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Load team data and get sorted team list
data = load_teams()
all_teams = sorted(data["attacking"]["Team"].tolist())

# Team multi-select filter
st.markdown('<div class="select-box-wrap"><div class="select-label">Select Teams</div>', unsafe_allow_html=True)
selected_teams = st.multiselect(
    "",
    options=all_teams,
    default=[],
    placeholder="Choose teams..."
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Category tabs and keys
tab_names = ["Attacking", "Distribution", "Defending", "Discipline", "Goalkeeping", "Movement", "Physical"]
tab_keys = ["attacking", "distribution", "defending", "discipline", "goalkeeping", "movement", "physical"]

# Render each category tab
tabs = st.tabs(tab_names)
for tab, key in zip(tabs, tab_keys):
    with tab:
        df = data[key].copy()
        # Filter by selected teams if any
        if selected_teams:
            df = df[df["Team"].isin(selected_teams)]
        st.dataframe(df.reset_index(drop=True), use_container_width=True, hide_index=True)