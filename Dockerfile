# Dockerfile for Raspberry Pi (ARMv7) with NUT + dummy-ups + powerwatch
# Dockerfile
FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y \
    nut \
    python3 \
    iputils-ping \
    at \
    supervisor

RUN apt-get install -y \
    mc \
    nano \
    procps

RUN mkdir -p /var/run/nut /var/log/nut && \
    useradd -r -s /sbin/nologin nut || true

COPY nut /etc/nut/
COPY powerwatch.py /usr/local/bin/powerwatch.py
COPY supervisord.conf /etc/supervisord.conf

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
