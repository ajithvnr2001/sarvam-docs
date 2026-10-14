# Sarvam AI Docs — End-to-End Crawler

Crawls **https://docs.sarvam.ai/** completely (533 sitemap URLs + linked Sarvam domains: status/indus/main site where reachable) and saves clean markdown docs. Three stacks: **Scrapling** → **Crawl4AI** → **ScrapeGraphAI** (local, no LLM key).

## Install

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

## Run (resume-safe — re-run to resume)

```bash
python3 crawl_sarvam.py --max-pages 8000 --concurrency 15
python3 update_incremental.py --check-only   # new URLs only, never recrawls
python3 update_incremental.py
```

## Layout

```
crawl_sarvam.py  update_incremental.py  requirements.txt
guide_code/      # coder guide + coder_scrape.py / coder_update.py
sarvam-crawl.service  boot.sh  cloud-init.yaml   # spot-VM boot resilience
docs/            # output: <area>/<path>.md + _meta/ + _index.jsonl + _manifest.json
```

## Notes

- Fern platform: every page also serves clean Markdown at `<url>.md`; per-section index at `<section>/llms.txt`.
- Login-walled (dashboard) and invite-walled (discord) links recorded as failed, not silently dropped.
