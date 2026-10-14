# Guide: scrape + update Sarvam docs (coder end-to-end)

Base: `/data/opencode/sarvam/` · Target: `https://docs.sarvam.ai/` (533 sitemap URLs + linked Sarvam domains)

## 1. Scrape one page (all 3 libs)

```bash
python3 guide_code/coder_scrape.py https://docs.sarvam.ai/api/getting-started/quickstart /tmp/q.md
```

Flow (`coder_scrape.py`): `Fetcher.get(stealthy_headers=True)` → keep `<main>/<article>` → `scrapegraph-ai/utils/convert_to_md.py::convert_to_md` → fallback `AsyncWebCrawler(CacheMode.BYPASS)`. Tip: appending `.md` to any docs URL also returns clean Markdown (Fern native).

## 2. Full crawl

```bash
python3 crawl_sarvam.py --max-pages 8000 --concurrency 15
```

Seeds = `sitemap.xml` (533) + `llms.txt`/`llms-full.txt` links; `normalize_url()` allows `*.sarvam.ai` + `sarvam.ai`, skips binary/`.json`/backtick; saves `docs/<path>.md` + `_meta/*.json`, appends `_index.jsonl`. Subdomain/linked-domain pages go to `docs/_subdomains/<host>/` (status.sarvam.ai, sarvam.ai, indus.sarvam.ai where reachable; dashboard/discord login-walled, recorded as failed).

## 3. Update without recrawling

```bash
python3 update_incremental.py --check-only
python3 update_incremental.py
python3 guide_code/coder_update.py --check-only
python3 guide_code/coder_update.py --run --concurrency 10
```

## 4. Verify

```bash
python3 update_incremental.py --check-only   # expect new=0
find docs -name '*.md' | wc -l
cat docs/_manifest.json
```

## 5. Surviving VM restarts

- `sarvam-crawl.service` (systemd, `Restart=always`) + `boot.sh` + `cloud-init.yaml` — same pattern as the GCP box: power returns → service starts → crawl resumes from `crawl_state.json` (skips existing files).
- One-time: attach `cloud-init.yaml` as custom-data if the VM is ever deleted/recreated (eviction-deallocate needs nothing).

## Tools

- D4Vinci/Scrapling, unclecode/crawl4AI, ScrapeGraphAI/Scrapegraph-ai (`tools/`, symlinked shared clones; pip fallback in resolver).
