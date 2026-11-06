#!/usr/bin/env python3
"""
Automated Scheduled Healthcare Campaign Runner
Schedules and dispatches the 50 healthcare emails across 3 staggered batches during Nairobi business hours:
- Batch 1 (08:30 AM EAT): Targets 01 - 15 (Nairobi Dental & Med-Spas)
- Batch 2 (11:30 AM EAT): Targets 16 - 30 (Specialists, Hospitals & Coastal Region)
- Batch 3 (02:30 PM EAT): Targets 31 - 50 (Kisumu, Eldoret, Nakuru & Regional Hubs)

Enforces 40-75s anti-spam throttling between each send and full IMAP INBOX.Sent sync.
"""

import datetime
import os
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "../outreach_drafts/healthcare_campaign/scheduled_run.log")

BATCHES = [
    {"batch": 1, "target_time": "08:30", "start_id": "01", "limit": 15, "label": "Batch 1: Nairobi Dental & Med-Spas (01-15)"},
    {"batch": 2, "target_time": "11:30", "start_id": "16", "limit": 15, "label": "Batch 2: Specialists & Coastal Region (16-30)"},
    {"batch": 3, "target_time": "14:30", "start_id": "31", "limit": 20, "label": "Batch 3: Western, Eldoret, Nakuru & Central (31-50)"}
]

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    sys.stdout.flush()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def get_seconds_until(target_time_str):
    now = datetime.datetime.now()
    target_hour, target_minute = map(int, target_time_str.split(":"))
    target = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
    
    if target <= now:
        # If target time is past, schedule for today if within a 30m window, else return 0 (run immediately)
        diff = (now - target).total_seconds()
        if diff < 1800:
            return 0
        return 0
    return (target - now).total_seconds()

def run_batch(batch_info):
    log(f"Starting execution of {batch_info['label']}...")
    cmd = [
        sys.executable,
        os.path.join(SCRIPT_DIR, "dispatch_healthcare_campaign.py"),
        "--start-from", batch_info["start_id"],
        "--limit", str(batch_info["limit"]),
        "--delay-min", "40",
        "--delay-max", "75"
    ]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in proc.stdout:
            log("  [DISPATCH] " + line.strip())
        proc.wait()
        log(f"Completed {batch_info['label']} with exit code {proc.returncode}.")
    except Exception as e:
        log(f"Error running {batch_info['label']}: {e}")

def main():
    log("Scheduled Campaign Runner Initialized.")
    log(f"Current local time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    for b in BATCHES:
        sec = get_seconds_until(b["target_time"])
        if sec > 0:
            hours = int(sec // 3600)
            mins = int((sec % 3600) // 60)
            log(f"Waiting for {b['label']} scheduled at {b['target_time']} EAT ({hours}h {mins}m from now)...")
            time.sleep(sec)
        
        run_batch(b)
        log(f"Resting after {b['label']}...")

    log("All 3 scheduled batches completed successfully!")

if __name__ == "__main__":
    main()

