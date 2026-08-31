# KickCore Analytics - FIFA World Cup 2026
# Scrapes player and team statistics from FIFA official website
import os
import time
import traceback
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# FIFA stats page URLs
player_url = (
    "https://www.fifa.com/en/tournaments/mens/worldcup/"
    "canadamexicousa2026/statistics/player-statistics"
)
team_url = (
    "https://www.fifa.com/en/tournaments/mens/worldcup/"
    "canadamexicousa2026/statistics/team-statistics"
)

# Player tab config: button text, name, csv file, columns
player_tabs = [
    {"button": "adidas Golden Boot", "name": "Golden Boot", "csv": "player_golden_boot.csv", "columns": ["Goals", "Assists", "Minutes Played"]},
    {"button": "Attacking", "name": "Attacking", "csv": "player_attacking.csv", "columns": ["Assists", "Attempts On Target", "Attempts At Goal", "Attempts At Goal Conv.Rate (%)", "Attempts Inside Penalty Area", "Attempts Outside Penalty Area", "Headed Attempts At Goal", "xG", "xG Efficiency", "Corners"]},
    {"button": "Distribution", "name": "Distribution", "csv": "player_distribution.csv", "columns": ["Passes", "Passes Completed", "Passing Accuracy (%)", "Crosses", "Crossing Accuracy (%)", "Take-Ons Completed", "Defensive Linebreaks Attempts", "Defensive Linebreaks Accuracy (%)", "Switches Of Play Attempts", "Switches Of Play Accuracy (%)"]},
    {"button": "Defending", "name": "Defending", "csv": "player_defending.csv", "columns": ["Own Goals", "Forced Turnovers", "Defensive Pressure Applied", "Defensive Pressure Directly Applied"]},
    {"button": "Discipline", "name": "Discipline", "csv": "player_discipline.csv", "columns": ["Fouls Against", "Fouls For", "Yellow Cards", "Red Cards", "Indirect Red Cards", "Offsides"]},
    {"button": "Goalkeeping", "name": "Goalkeeping", "csv": "player_goalkeeping.csv", "columns": ["Goalkeeper Saves", "Goalkeeper Actions Inside Penalty Area", "Goalkeeper Actions Outside Penalty Area"]},
    {"button": "Movement", "name": "Movement", "csv": "player_movement.csv", "columns": ["Offers To Receive", "Offers In Behind", "Offers In Between", "Offers In Front", "Offers Inside Team Shape", "Offers Outside Team Shape", "Receptions In Between", "Receptions Between Midfield And Defensive Line", "Receptions Under Pressure", "Player Involvement"]},
    {"button": "Physical", "name": "Physical", "csv": "player_physical.csv", "columns": ["Top Speed (km/h)", "High Speed Running", "Sprints", "Total Distance (m)"]},
]

# Team tab config: button text, name, csv file, columns
team_tabs = [
    {"button": "Attacking", "name": "Attacking", "csv": "team_attacking.csv", "columns": ["Goals", "Assists", "Attempts At Goal", "Attempts On Target", "Off Target Attempts", "Attempts At Goal Conv.Rate (%)", "Attempts Inside Penalty Area", "Attempts Outside Penalty Area", "Headed Attempts At Goal", "xG", "xG Efficiency", "Corners", "Possession Control (%)"]},
    {"button": "Distribution", "name": "Distribution", "csv": "team_distribution.csv", "columns": ["Passes Completed", "Passing Accuracy (%)", "Crosses", "Crossing Accuracy (%)", "Take-Ons Completed", "Defensive Linebreaks Attempts", "Defensive Linebreaks Accuracy (%)", "Switches Of Play Attempts", "Switches Of Play Accuracy (%)"]},
    {"button": "Defending", "name": "Defending", "csv": "team_defending.csv", "columns": ["Own Goals", "Goals Conceded", "Forced Turnovers", "Ball Recovery Time (s)", "Defensive Pressure Applied", "Defensive Pressure Directly Applied"]},
    {"button": "Discipline", "name": "Discipline", "csv": "team_discipline.csv", "columns": ["Fouls Against", "Fouls For", "Yellow Cards", "Red Cards", "Indirect Red Cards", "Offsides"]},
    {"button": "Goalkeeping", "name": "Goalkeeping", "csv": "team_goalkeeping.csv", "columns": ["Clean Sheets", "Goals Conceded", "Goalkeeper Saves", "Goalkeeper Actions Inside Penalty Area", "Goalkeeper Actions Outside Penalty Area"]},
    {"button": "Movement", "name": "Movement", "csv": "team_movement.csv", "columns": ["Offers To Receive", "Offers In Behind", "Offers In Between", "Offers In Front", "Offers Inside Team Shape", "Offers Outside Team Shape", "Receptions In Between", "Receptions Between Midfield And Defensive Line", "Receptions Under Pressure"]},
    {"button": "Physical", "name": "Physical", "csv": "team_physical.csv", "columns": ["Average Speed (km/h)", "High Speed Running", "Sprints", "Total Distance (m)"]},
]

