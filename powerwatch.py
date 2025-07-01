#!/usr/bin/env python3
import subprocess, time

SENTINELS = ["yandex.ru"]
PING_INTERVAL = 5
MAX_MISSED = 6
UPS_NAME = "fakeups"
UPS_USER = "admin"
UPS_PASS = "adminpass"



print("Powerwatch starting with:")
print(f"  SENTINELS = {SENTINELS}")
print(f"  UPS_NAME = {UPS_NAME}")
print(f"  UPS_USER = {UPS_USER}")
print(f"  UPS_PASS = {'*' * len(UPS_PASS)}")

def ping(host):
    return subprocess.call(["ping", "-c", "1", "-W", "1", host],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) == 0

def set_status(status, charge):
    subprocess.call(["upsrw", "-s", f"ups.status={status}",
                     "-u", UPS_USER, "-p", UPS_PASS, f"{UPS_NAME}@localhost"])
    #subprocess.call(["upsrw", "-s", f"battery.charge={charge}",
    #                 "-u", UPS_USER, "-p", UPS_PASS, f"{UPS_NAME}@localhost"])

def trigger_fsd():
    subprocess.call(["upscmd", "-u", UPS_USER, "-p", UPS_PASS,
                     f"{UPS_NAME}@localhost", "fsd"])

def main():
    misses = 0
    on_battery = False
    while True:
        if any(ping(h) for h in SENTINELS if h.strip()):
            if on_battery:
                print("Power restored. Setting status to OL")
                set_status("OL", 100)
                on_battery = False
            misses = 0
        else:
            misses += 1
            print(f"Missed {misses} pings")
            if not on_battery and misses >= MAX_MISSED:
                print("Triggering OB state")
                set_status("OB", 10)
                trigger_fsd()
                on_battery = True
        time.sleep(PING_INTERVAL)

if __name__ == "__main__":
    main()