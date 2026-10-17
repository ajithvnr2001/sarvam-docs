# GUIDE — docs.sarvam.ai: full redo + incremental updates (end to end)

Everything below executed as written (1,090 pages saved: 533/533 sitemap + 501 subdomain pages + mirrors). Redo from scratch via §2; keep-up-to-date via §3.

## 0. Architecture

```
crawl_sarvam.py        → docs/            (resume-safe crawl: sitemap + llms.txt + subdomains)
update_incremental.py  → incremental pass (new + lastmod-stale only)
sarvam-crawl.service   → systemd, Restart=on-failure
sarvam-update.timer    → daily 06:30 UTC incremental (VM-side; no GitHub Actions per project decision)
```

Stack: **Scrapling → Crawl4AI → ScrapeGraphAI → httpx** fallback chain (same `fetch_one` pattern as every repo in this family); docs saved as frontmatter `.md` + `_meta/*.json` + `_index.jsonl` + `_manifest.json`; state in `crawl_state.json`.

## 1. Setup

```bash
pip3 install -r requirements.txt
python3 -m playwright install chromium
# tools/: symlinked shared clones of scrapegraph-ai / crawl4AI / scrapling (patched), see ai-docs GUIDE §1
```

## 2. Full redo

```bash
python3 crawl_sarvam.py --concurrency 10        # rerun-safe: visited set skipped
python3 update_incremental.py --check-only      # expect new=0 when complete
find docs -name '*.md' | wc -l                  # ~1,090
```

- `docs/_subdomains/<host>/` holds the subdomain pages; login-walled hosts are recorded as failed, never dropped silently.
- Keep `_llms/` snapshot: `docs/_llms/docs.sarvam.ai_llms.txt` (llms.txt changes are a seed source).

## 3. Incremental updates

```bash
python3 update_incremental.py --check-only      # diff only
python3 update_incremental.py --force URL       # refetch one page
python3 update_incremental.py --concurrency 10  # full pass (new URLs + newest-first stale refresh, cap 100)
```

Automation on the VM (installed by `boot.sh`):

```bash
systemctl enable --now sarvam-update.timer      # daily 06:30 UTC, Persistent=true
systemctl list-timers sarvam-update.timer
journalctl -u sarvam-update.service -n 50
```

The updater stamps `docs/_last_verified.json` and rewrites `Last verified:` in `README.md` on every run — commit any changed files to git afterwards (`git add docs/ README.md && git commit -m "daily update" && git push`), or wire commit+push into a wrapper if you want it fully hands-off.

## 4. Redo from zero on a new VM (disaster recovery)

1. Attach `/data` disk (has all state; `boot.sh` exists there).
2. `bash /data/opencode/sarvam/boot.sh` — reinstalls units, enables timer, starts crawl if not already running.
3. Fresh VM template: attach `cloud-init.yaml` as custom-data — first boot runs `boot.sh` automatically.

## 5. Troubleshooting

| Symptom | Fix |
|---|---|
| updater keeps adding the same broken page | add the URL to `KNOWN_BROKEN` in `update_incremental.py` (verified-broken origin). |
| crawl_sarvam + update_incremental race | updater locks nothing — run when crawl is idle (timer is already scheduled off-peak); or stop `sarvam-crawl.service` first. |
| scrapegraphai ImportError | patched clone in `tools/`; don't pip-install raw 1.36.0 for markdown conversion. |
