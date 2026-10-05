# ⚽ KickCore Analytics

**An end-to-end data analytics project on FIFA World Cup 2026 (Canada · Mexico · USA)** — from web scraping and data cleaning to statistical analysis, visualization, and an interactive Streamlit dashboard.

KickCore covers **1,231 players** and **48 national teams** across **15 stat categories**, and lets you explore, compare, visualize, and download the data in one place.

---

## ✨ Features

- **Automated data collection** — Selenium + BeautifulSoup scraper pulls player and team stats from the official FIFA statistics pages (8 player tabs, 7 team tabs).
- **Data cleaning pipeline** — Pandas-based cleaner that fixes data types, handles the `xG Efficiency` format, and fills missing values intelligently (counts → `0`, rates/measurements → median).
- **Statistical analysis** — NumPy summary statistics (mean, median, std, percentiles) plus GroupBy breakdowns by nationality and position.
- **18 charts** — 10 Matplotlib + 8 Seaborn visualizations (heatmaps, violin plots, pair plots, KDE, regression, and more).
- **Interactive multi-page dashboard** — built with Streamlit, with a custom dark/gold theme.

---

## 🖥️ Dashboard Pages

| Page | What it does |
|------|--------------|
| **🏠 Home** | Tournament at a glance — total players, nations, goals, assists, cards, Golden Boot leader, top scoring team, top goalkeeper, and Top 5 scorers |
| **🔍 Explorer** | Search any player or team and view their full stat profile |
| **📊 Statistics** | Leaderboards: top performers, physical stats, discipline, position analysis, NumPy summary, and team leaderboards |
| **⚔️ Compare** | Head-to-head comparison for players and teams, with winners highlighted and radar-style profiles |
| **🌍 Teams** | Team stats across 7 categories with multi-team filtering |
| **📈 Visualizations** | Gallery of all Matplotlib and Seaborn charts |
| **💾 Download** | Download any raw/cleaned dataset as CSV |


---

## 🧱 Tech Stack

| Area | Tools |
|------|-------|
| **Language** | Python 3 |
| **Scraping** | Selenium, BeautifulSoup4, webdriver-manager |
| **Data processing** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **Dashboard** | Streamlit |

---

## 📁 Project Structure

```
KickCore/
├── app.py                  # Streamlit home page (entry point)
├── pages/
│   ├── 1_explorer.py       # Player & team explorer
│   ├── 2_stats.py          # Statistics dashboard
│   ├── 3_compare.py        # Player/team comparison tool
│   ├── 4_teams.py          # Team stats by category
│   ├── 5_charts.py         # Visualization gallery
│   └── 6_download.py       # CSV downloads
├── scraper.py              # Step 1: scrape data from FIFA
├── cleaner.py              # Step 2: clean raw data
├── analysis.py             # Step 3: statistical analysis
├── visualization.py        # Step 4: generate charts
├── utils.py                # Shared helpers (theme, CSS, data loaders, images)
├── assets/                 # Background image (and optional player photos)
├── charts/                 # 18 generated PNG charts
├── data/
│   ├── raw/                # Scraped CSVs (player_stats/, team_stats/)
│   ├── cleaned/            # Cleaned CSVs
│   └── analysis/           # Leaderboards & summary tables
└── requirements.txt
```

---

## 🔄 Data Pipeline

```
 FIFA Website ──► scraper.py ──► data/raw ──► cleaner.py ──► data/cleaned
                                                                  │
                          charts/ ◄── visualization.py ◄──────────┤
                                                                  │
                    data/analysis ◄── analysis.py ◄───────────────┘
                                           │
                                           ▼
                                   Streamlit Dashboard
```

### Datasets

**Player stats (8 files):** Golden Boot, Attacking, Distribution, Defending, Discipline, Goalkeeping, Movement, Physical

**Team stats (7 files):** Attacking, Distribution, Defending, Discipline, Goalkeeping, Movement, Physical

Examples of tracked metrics: goals, assists, xG, xG efficiency, shot conversion rate, passing accuracy, forced turnovers, saves, clean sheets, top speed, sprints, total distance, possession, and more.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/uzair146/KickCore.git
cd KickCore
```

### 2. Install dependencies

```bash
pip install streamlit pandas numpy matplotlib seaborn
```

To run the scraper as well:

```bash
pip install selenium beautifulsoup4 webdriver-manager
```

> The scraper also requires Google Chrome to be installed.

### 3. Run the dashboard

The repo already includes the scraped, cleaned, and analyzed data, so you can launch the app right away:

```bash
streamlit run app.py
```

### 4. (Optional) Re-run the full pipeline

```bash
python scraper.py          # scrape fresh data from FIFA
python cleaner.py          # clean raw data
python analysis.py         # generate leaderboards & summaries
python visualization.py    # regenerate all 18 charts
```

---

## 🧹 Cleaning Rules

- `xG Efficiency` values have the trailing `x` removed and are converted to floats.
- Non-numeric values in stat columns are coerced to numbers.
- Missing **count/event** stats (goals, assists, cards, saves, fouls, passes, etc.) are filled with `0`.
- Missing **rate/physical** stats (accuracy %, speed, distance) are filled with the column **median**.

---

## 🗺️ Roadmap

- [ ] Add match-by-match data and tournament bracket view
- [ ] Interactive charts (Plotly)
- [ ] Deploy to Streamlit Community Cloud
- [ ] Scheduled auto-refresh of scraped data

---

## ⚠️ Disclaimer

This is an independent educational/portfolio project and is **not affiliated with or endorsed by FIFA**. Statistics are collected from publicly available pages on the official FIFA website for learning and analysis purposes.

---

## 👤 Author

**Muhammad Uzair Hussain** — BSCS student, FAST NUCES (CFD Campus), building toward a career in data analytics and data science.

- GitHub: [@uzair146](https://github.com/uzair146)

⭐ If you found this project useful, consider giving it a star!
