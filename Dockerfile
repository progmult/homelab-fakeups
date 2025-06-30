FROM arm32v7/debian:bullseye-slim

RUN apt-get update && apt-get install -y \
    nut python3 iputils-ping at supervisor && \
    mkdir -p /var/run/nut && \
    useradd -r -s /sbin/nologin nut

COPY powerwatch.py /usr/local/bin/powerwatch.py
COPY nut/ /etc/nut/
COPY supervisord.conf /etc/supervisord.conf

RUN chmod +x /usr/local/bin/powerwatch.py

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
