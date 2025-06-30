# Dockerfile for Raspberry Pi (ARMv7) with NUT + dummy-ups + powerwatch
FROM arm32v7/debian:bullseye-slim

RUN apt-get update && apt-get install -y \
    nut \
    python3 \
    iputils-ping \
    at \
    supervisor

COPY nut/ /etc/nut/
COPY powerwatch.py /usr/local/bin/powerwatch.py
COPY supervisord.conf /etc/supervisord.conf

RUN echo "MODE=netserver" > /etc/nut/nut.conf \
 && chmod 640 /etc/nut/upsd.users \
 && chown root:nut /etc/nut/upsd.users \
 && chmod +x /usr/local/bin/powerwatch.py

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]