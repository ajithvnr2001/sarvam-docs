#!/usr/bin/env python3
"""Coder: incremental update without recrawling (docs.sarvam.ai).
Usage:
  python3 coder_update.py --check-only
  python3 coder_update.py --run --concurrency 10
"""
import argparse, json, re, asyncio, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from guide_code.coder_scrape import scrape
import crawl_sarvam as C

DOCS = pathlib.Path("/data/opencode/sarvam/docs")

async def live():
    import httpx
    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as c:
        r = await c.get("https://docs.sarvam.ai/sitemap.xml")
        r.raise_for_status()
        return sorted({C.normalize_url(u) for u in re.findall(r"<loc>([^<]+)</loc>", r.text) if C.normalize_url(u)})

async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--concurrency", type=int, default=10)
    a = ap.parse_args()
    indexed = {json.loads(l)["url"] for l in open(DOCS / "_index.jsonl")} if (DOCS / "_index.jsonl").exists() else set()
    from urllib.parse import unquote
    idec = {unquote(u) for u in indexed}
    lv = await live()
    new = [u for u in lv if u not in indexed and unquote(u) not in idec and ".json" not in u and "`" not in u]
    print(f"live={len(lv)} indexed={len(indexed)} new={len(new)}")
    for u in new[:20]:
        print(" NEW:", u)
    if a.check_only or not a.run or not new:
        return
    sem = asyncio.Semaphore(a.concurrency)
    idx = open(DOCS / "_index.jsonl", "a")
    async def one(u):
        async with sem:
            md, title, method = await scrape(u)
            rel = C.url_to_relpath(u)
            (DOCS / rel).parent.mkdir(parents=True, exist_ok=True)
            (DOCS / rel).write_text(md)
            idx.write(json.dumps({"url": u, "file": str(rel), "title": title, "method": method}) + "\n")
            print("[ok]", u)
    await asyncio.gather(*(one(u) for u in new))
    idx.close()

if __name__ == "__main__":
    asyncio.run(main())