# Output directories
from pathlib import Path as _Path
_BASE_DIR = _Path(__file__).parent
player_dir = str(_BASE_DIR / "data" / "raw" / "player_stats")
team_dir = str(_BASE_DIR / "data" / "raw" / "team_stats")

# CSS selectors
row_sel = "tr.row-even, tr.row-odd"
loadmore_sel = "button.button--has-loader"

# Launch Chrome browser with Selenium
def setup_driver():
    opts = Options()
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        print("Chrome ready.")
        return driver
    except Exception as e:
        print(f"WebDriver Manager failed: {e}")
        try:
            driver = webdriver.Chrome(options=opts)
            print("System Chrome ready.")
            return driver
        except Exception as e2:
            raise Exception(f"Chrome setup failed: {e2}")

# Click a stats tab button by its text
def click_tab(driver, button_text):
    for _ in range(3):
        try:
            for btn in driver.find_elements(By.CSS_SELECTOR, "button.filter-chip"):
                if button_text.lower() in btn.text.strip().lower():
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(3)
                    return True
            for btn in driver.find_elements(By.TAG_NAME, "button"):
                if button_text.lower() in btn.text.strip().lower():
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(3)
                    return True
        except Exception:
            time.sleep(1)
    print(f"  [WARN] Tab not found: '{button_text}'")
    return False

# Count currently loaded player rows
def get_row_count(driver):
    try:
        return len(driver.find_elements(By.CSS_SELECTOR, row_sel))
    except Exception:
        return 0

# Click Load More repeatedly until all rows are loaded
def load_all_rows(driver):
    prev = get_row_count(driver)
    clicks = 0
    no_chg = 0
    print(f"  Rows: {prev}", end="", flush=True)
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.8)
        btn = None
        try:
            candidate = driver.find_element(By.CSS_SELECTOR, loadmore_sel)
            if candidate.is_displayed() and candidate.is_enabled():
                btn = candidate
        except Exception:
            pass
        if btn is None:
            try:
                for b in driver.find_elements(By.TAG_NAME, "button"):
                    try:
                        if b.text.strip().lower() == "load more" and b.is_displayed():
                            btn = b
                            break
                    except Exception:
                        continue
            except Exception:
                pass
        if btn is None:
            print(f"  [Done] All rows loaded.")
            break
        try:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            driver.execute_script("arguments[0].click();", btn)
        except Exception:
            pass
        clicks += 1
        time.sleep(1.5)
        new = get_row_count(driver)
        if new > prev:
            print(f" -> {new}", end="", flush=True)
            prev = new
            no_chg = 0
        else:
            no_chg += 1
            if no_chg >= 3:
                print(f"  [Done] No new rows.")
                break
    final = get_row_count(driver)
    print(f"  Final: {final} rows ({clicks} clicks)")
    return final

# Extract nationality and position from raw string e.g. "FRAFRAFW" -> ("FRA", "FW")
VALID_POSITIONS = {"FW", "MF", "DF", "GK"}

def parse_extra_info(raw):
    raw = (raw or "").strip()
    if not raw:
        return "", ""
    position = raw[-2:] if len(raw) >= 2 else ""
    nationality = raw[:3] if len(raw) >= 3 else raw
    if position not in VALID_POSITIONS:
        print(f"  [WARN] Unexpected position '{position}' from raw: '{raw}'")
    return nationality, position

