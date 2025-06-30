#!/usr/bin/env python3
import subprocess, time

SENTINELS = ["192.168.1.50"]    # IP устройств без ИБП
PING_INTERVAL = 5
MAX_MISSED = 6
UPS_NAME = "fakeups"
UPS_USER = "admin"
UPS_PASS = "adminpass"

def ping(host):
    return subprocess.call(["ping", "-c", "1", "-W", "1", host],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) == 0

def set_status(status, charge):
    subprocess.call(["upsrw", "-s", f"ups.status={status}",
                     "-u", UPS_USER, "-p", UPS_PASS, f"{UPS_NAME}@localhost"])
    subprocess.call(["upsrw", "-s", f"battery.charge={charge}",
                     "-u", UPS_USER, "-p", UPS_PASS, f"{UPS_NAME}@localhost"])

def trigger_fsd():
    subprocess.call(["upscmd", "-u", UPS_USER, "-p", UPS_PASS,
                     f"{UPS_NAME}@localhost", "fsd"])

def main():
    misses = 0
    while True:
        if any(ping(h) for h in SENTINELS):
            misses = 0
            set_status("OL", 100)
        else:
            misses += 1
            if misses >= MAX_MISSED:
                set_status("OB", 10)
                trigger_fsd()
                break
        time.sleep(PING_INTERVAL)

if __name__ == "__main__":
    main()
