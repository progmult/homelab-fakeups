# FakeUPS: Virtual UPS for Home Infrastructure

Emulates a UPS (Uninterruptible Power Supply) using [Network UPS Tools](https://github.com/networkupstools/nut) (NUT) for setups where clients are powered by a UPS without USB — triggers safe shutdowns by monitoring network power-dependent device availability.

It helps enables devices on your network to respond properly to power outages.

## About 

### How It Works

- Pings power-dependent devices on the local network (e.g. router, server without UPS);

- If those devices become unreachable, it simulates a power failure by setting the [Dummy UPS](https://networkupstools.org/docs/man/dummy-ups.html) status to OB (on battery) or OB LB (low battery);

- Once devices are reachable again, it restores the status to OL (online).

### Why Use It

✅ Notifies QNAP, Synology, ESXi, and other clients about power events;

✅ Allows clients to shutdown safely or enter a low-power state;

✅ No need to store passwords or SSH credentials;

✅ Runs as a Docker container on Raspberry Pi or any Linux host.

### When to Use
FakeUPS is ideal if you have multiple devices connected to a single physical UPS **without USB interface**, and you need centralized power status management across your network.

### Architecture

* Simulated UPS using `dummy-ups` driver;
* UPS status served over the network on port 3493;
* Python script `powerwatch.py` watches network devices and updates UPS status (`OL`, `OB`, `OB LB`);
* Logs in monolog-style format to a mounted directory;

## Usage

### Requirements

* Docker
* docker-compose

### Build and Run

```bash
docker-compose up --build -d
```
This will build the container and run it in the background.

### Folder Structure

```
project/
├── Dockerfile
├── docker-compose.yml
├── powerwatch.py
├── nut/
│   ├── ups.conf
│   ├── nut.conf
│   ├── upsd.conf
│   ├── upsmon.conf
│   └── upsd.users
├── supervisord.conf
└── logs/         # log output is mounted here
```

### Configuration

Edit `nut/ups.conf` to change UPS name or type.

Edit `powerwatch.py` to change which devices to ping:

```python
SENTINELS = ["192.168.1.50"]  # Add more IPs if needed
```

### Logs

Logs are saved in `logs/powerwatch.log` and follow this format:

```
[2025-07-01T12:00:00] INFO: Power restored
[2025-07-01T12:05:30] WARNING: Power lost - switching to OB
[2025-07-01T12:15:00] CRITICAL: Battery critically low - switching to OB LB
```

You can mount `logs/` anywhere you want for external log aggregation or backup.

### Network Clients

Clients on your LAN can connect to the container at port 3493 and use `upsmon`, `upsc` etc. to monitor the UPS:

```bash
upsc fakeups@<docker-host-ip>
upsc qnapups@<docker-host-ip> #special virtual ups for qnap
```

### Optional: Sentry Support

`powerwatch.py` attempts to import and initialize Sentry if the SDK is installed. You can add your Sentry DSN in the `sentry_sdk.init()` call.

## ⚠️ Important Note
FakeUPS relies on pinging power-dependent network devices to detect power loss. This method does **not** directly monitor electrical power. As a result, false shutdown signals may occur if the monitored device restarts, loses network connectivity, or its IP becomes temporarily unreachable (e.g., due to internet issues or device reboots).

By default, FakeUPS pings `192.168.3.1` and `google.com`. To minimize false positives:

- Choose sentinel devices that are **always on**, **on local network**, and **not protected by a UPS**;

- Alternatively, choose devices that **lose network connectivity when power is lost** (such as a router connected through an unprotected switch).

When performing maintenance or rebooting monitored devices, stop FakeUPS first:

```bash
docker stop fakeups
```

Then start it again after:

```bash
docker start fakeups
```


## License

MIT License
