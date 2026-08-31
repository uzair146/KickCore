# KickCore Analytics - Shared utilities
import base64
import html
import os
import pandas as pd
from pathlib import Path
import streamlit as st

# Base directory relative to this file
BASE_DIR = Path(__file__).parent

# Build background CSS from image (cached)
@st.cache_data(show_spinner=False)
def _get_background_css(image_path: str) -> str:
    try:
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        ext = Path(image_path).suffix.lstrip(".")
        return f"""
        <style>
        .stApp {{
            background-image: url("data:image/{ext};base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .stApp > header {{ background: transparent !important; }}
        </style>
        """
    except Exception:
        return ""

# Apply background image to the page
def set_background(image_path: str):
    css = _get_background_css(str(BASE_DIR / image_path))
    if css:
        st.markdown(css, unsafe_allow_html=True)

# Inject global custom CSS styles
def inject_css():
    st.markdown("""
    <style>

    /* Hide Streamlit default sidebar nav */
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarNavItems"],
    [data-testid="stSidebarNavSeparator"] { display: none !important; }

    /* Main content block */
    .main .block-container {
        background: rgba(4, 8, 18, 0.95) !important;
        border-radius: 16px;
        padding: 2rem 2.5rem;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(232,200,74,0.2);
    }

    /* Global base font */
    html, body, .stApp, [data-testid="stAppViewContainer"],
    [data-testid="stMarkdownContainer"], .main, .block-container {
        font-size: 14px !important;
    }

    /* Sidebar background & colors */
    section[data-testid="stSidebar"] {
        background: rgba(4, 8, 18, 0.97) !important;
        border-right: 1px solid rgba(232,200,74,0.25);
    }
    section[data-testid="stSidebar"] a:hover { color: #e8c84a !important; }

    /* Markdown text */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] span,
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #e0e8f0 !important;
        font-size: 1.25rem !important;
        line-height: 1.8 !important;
    }

    /* Headings */
    [data-testid="stMarkdownContainer"] h1, .stMarkdown h1 { font-size: 2.2rem !important; color: #e8c84a !important; }
    [data-testid="stMarkdownContainer"] h2, .stMarkdown h2 { font-size: 1.8rem !important; color: #e8c84a !important; }
    [data-testid="stMarkdownContainer"] h3, .stMarkdown h3 { font-size: 1.5rem !important; color: #e8c84a !important; }
    h1, h2, h3 { color: #e8c84a !important; }

    /* Caption */
    [data-testid="stCaptionContainer"] p { font-size: 1.1rem !important; color: #a8c8e8 !important; }

    /* Radio + Checkbox */
    [data-testid="stRadio"] label span,
    [data-testid="stCheckbox"] label span,
    [data-testid="stRadio"] label,
    [data-testid="stCheckbox"] label { font-size: 1.2rem !important; color: #e0e8f0 !important; }

    /* Alert / Info */
    [data-testid="stAlert"] p { font-size: 1.2rem !important; }

    hr { border-color: rgba(232,200,74,0.2) !important; }

    /* Section title */
    .section-title {
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        color: #e8c84a !important;
        background: #060e1f;
        border-radius: 10px;
        padding: 12px 36px;
        text-align: center;
        display: block;
        margin: 1.2rem auto 1rem auto;
        width: fit-content;
        border: 1px solid rgba(232,200,74,0.4);
        letter-spacing: 1px;
    }

    /* Metric cards (custom HTML) */
    .metric-card {
        background: rgba(20,45,80,0.95);
        border: 1px solid rgba(232,200,74,0.4);
        border-radius: 12px;
        padding: 1.2rem 1rem;
        text-align: center;
    }
    .metric-value {
        font-size: 2.4rem !important;
        font-weight: 800 !important;
        color: #e8c84a !important;
        line-height: 1.2 !important;
    }
    .metric-label {
        font-size: 1.1rem !important;
        color: #a8c8e8 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }

    /* Player card */
    .player-card {
        background: rgba(20,45,80,0.95);
        border: 1px solid rgba(232,200,74,0.35);
        border-radius: 14px;
        padding: 1.1rem 1.2rem;
        margin-bottom: 0.5rem;
    }

    /* Streamlit metric widget */
    [data-testid="stMetricValue"] { color: #e8c84a !important; font-weight: 800 !important; font-size: 2.1rem !important; }
    [data-testid="stMetricLabel"] { color: #a8c8e8 !important; font-size: 1.05rem !important; }
    [data-testid="stMetric"] {
        background: rgba(15, 35, 65, 0.97) !important;
        border: 1px solid rgba(232,200,74,0.3) !important;
        border-radius: 10px !important;
        padding: 14px 16px !important;
    }

    /* Unified Tab pills (used by all pages) */
    .stTabs [data-baseweb="tab-list"] {
        background: #091529 !important;
        border-radius: 50px !important;
        padding: 5px 8px !important;
        gap: 4px !important;
        width: fit-content !important;
        margin: 0 auto !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 50px !important;
        color: #a8c8e8 !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        padding: 10px 30px !important;
        border: none !important;
        transition: all 0.2s !important;
    }
    .stTabs [aria-selected="true"] {
        background: #1a3a6e !important;
        color: #e0e8f0 !important;
        border-radius: 50px !important;
        border: 1px solid rgba(168,200,232,0.35) !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: #152a55 !important;
        color: #e0e8f0 !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background: rgba(6, 16, 35, 0.97) !important;
        border-radius: 0 0 14px 14px !important;
        padding: 1.5rem !important;
        border: 1px solid rgba(232,200,74,0.15) !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(20,45,80,0.95) !important;
        border: 1px solid rgba(232,200,74,0.3) !important;
        color: #e0e8f0 !important;
        font-size: 1.15rem !important;
    }
    .stSelectbox label { font-size: 1.15rem !important; color: #a8c8e8 !important; }
    div[data-baseweb="select"] > div { font-size: 1.1rem !important; }

    /* Radio */
    [data-testid="stRadio"] {
        background: rgba(10, 25, 50, 0.97) !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
    }
    [data-testid="stRadio"] label { font-size: 1.15rem !important; }

    /* Slider */
    [data-testid="stSlider"] {
        background: rgba(10, 25, 50, 0.95) !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
    }

    /* Alerts */
    .stAlert, [data-testid="stAlert"] {
        background: rgba(10, 25, 50, 0.97) !important;
        font-size: 1.15rem !important;
    }

    /* Dataframe / Table */
    [data-testid="stDataFrame"] th,
    .stDataFrame th {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: #e8c84a !important;
        padding: 12px 14px !important;
    }
    [data-testid="stDataFrame"] td,
    .stDataFrame td {
        font-size: 1.15rem !important;
        color: #e0e8f0 !important;
        padding: 10px 14px !important;
    }

    /* Download button */
    [data-testid="stDownloadButton"] button {
        background: rgba(20,45,80,0.95) !important;
        border: 1px solid rgba(232,200,74,0.4) !important;
        color: #e8c84a !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        padding: 12px 20px !important;
        transition: all 0.2s !important;
    }
    [data-testid="stDownloadButton"] button:hover {
        background: rgba(232,200,74,0.15) !important;
    }

    /* Buttons */
    .stButton button {
        background: rgba(20,45,80,0.95) !important;
        border: 1px solid rgba(168,200,232,0.3) !important;
        color: #e0e8f0 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.2s !important;
    }
    .stButton button:hover {
        border-color: rgba(232,200,74,0.5) !important;
        color: #e8c84a !important;
    }

    /* Multiselect */
    [data-testid="stMultiSelect"] > div > div {
        background: rgba(20,45,80,0.95) !important;
        border: 1px solid rgba(232,200,74,0.3) !important;
        font-size: 1.1rem !important;
    }

    /* Chart / viz titles */
    .chart-title {
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        color: #e8c84a !important;
        text-align: center;
        margin: 1rem 0 0.5rem 0;
    }
    .viz-title {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #e8c84a !important;
    }

    /* Page title / desc */
    .page-title {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #e8c84a !important;
    }
    .page-desc {
        background: #1a2e50;
        border-radius: 8px;
        padding: 12px 22px;
        color: #e0e8f0;
        font-size: 1.25rem !important;
        margin-bottom: 1.2rem;
        display: block;
    }
    .select-box-wrap {
        background: rgba(10, 25, 55, 0.97);
        border: 1px solid rgba(232,200,74,0.3);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
    }
    .select-label {
        color: #a8c8e8;
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .section-heading {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #e8c84a !important;
        margin-bottom: 1rem;
    }

    </style>
    """, unsafe_allow_html=True)

