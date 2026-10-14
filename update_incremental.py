#!/usr/bin/env python3
"""Incremental update for docs.sarvam.ai: crawl NEW docs AND refetch
sitemap-updated pages (lastmod vs fetched_at, newest-first, capped).
Usage:
  python3 update_incremental.py --check-only
  python3 update_incremental.py
  python3 update_incremental.py --force URL
"""
import argparse, json, os, re, pathlib, asyncio, sys
from urllib.parse import urlparse, urljoin, urldefrag
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import crawl_sarvam as C

DOCS = C.OUT_ROOT
STATE = C.STATE_FILE
REFRESH_CAP = 100  # max stale-page refetches per run (newest first)

# Sitemap URLs whose origin is broken (verified by hand): excluded from auto-update
# so the daily Action doesn't re-add an error page every run.
KNOWN_BROKEN = {
    # serves Next.js "This page couldn't load" (was HTTP 500 at crawl time)
    "https://docs.sarvam.ai/ms-agent-harness-dotnet/tutorials/ai-powered-textarea/step-2-setup-copilotkit/",
}

async def live_sitemaps():
    import httpx
    out, lastmod = {}, {}
    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as c:
        r = await c.get("https://docs.sarvam.ai/sitemap.xml", timeout=30); r.raise_for_status()
        locs = re.findall(r"<loc>([^<]+)</loc>", r.text)
        out["docs"] = sorted({C.normalize_url(u) for u in locs if C.normalize_url(u)})
        for u, d in re.findall(r"<loc>([^<]+)</loc><lastmod>([^<]+)</lastmod>", r.text):
            n = C.normalize_url(u)
            if n and (n not in lastmod or d > lastmod[n]): lastmod[n] = d
    return out, lastmod

