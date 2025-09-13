# scheduler.py
import time, subprocess, datetime as dt, sys, os

# Mon=1..Sun=7; run Wed→Mon (skip Tue=2)
ALLOWED = {1,3,4,5,6,7}

USERS = [
    {"state": "state_user1.json", "tag": "user1"},
    {"state": "state_user2.json", "tag": "user2"},
]

def should_run_now():
    now = dt.datetime.now()
    return (now.isoweekday() in ALLOWED) and (now.hour == 8 and now.minute == 0)

while True:
    if should_run_now():
        for u in USERS:
            try:
                subprocess.run(
                    ["python", "reserve.py", "--state", u["state"], "--tag", u["tag"], "--headless"],
                    check=False
                )
            except Exception as e:
                print(f"[ERR] {u['tag']} run failed:", e)
        time.sleep(61)   # avoid multiple runs in the same minute
    else:
        time.sleep(5)