# Custom sidebar navigation
def sidebar_nav():
    with st.sidebar:
        st.markdown("""
        <style>
        .kick-title {
            text-align: center !important;
            font-size: 2.6rem !important;
            font-weight: 900 !important;
            color: #e8c84a !important;
            margin-bottom: 2px !important;
            letter-spacing: 3px !important;
            text-shadow: 0 2px 18px rgba(232,200,74,0.5) !important;
        }
        .kick-subtitle {
            text-align: center !important;
            color: #a8c8e8 !important;
            font-size: 1.15rem !important;
            margin-bottom: 10px !important;
            font-style: italic !important;
        }
        section[data-testid="stSidebar"] a[data-testid="stPageLink"] p,
        section[data-testid="stSidebar"] a[data-testid="stPageLink"] span,
        section[data-testid="stSidebar"] [data-testid="stPageLink"] p,
        section[data-testid="stSidebar"] [data-testid="stPageLink"] span {
            font-size: 1.4rem !important;
            font-weight: 600 !important;
        }
        </style>
        <div class="kick-title">⚽ KickCore</div>
        <div class="kick-subtitle">FIFA World Cup 2026</div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.page_link("app.py", label="🏠  Home")
        st.page_link("pages/1_explorer.py", label="🔍  Player Explorer")
        st.page_link("pages/2_stats.py", label="📊  Statistics")
        st.page_link("pages/3_compare.py", label="⚔️  Comparison")
        st.page_link("pages/4_teams.py", label="🌍  Team Stats")
        st.page_link("pages/5_charts.py", label="📈  Visualizations")
        st.page_link("pages/6_download.py", label="💾  Download")
        st.markdown("---")
        st.caption("Data: FIFA World Cup 2026™")

# Nationality code to ISO2 mapping for flags
nat_to_iso2 = {
    "FRA": "fr", "ARG": "ar", "ENG": "gb-eng", "NOR": "no",
    "ESP": "es", "BEL": "be", "NED": "nl", "GER": "de",
    "BRA": "br", "POR": "pt", "MAR": "ma", "SEN": "sn",
    "USA": "us", "MEX": "mx", "CAN": "ca", "JPN": "jp",
    "KOR": "kr", "AUS": "au", "SUI": "ch", "CRO": "hr",
    "URU": "uy", "COL": "co", "ECU": "ec", "ALG": "dz",
    "EGY": "eg", "GHA": "gh", "CIV": "ci", "CMR": "cm",
    "IRN": "ir", "KSA": "sa", "QAT": "qa", "SWE": "se",
    "DEN": "dk", "AUT": "at", "SCO": "gb-sct", "TUR": "tr",
    "POL": "pl", "CZE": "cz", "SRB": "rs", "ROU": "ro",
    "UKR": "ua", "RSA": "za", "CPV": "cv", "NZL": "nz",
    "HAI": "ht", "PAN": "pa", "PAR": "py", "BIH": "ba",
    "COD": "cd", "IRQ": "iq", "JOR": "jo", "UZB": "uz",
    "TUN": "tn", "CUW": "cw",
}

# Team full-name to ISO3 code mapping
team_to_nat = {
    "England": "ENG", "France": "FRA", "Argentina": "ARG",
    "Spain": "ESP", "Belgium": "BEL", "Netherlands": "NED",
    "Germany": "GER", "Brazil": "BRA", "Portugal": "POR",
    "Morocco": "MAR", "Senegal": "SEN", "USA": "USA",
    "Mexico": "MEX", "Canada": "CAN", "Japan": "JPN",
    "South Korea": "KOR", "Australia": "AUS", "Switzerland": "SUI",
    "Croatia": "CRO", "Uruguay": "URU", "Colombia": "COL",
    "Ecuador": "ECU", "Algeria": "ALG", "Egypt": "EGY",
    "Ghana": "GHA", "Norway": "NOR", "Sweden": "SWE",
    "Denmark": "DEN", "Austria": "AUT", "Scotland": "SCO",
    "Turkey": "TUR", "Iran": "IRN", "Saudi Arabia": "KSA",
    "Qatar": "QAT", "Ivory Coast": "CIV", "Cameroon": "CMR",
    "Bosnia and Herzegovina": "BIH", "DR Congo": "COD",
    "Iraq": "IRQ", "Jordan": "JOR", "Uzbekistan": "UZB",
    "Tunisia": "TUN", "New Zealand": "NZL", "Haiti": "HAI",
    "Panama": "PAN", "Paraguay": "PAR", "South Africa": "RSA",
    "Cape Verde": "CPV", "Curacao": "CUW",
}

# Get flag URL from nationality code
def get_flag_url(nat_code: str) -> str | None:
    iso2 = nat_to_iso2.get(nat_code, "").lower()
    return f"https://flagcdn.com/w80/{iso2}.png" if iso2 else None

# Get flag URL from team full name
def get_team_flag_url(team_name: str) -> str | None:
    """Get flag URL directly from a team's full name."""
    nat_code = team_to_nat.get(team_name, "")
    return get_flag_url(nat_code)

# Look for a local player image in assets/players
def get_local_image_path(player_name: str) -> str | None:
    safe = player_name.replace("/", "-").replace("\\", "-").replace(":", "")
    for ext in [".jpg", ".jpeg", ".png", ".webp"]:
        path = BASE_DIR / "assets" / "players" / f"{safe}{ext}"
        if path.exists():
            return str(path)
    return None

# Fetch player image from Wikipedia (cached)
@st.cache_data(show_spinner=False)
def get_wikipedia_image(player_name: str) -> str | None:
    import urllib.request
    import urllib.parse
    import json
    import re

    headers = {
        "User-Agent": "KickCoreAnalytics/1.0 (football analytics project)",
        "Accept": "application/json",
    }

    def fetch_json(url):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=4) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception:
            return None

    def normalize(name):
        name = re.sub(r"[-\u2010-\u2014]", " ", str(name).strip())
        return re.sub(r"\s+", " ", name).strip().lower()

    def names_match(original, wiki_title):
        o = normalize(original)
        t = normalize(wiki_title)
        if o == t:
            return True
        for suffix in [" footballer", " football player", " soccer player"]:
            if t == o + suffix:
                return True
        return False

    def get_summary(title):
        encoded = urllib.parse.quote(title.replace(" ", "_"))
        return fetch_json(f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}")

    original_name = str(player_name).strip()
    if not original_name:
        return None

    # Try hyphenated variant for names like "Wan Bissaka"
    hyphenated = re.sub(r"\bwan\s+bissaka\b", "Wan-Bissaka", original_name, flags=re.IGNORECASE)
    search_names = list(dict.fromkeys([original_name, hyphenated]))

    football_terms = [
        "footballer", "football player", "soccer player",
        "professional football", "association football",
        "football defender", "football midfielder",
        "football forward", "goalkeeper",
    ]
    bad_terms = ["disambiguation", "may refer to", "surname", "family name", "given name"]

    for name in search_names:
        summary = get_summary(name)
        if not summary:
            continue
        page_title = summary.get("title", "")
        if not names_match(name, page_title):
            continue
        desc = str(summary.get("description", "")).lower()
        extract = str(summary.get("extract", "")).lower()
        if any(t in desc or t in extract for t in bad_terms):
            continue
        if not any(t in desc or t in extract for t in football_terms):
            continue
        img = summary.get("thumbnail", {}).get("source")
        if img:
            return img

    return None

