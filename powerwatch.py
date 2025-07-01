#!/usr/bin/env python3
import subprocess
import time
from datetime import datetime

# ==== Настройки ====
SENTINELS = ["yandex.ru"]
PING_INTERVAL = 5
MAX_MISSED = 6
UPS_NAME = "fakeups"
UPS_USER = "admin"
UPS_PASS = "adminpass"

# ==== Логирование ====
def log(level, message):
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    print(f"{timestamp} {level.upper()}: {message}")

# ==== Пинг утилита ====
def ping(host):
    return subprocess.call(["ping", "-c", "1", "-W", "1", host],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) == 0

# ==== Изменение статуса ====
def set_status(status):
    result = subprocess.run([
        "upsrw", "-s", f"ups.status={status}",
        "-u", UPS_USER, "-p", UPS_PASS, f"{UPS_NAME}@localhost"
    ], capture_output=True, text=True)
    if result.returncode == 0:
        log("info", f"Set status to {status}")
    else:
        log("error", f"Failed to set status: {result.stderr.strip()}")

# ==== Главный цикл ====
def main():
    misses = 0
    power_lost = False

    while True:
        alive = any(ping(host) for host in SENTINELS)

        if alive:
            if power_lost:
                log("notice", "Power restored")
                set_status("OL")
                power_lost = False
            misses = 0
        else:
            misses += 1
            log("warning", f"Missed ping ({misses}/{MAX_MISSED})")
            if not power_lost and misses >= MAX_MISSED:
                log("critical", "Power lost — switching to battery")
                set_status("OB LB")
                power_lost = True

        time.sleep(PING_INTERVAL)

if __name__ == "__main__":
    main()