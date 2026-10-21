#!/bin/bash
# boot-all.sh — runs on every boot (root crontab @reboot + cloud-init on reprovision).
# Waits for /data, then restores systemd units for the VM-managed sites.
for i in $(seq 1 60); do
  [ -d /data/opencode ] && break
  sleep 5
done
[ -d /data/opencode ] || { echo "FATAL: /data not mounted"; exit 1; }
for b in /data/opencode/gcpdocs/boot.sh /data/opencode/sarvam/boot.sh /data/opencode/canva/boot.sh; do
  echo "== $(date -u +%FT%TZ) running $b"
  bash "$b" || echo "WARN: $b failed"
done
echo "== $(date -u +%FT%TZ) boot-all done"
