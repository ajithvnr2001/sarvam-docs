#!/bin/bash
# boot.sh — reinstall + start the Sarvam crawler after a spot-VM reallocation.
# Lives on /data (survives). Idempotent: safe to run any time.
set -e
UNIT_SRC="/data/opencode/sarvam/sarvam-crawl.service"
UNIT_DST="/etc/systemd/system/sarvam-crawl.service"

if [ ! -f "$UNIT_SRC" ]; then
  echo "FATAL: $UNIT_SRC missing (/data not attached?)" >&2
  exit 1
fi
cp -f "$UNIT_SRC" "$UNIT_DST"
systemctl daemon-reload
systemctl enable sarvam-crawl.service
if ! systemctl is-active --quiet sarvam-crawl.service; then
  if pgrep -f "crawl_sarvam.py" >/dev/null; then
    echo "crawl_sarvam.py already running — service enabled for future boots, not starting a duplicate."
  else
    systemctl start sarvam-crawl.service
    echo "sarvam-crawl.service started."
  fi
else
  echo "sarvam-crawl.service already active."
fi
systemctl is-enabled sarvam-crawl.service
