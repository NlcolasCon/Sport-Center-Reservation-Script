# Sport Center Reservation Script

Automates booking a Sport Center Reservation. Built with **Python** + **Playwright**, it supports multiple users, customizable reservation hours, daily scheduling, session persistence, and logging with screenshots.

> Educational use only. Respect the Sports Center's rules and booking policies.

## Features
- **Automatic reservations** with customizable time slots per day
- **Multi-user support** (add as many users as you want with their own session state)
- **Session persistence** (`.json` state files with cookies/tokens)
- **Daily scheduler** (runs every morning at 08:00, skipping Tuesdays by default, can customise)
- **Robust navigation** (fallback locators if defaults fail)
- **Screenshots & logs** for every run
- **Headless mode** (for unattended automation)

## Quickstart

```bash
# 1) create & activate venv (Windows PowerShell)
py -m venv .venv
.venv\Scripts\activate

# or Linux/WSL
python3 -m venv .venv
source .venv/bin/activate

# 2) install deps
pip install -r requirements.txt
playwright install chromium
```

### 1) Save login state (one-time per user)
- Run once to log in manually:
```bash
python save_state.py --state state_user1.json
python save_state.py --state state_user2.json
# A Chromium window will open — login and reach Reservations page, then press ENTER in the terminal.
# This creates state.json with saved cookies in them (already in .gitignore).
```

### 2) Test a reservation run
```bash
python reserve.py --state state_user1.json --tag user1 --headless
```
This will:
- Open the Sports Center site
- Navigate to Reservations → Gymnastic
- Pick target date (today + 5 days)
- Select the correct time for today (see below)
- Confirm and save a screenshot

## Scheduling
- Self-scheduler loop
```bash
python scheduler.py
```
- Checks every 5 seconds whether it’s time to run.
- At 08:00 (except Tuesday) → launches reserve.py for each user.
- Sleeps 61 seconds to avoid duplicate runs in the same minute.

## Repo layout
```
Sport-Center-Reservation-Script/
├─ scheduler.py          # Orchestrates daily runs for multiple users
├─ reserve.py            # Main reservation logic (navigates and books)
├─ save_state.py         # Helper: log in once manually and save session
├─ requirements.txt      # Dependencies (Playwright, dotenv)
├─ .gitignore
├─ LICENSE
├─ readme.md
└─ runs/                 # Logs & screenshots per user
```

## Reservation times
- The reservation time is customizable in reserve.py inside desired_time_for_today().
- By default:
```
Monday → 12:15
Friday → 09:30
Sunday → 16:45
All other days → 20:15
```
- To change these, simply edit the function in reserve.py to return your preferred times.

## Multi-user support
- Add as many users as needed in the USERS list inside scheduler.py:
```bash
USERS = [
    {"state": "state_user1.json", "tag": "user1"},
    {"state": "state_user2.json", "tag": "user2"},
    # Add more users here
]
```

## Logs & Screenshots
- On success:
```
runs/<tag>/<tag>_success_YYYYMMDD_HHMMSS.png
```
- On failure:
```
runs/<tag>/<tag>_error_YYYYMMDD_HHMMSS.png
```
- and a text log <tag>_last_error.txt
- Each user requires their own saved session file (save_state.py).

## Configuration
- Allowed days: configured in scheduler.py
- ALLOWED = {1,3,4,5,6,7}  # Mon=1 .. Sun=7 (Tuesday skipped)
- Reservation hours: customizable in reserve.py → desired_time_for_today()
- Users: customizable in scheduler.py → USERS

## Tech Stack
- Python 3.9+
- Playwright (browser automation)
- Chromium (headless browser)

## Author
- Developed by Nicolas Constantinou — 2025

## Notes
- `state.json` and `runs/` are ignored from git for privacy and cleanliness.
- If the sport center logs you out periodically, just run `python save_state.py --state state_user1.json` again to refresh cookies.
