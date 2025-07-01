# FakeUPS Docker Setup

This project sets up a simulated UPS server using NUT (Network UPS Tools) inside a Docker container. It includes a watcher script that monitors power status by pinging configured devices and changes the UPS status accordingly. Clients on the network can connect and shut down gracefully based on the reported UPS status.

## Features

* Simulated UPS using `dummy-ups` driver.
* UPS status served over the network on port 3493.
* Python script `powerwatch.py` watches network devices and updates UPS status (`OL`, `OB`, `OB LB`).
* Automatically triggers FSD (Forced Shutdown) if power outage persists.
* Logs in monolog-style format to a mounted directory.
* Works on Raspberry Pi 2 (and maybe another arm).
* Dockerized and easy to deploy.

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
```

### Optional: Sentry Support

`powerwatch.py` attempts to import and initialize Sentry if the SDK is installed. You can add your Sentry DSN in the `sentry_sdk.init()` call.

## Security Note

Only password-protected local access is enabled by default. The container does **not** SSH into other devices to shut them down. This is intentional to avoid storing secrets inside the container.

## License

MIT License