# Parse a single player row and return a dict
def parse_player_row(row, columns):
    p = {}
    rank_td = row.find("td", class_=lambda x: x and "rank" in str(x).lower())
    p["Rank"] = rank_td.get_text(strip=True) if rank_td else ""
    name_div = row.find("div", class_="main-text")
    if not name_div:
        return None
    p["Name"] = name_div.get_text(strip=True)
    extra = row.find("div", class_="extra-info-container")
    if extra:
        nat, pos = parse_extra_info(extra.get_text(strip=True))
        p["Nationality"] = nat
        p["Position"] = pos
    else:
        p["Nationality"] = ""
        p["Position"] = ""
    # Skip rows where nationality is missing
    if not p["Nationality"]:
        return None
    vals = [s.get_text(strip=True) for s in row.find_all("span", class_="value")]
    for i, col in enumerate(columns):
        val = vals[i] if i < len(vals) else None
        p[col] = "0" if val in ("-", "", None) else val
    return p

# Parse a single team row and return a dict
def parse_team_row(row, columns):
    t = {}
    rank_td = row.find("td", class_=lambda x: x and "rank" in str(x).lower())
    t["Rank"] = rank_td.get_text(strip=True) if rank_td else ""
    name_div = row.find("div", class_="main-text")
    if not name_div:
        return None
    t["Team"] = name_div.get_text(strip=True)
    vals = [s.get_text(strip=True) for s in row.find_all("span", class_="value")]
    for i, col in enumerate(columns):
        val = vals[i] if i < len(vals) else None
        t[col] = "0" if val in ("-", "", None) else val
    return t

# Parse all rows from HTML using BeautifulSoup
def parse_rows(html, columns, row_parser):
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("tr", class_=lambda x: x and ("row-even" in x or "row-odd" in x))
    out = []
    for row in rows:
        try:
            record = row_parser(row, columns)
            if record:
                out.append(record)
        except Exception as e:
            print(f"[ROW ERROR] {e}")
            continue
    return out

# Save list of dicts to CSV file
def save_csv(data, folder, filename):
    if not data:
        print(f"  [WARN] No data for {filename}, skipping.")
        return
    os.makedirs(folder, exist_ok=True)
    fp = os.path.join(folder, filename)
    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset=["Name"] if "Name" in df.columns else None)
    df.to_csv(fp, index=False, encoding="utf-8-sig")
    print(f"  Saved: {fp} ({len(data)} rows)")

# Open a stats page, loop through all tabs, load all rows and save CSVs
def process_page(driver, url, tabs, out_dir, row_parser, label):
    print(f"\n[{label}] Loading page...")
    driver.get(url)
    time.sleep(8)
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, row_sel))
        )
        print("  Page loaded.")
    except Exception:
        print("  [WARN] Table wait timed out, continuing.")
    for i, tab in enumerate(tabs):
        t0 = time.time()
        print(f"\n  [{i+1}/{len(tabs)}] {tab['name']}")
        if not click_tab(driver, tab["button"]):
            print(f"  [SKIP] Tab click failed.")
            continue
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        load_all_rows(driver)
        data = parse_rows(driver.page_source, tab["columns"], row_parser)
        print(f"  Parsed {len(data)} rows ({time.time()-t0:.0f}s)")
        save_csv(data, out_dir, tab["csv"])

# Print final summary of all saved CSV files
def print_summary():
    print("\nSummary")
    grand_total = 0
    for tabs, folder, label in [
        (player_tabs, player_dir, "Player Stats"),
        (team_tabs, team_dir, "Team Stats"),
    ]:
        print(f"  {label}:")
        for tab in tabs:
            fp = os.path.join(folder, tab["csv"])
            if os.path.exists(fp):
                df = pd.read_csv(fp)
                count = len(df)
                grand_total += count
                nulls = df.isnull().sum().sum()
                status = "OK" if nulls == 0 else f"{nulls} nulls"
                print(f"    {tab['name']:<15} {count:>5} rows  [{status}]")
            else:
                print(f"    {tab['name']:<15} MISSING")
    print(f"\n  Grand Total: {grand_total:,} records across 15 files")

def main():
    print(f"KickCore Analytics - FIFA World Cup 2026")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    os.makedirs(player_dir, exist_ok=True)
    os.makedirs(team_dir, exist_ok=True)
    driver = setup_driver()
    try:
        process_page(driver, player_url, player_tabs, player_dir, parse_player_row, "PLAYER STATS")
        process_page(driver, team_url, team_tabs, team_dir, parse_team_row, "TEAM STATS")
    except Exception as e:
        print(f"\nError: {e}")
        traceback.print_exc()
    finally:
        driver.quit()
    print_summary()
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()