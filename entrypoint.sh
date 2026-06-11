#!/bin/bash
set -e

echo "Starting NUT drivers..."
upsdrvctl -u nut start
sleep 3

echo "Starting upsd..."
upsd -u nut
sleep 2

echo "Starting upsmon..."
upsmon

echo "Handing over to supervisord..."
exec /usr/bin/supervisord -c /etc/supervisord.conf
