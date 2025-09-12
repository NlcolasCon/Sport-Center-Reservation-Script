# scheduler.py
import time, subprocess, datetime as dt
# Allowed days: Mon=1 .. Sun=7; skip Tue(2)
ALLOWED = {1,3,4,5,6,7}

def should_run_now():
    now = dt.datetime.now()
    return (now.isoweekday() in ALLOWED) and (now.hour == 8 and now.minute == 0)

while True:
    if should_run_now():
        try:
            subprocess.run(
                ["python3", "reserve.py"],
                cwd=None,  # current dir
                check=False
            )
        except Exception as e:
            print("Run failed:", e)
        time.sleep(61)  # avoid double-runs in the same minute
    else:
        time.sleep(5)
