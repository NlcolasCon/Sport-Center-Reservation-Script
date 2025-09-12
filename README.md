# UCY Gym Auto-Reservation

Automates booking a UCY Sports Center slot at **20:15** for the day **5 days ahead**.  
Runs with **Playwright** and can be scheduled to fire at **08:00**, Wednesday → Monday.

> Educational use only. Respect the Sports Center's rules and booking policies.

## Features
- One-time login saved to `state.json` (cookies/session)
- Clicks through Reservations → Gymnastic → Agree → picks target day (+5) → selects **20:15** → writes purpose **`g`** → submits
- Headless-friendly (works on WSL); screenshots saved in `runs/`
- Can change code to change time slot, purpose of reservation and hit time

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

### 1) Save login state (one-time)
```bash
python save_state.py
# A Chromium window will open — login and reach Reservations page, then press ENTER in the terminal.
# This creates state.json (already in .gitignore).
```

### 2) Test a reservation run
```bash
python reserve.py
```
- Successful runs: a screenshot is saved in `runs/success_*.png`.

## Scheduling

See **[docs/SCHEDULING.md](docs/SCHEDULING.md)** for:
- Windows Task Scheduler (recommended)
- Cron (Linux)
- Self-scheduler loop (`scheduler.py`)

## Repo layout
```
ucy-gym-reserver/
├─ reserve.py          # main booking script
├─ save_state.py       # one-time login to create state.json
├─ scheduler.py        # optional self-scheduler that runs reserve.py at 08:00
├─ requirements.txt
├─ .gitignore
├─ LICENSE
├─ docs/
│  ├─ SCHEDULING.md
│  └─ TROUBLESHOOTING.md
└─ tasks/
   ├─ windows_task_wsl.xml       # importable Task for WSL Python
   └─ windows_task_python.xml    # importable Task for native Windows Python
```

## Notes
- `state.json` and `runs/` are ignored from git for privacy and cleanliness.
- If UCY logs you out periodically, just run `python save_state.py` again to refresh cookies.