async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--force", default=None)
    ap.add_argument("--concurrency", type=int, default=10)
    a = ap.parse_args()
    idx = [json.loads(l) for l in open(DOCS / "_index.jsonl")] if (DOCS / "_index.jsonl").exists() else []
    indexed = set(r["url"] for r in idx)
    from urllib.parse import unquote
    idec = {unquote(u) for u in indexed}
    live, lastmod = await live_sitemaps()
    new = {}
    for k, urls in live.items():
        miss = [u for u in urls if u not in indexed and unquote(u) not in idec and ".json" not in u and "`" not in u and u not in KNOWN_BROKEN]
        new[k] = miss
        print(f"{k}: live={len(urls)} indexed~{len(indexed)} new={len(miss)}")
        for u in miss[:20]: print(f"  NEW: {u}")
    total_new = sum(len(v) for v in new.values())
    # stale: sitemap lastmod newer than our _meta fetched_at (newest first, capped)
    stale = []
    if lastmod:
        for mfile in (DOCS / "_meta").rglob("*.json"):
            try:
                m = json.loads(mfile.read_text())
            except Exception:
                continue
            u, fa = m.get("url"), m.get("fetched_at")
            d = lastmod.get(u) if u else None
            if not u or not fa or not d:
                continue
            if u in set(sum(new.values(), [])) or u in KNOWN_BROKEN:
                continue
            try:
                from datetime import datetime as _dt
                if _dt.fromisoformat(d.replace("Z", "+00:00")) > _dt.fromisoformat(fa):
                    stale.append((d, u))
            except Exception:
                pass
    stale.sort(reverse=True)
    refresh = [u for _, u in stale[:REFRESH_CAP]]
    print(f"stale: {len(stale)}, refreshing newest {len(refresh)}")
    targets = [a.force] if a.force else [u for v in new.values() for u in v] + refresh
    refresh_urls = set(refresh)
    if not a.check_only:
        # daily verification stamp (committed even when nothing new)
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        stamp = {"date": now.strftime("%F"), "at": now.isoformat(),
                 "new": {k: len(v) for k, v in new.items()},
                 "refreshed": len(refresh), "stale_total": len(stale),
                 "total_index": len(indexed) + (1 if a.force else 0)}
        (DOCS / "_last_verified.json").write_text(json.dumps(stamp, indent=2))
        try:
            mp = DOCS / "_manifest.json"
            m = json.loads(mp.read_text()) if mp.exists() else {}
            m["last_verified"] = stamp["date"]
            m["generated_at"] = stamp["at"]
            mp.write_text(json.dumps(m, indent=2))
        except Exception as e:
            print("stamp manifest skip:", e)
        try:  # keep README verification date fresh (committed by Actions)
            for _rp in [C.REPO_ROOT / "README.md", C.REPO_ROOT / "guide_code" / "README.md"]:
                if _rp.exists():
                    _t = _rp.read_text()
                    _t2 = re.sub(r"Last verified: \d{4}-\d{2}-\d{2}", f"Last verified: {stamp['date']}", _t)
                    _t2 = re.sub(r"## Results \(verified \d{4}-\d{2}-\d{2}\)", f"## Results (verified {stamp['date']})", _t2)
                    if _t2 != _t:
                        _rp.write_text(_t2)
                        print(f"readme date -> {stamp['date']} ({_rp})")
        except Exception as e:
            print("readme stamp skip:", e)
        print(f"stamped {stamp['date']} (new={total_new} refresh={len(refresh)})")
    if a.check_only or not targets:
        print("check-only" if a.check_only else "no new docs — up to date")
        return
    print(f"fetching {len(targets)} docs ({total_new} new + {len(refresh)} refresh)...")
    st = json.load(open(STATE)) if STATE.exists() else {"visited": {}, "failed": {}}
    vs, failed = st.get("visited", {}), st.get("failed", {})
    from datetime import datetime, timezone
    lines = [json.loads(l) for l in open(DOCS / "_index.jsonl")] if (DOCS / "_index.jsonl").exists() else []
    if len({r["url"] for r in lines}) != len(lines):  # drop dupes from legacy appends
        seen, ded = set(), []
        for r in reversed(lines):
            if r["url"] not in seen:
                seen.add(r["url"]); ded.append(r)
        lines = list(reversed(ded))
    pos = {r["url"]: i for i, r in enumerate(lines)}
    sem = asyncio.Semaphore(a.concurrency)
    ok = fail = 0
    async def one(url):
        nonlocal ok, fail
        async with sem:
            try:
                data = await C.fetch_one(url)
                rel = C.url_to_relpath(url); fp = DOCS / rel
                fp.parent.mkdir(parents=True, exist_ok=True)
                fm = f"---\nurl: {url}\ntitle: {json.dumps(data['title'])[1:-1]}\nmethod: {data['method']}\nfetched_at: {datetime.now(timezone.utc).isoformat()}\n---\n\n"
                fp.write_text(fm + data["markdown"], encoding="utf-8")
                mr = pathlib.Path("_meta") / rel.with_suffix(".json")
                (DOCS / mr).parent.mkdir(parents=True, exist_ok=True)
                (DOCS / mr).write_text(json.dumps({"url": url, "file": str(rel), "title": data["title"], "method": data["method"], "fetched_at": datetime.now(timezone.utc).isoformat()}, indent=2))
                vs[url] = {"file": str(rel), "title": data["title"], "method": data["method"]}
                row = {"url": url, "file": str(rel), "title": data["title"], "method": data["method"]}
                if url in pos:
                    lines[pos[url]] = row
                    print(f"[refresh] {url}")
                else:
                    pos[url] = len(lines); lines.append(row)
                    print(f"[new] {url}")
                ok += 1
            except Exception as e:
                failed[url] = str(e)[:300]; fail += 1; print(f"[fail] {url}: {e}")
    await asyncio.gather(*(one(u) for u in targets))
    (DOCS / "_index.jsonl").write_text("".join(json.dumps(r) + "\n" for r in lines))
    try:
        if C._crawler is not None: await C._crawler.close()
    except Exception: pass
    open(STATE, "w").write(json.dumps({"visited": vs, "failed": failed}))
    print(f"done: ok={ok} fail={fail}")

if __name__ == "__main__":
    asyncio.run(main())