# Fetch Wikipedia images for multiple players in parallel
def fetch_images_parallel(names: list[str]) -> dict[str, str | None]:
    """Fetch Wikipedia images for multiple players in parallel (max 4 threads)."""
    from concurrent.futures import ThreadPoolExecutor, as_completed
    results = {name: None for name in names}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(get_wikipedia_image, name): name for name in names}
        for future in as_completed(futures):
            name = futures[future]
            try:
                results[name] = future.result()
            except Exception:
                results[name] = None
    return results

# Generate avatar HTML with initials when no photo exists
def get_avatar_html(name: str, color: str = "#e8c84a", size: int = 160) -> str:
    initials = "".join(w[0].upper() for w in name.split()[:2])
    return f"""
    <div style="width:{size}px;height:{int(size*1.2)}px;
        background:linear-gradient(135deg,rgba(20,45,80,0.98),rgba(8,20,45,0.98));
        border:2px solid {color};border-radius:12px;
        display:flex;flex-direction:column;align-items:center;justify-content:center;
        font-size:{int(size*0.3)}px;font-weight:900;color:{color};
        letter-spacing:2px;font-family:sans-serif;
        box-shadow:0 4px 20px rgba(0,0,0,0.5);">
        {html.escape(initials)}
        <div style="font-size:{int(size*0.08)}px;color:#a8c8e8;
            margin-top:8px;font-weight:400;letter-spacing:1px;text-transform:uppercase">
            No Photo
        </div>
    </div>"""

