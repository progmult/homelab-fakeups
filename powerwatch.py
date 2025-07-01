#!/usr/bin/env python3
import subprocess, time, logging
from datetime import datetime
# ==== Settings ====
SENTINELS = ["yandex.ru"]
PING_INTERVAL = 5
MAX_MISSED_WARN = 6
MAX_MISSED_CRIT = 30
UPS_NAME = "fakeups"
UPS_USER = "admin"
UPS_PASS = "adminpass"

# Setup logging
logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S',
        handlers=[logging.FileHandler("/var/log/nut/powerwatch.log"), logging.StreamHandler()]
        )

try:
    import sentry_sdk
    sentry_sdk.init(dsn="", traces_sample_rate=1.0)  # Fill in DSN if needed
except ImportError:
    pass

def ping(host):
    return subprocess.call(["ping", "-c", "1", "-W", "1", host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL) == 0

def set_status(status):
    subprocess.call([
        "upsrw", "-s", f"ups.status={status}",
        "-u", UPS_USER, "-p", UPS_PASS,
        f"{UPS_NAME}@localhost"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0)

def trigger_fsd():
    # raises error, commented
    subprocess.call([
        "upscmd", "-u", UPS_USER, "-p", UPS_PASS,
        f"{UPS_NAME}@localhost", "fsd"
        ])

def main():
    misses = 0
    on_battery = False

    while True:
        if any(ping(h) for h in SENTINELS):
            if on_battery:
                logging.info("Power restored")
                set_status("OL")
                on_battery = False
            misses = 0
        else:
            misses += 1
            if misses == MAX_MISSED_WARN:
                logging.warning("Power lost - switching to OB")
                set_status("OB")
                on_battery = True
            elif misses == MAX_MISSED_CRIT:
                logging.critical("Battery critically low - switching to OB LB")
                set_status("OB LB")
                #trigger_fsd()
                break
        time.sleep(PING_INTERVAL)

if __name__ == "__main__":
    main()