# Shorten long names for display in metric cards
def format_scorer_name(full_name: str) -> str:
    """Shorten long names for display in metric cards."""
    if not full_name or not full_name.strip():
        return "N/A"
    parts = full_name.split()
    if len(parts) == 1 or len(full_name) <= 14:
        return full_name
    return f"{parts[0]} {parts[-1][0]}."

# Load a CSV relative to BASE_DIR with error if missing
def _csv(relative_path: str) -> pd.DataFrame:
    """Load a CSV relative to BASE_DIR with a friendly error if missing."""
    path = BASE_DIR / relative_path
    if not path.exists():
        st.error(
            f"⚠️ Data file not found: `{relative_path}`\n\n"
            "Please run the data pipeline first:\n"
            "```\npython cleaner.py\npython analysis.py\n```"
        )
        st.stop()
    return pd.read_csv(path)

# Load all cleaned player datasets (cached)
@st.cache_data(show_spinner=False)
def load_players() -> dict[str, pd.DataFrame]:
    base = "data/cleaned/player_stats"
    return {
        "golden_boot": _csv(f"{base}/player_golden_boot.csv"),
        "attacking": _csv(f"{base}/player_attacking.csv"),
        "distribution": _csv(f"{base}/player_distribution.csv"),
        "defending": _csv(f"{base}/player_defending.csv"),
        "discipline": _csv(f"{base}/player_discipline.csv"),
        "goalkeeping": _csv(f"{base}/player_goalkeeping.csv"),
        "movement": _csv(f"{base}/player_movement.csv"),
        "physical": _csv(f"{base}/player_physical.csv"),
    }

# Load all cleaned team datasets (cached)
@st.cache_data(show_spinner=False)
def load_teams() -> dict[str, pd.DataFrame]:
    base = "data/cleaned/team_stats"
    return {
        "attacking": _csv(f"{base}/team_attacking.csv"),
        "distribution": _csv(f"{base}/team_distribution.csv"),
        "defending": _csv(f"{base}/team_defending.csv"),
        "discipline": _csv(f"{base}/team_discipline.csv"),
        "goalkeeping": _csv(f"{base}/team_goalkeeping.csv"),
        "movement": _csv(f"{base}/team_movement.csv"),
        "physical": _csv(f"{base}/team_physical.csv"),
    }

# Master player list — union across all player datasets
@st.cache_data(show_spinner=False)
def get_all_player_names() -> list[str]:
    """Master player list — union across all player datasets."""
    pdata = load_players()
    names = set()
    for df in pdata.values():
        if "Name" in df.columns:
            names.update(df["Name"].dropna().tolist())
    return sorted(names)