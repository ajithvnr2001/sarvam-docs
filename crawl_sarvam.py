#!/usr/bin/env python3
"""
End-to-end crawler for https://docs.sarvam.ai/ including subdomains.
Uses all three requested stacks:
  1. Scrapling (D4Vinci/Scrapling)  - fast static fetch + CSS/XPath extraction (primary)
  2. Crawl4AI (unclecode/crawl4AI)   - JS rendering fallback + markdown generation
  3. ScrapeGraphAI (ScrapeGraphAI/Scrapegraph-ai) - cleanup_html + convert_to_md (HTML->MD)

Saves markdown docs to /data/opencode/sarvam/docs
"""
import asyncio
import os
import re
import json
import time
import hashlib
import importlib.util
from pathlib import Path
from urllib.parse import urlparse, urljoin, urldefrag, unquote
from datetime import datetime, timezone

import httpx
from bs4 import BeautifulSoup

# ---------- paths (repo-relative so GitHub Actions runners work; override via env) ----------
REPO_ROOT = Path(__file__).resolve().parent
BASE_URL = "https://docs.sarvam.ai"
SITEMAP_INDEX = "https://docs.sarvam.ai/sitemap.xml"
MAIN_LLMS = "https://docs.sarvam.ai/llms.txt"
FULL_LLMS = "https://docs.sarvam.ai/llms-full.txt"
OUT_ROOT = Path(os.environ.get("DOCS_OUT", str(REPO_ROOT / "docs")))
TOOLS_ROOT = Path(os.environ.get("TOOLS_DIR", str(REPO_ROOT / "tools")))
STATE_FILE = Path(os.environ.get("CRAWL_STATE", str(REPO_ROOT / "crawl_state.json")))
INDEX_FILE = OUT_ROOT / "_index.jsonl"
MANIFEST_FILE = OUT_ROOT / "_manifest.json"

OUT_ROOT.mkdir(parents=True, exist_ok=True)
(OUT_ROOT / "_subdomains").mkdir(exist_ok=True, parents=True)
(OUT_ROOT / "_llms").mkdir(exist_ok=True, parents=True)
(OUT_ROOT / "_meta").mkdir(exist_ok=True, parents=True)

# ---------- load ScrapeGraphAI utils directly from cloned repo (bypass broken langchain imports) ----------
def load_module_from_file(name, filepath):
    spec = importlib.util.spec_from_file_location(name, filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def _resolve_sg_utils():
    cands = [
        TOOLS_ROOT / "scrapegraph-ai" / "scrapegraphai" / "utils",
        REPO_ROOT / "tools" / "scrapegraph-ai" / "scrapegraphai" / "utils",
        Path("/data/opencode/cloudflare/tools/scrapegraph-ai/scrapegraphai/utils"),
    ]
    for c in cands:
        if (c / "convert_to_md.py").exists():
            return c
    try:  # pip-installed package fallback (utils files are langchain-free)
        import scrapegraphai
        c = Path(scrapegraphai.__file__).parent / "utils"
        if (c / "convert_to_md.py").exists():
            return c
    except Exception:
        pass
    return cands[0]

SCRAPEGRAPH_UTILS = _resolve_sg_utils()
convert_to_md_mod = load_module_from_file("sg_convert_to_md", str(SCRAPEGRAPH_UTILS / "convert_to_md.py"))
cleanup_html_mod = load_module_from_file("sg_cleanup_html", str(SCRAPEGRAPH_UTILS / "cleanup_html.py"))
sg_convert_to_md = convert_to_md_mod.convert_to_md
try:
    sg_cleanup_html = cleanup_html_mod.cleanup_html
    print("[scrapegraph-ai] loaded convert_to_md + cleanup_html from", SCRAPEGRAPH_UTILS)
except Exception as e:
    sg_cleanup_html = None
    print("[scrapegraph-ai] cleanup_html unavailable:", e)

# ---------- Scrapling ----------
from scrapling import Fetcher
print("[scrapling] Fetcher loaded:", Fetcher)

# ---------- Crawl4AI (lazy, only for fallback) ----------
_crawler = None
async def get_crawler():
    global _crawler
    if _crawler is None:
        from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode  # noqa
        from crawl4ai.async_webcrawler import BrowserConfig
        browser_cfg = BrowserConfig(headless=True, verbose=False)
        _crawler = AsyncWebCrawler(config=browser_cfg)
        await _crawler.start()
        print("[crawl4ai] AsyncWebCrawler started")
    return _crawler

# ---------- helpers ----------
ALLOWED_ROOT_SUFFIXES = (".sarvam.ai",)
MAIN_HOST = "docs.sarvam.ai"

def normalize_url(u, base=BASE_URL):
    if not u:
        return None
    u = u.strip()
    if u.startswith("#") or u.startswith("mailto:") or u.startswith("tel:") or u.startswith("javascript:") or u.startswith("data:"):
        return None
    abs_u = urljoin(base, u)
    abs_u, _ = urldefrag(abs_u)
    try:
        p = urlparse(abs_u)
    except Exception:
        return None
    if p.scheme not in ("http", "https"):
        return None
    host = p.netloc.lower().split(":")[0]
    if host.endswith(".sarvam.ai") or host in ("sarvam.ai", "www.sarvam.ai"):
        pass
    else:
        return None
    # skip binary assets
    low = p.path.lower()
    for ext in (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico", ".css", ".js", ".woff", ".woff2", ".ttf", ".mp4", ".webm", ".zip", ".pdf"):
        if low.endswith(ext):
            # allow .pdf? skip for now to keep docs focused, but record
            return None
    # canonicalize: map /index.md -> /, /index -> /, *.md (doc source) -> HTML url
    # e.g. /zaraz/history/versions/index.md -> /zaraz/history/versions/
    #      /zaraz/history/versions/index -> /zaraz/history/versions/
    #      /zaraz/history/versions.md -> /zaraz/history/versions/
    path = p.path
    if path.endswith("/index.md"):
        path = path[:-len("/index.md")] + "/"
    elif path.endswith("/index"):
        # be careful: /index as root file vs legit slug ending with -index? only strip exact /index segment
        path = path[:-len("/index")] + "/"
    elif path == "/index.md" or path == "/index":
        path = "/"
    elif path.endswith(".md"):
        # product llms.txt markdown source links: strip .md -> trailing slash
        path = path[:-3]
        if not path.endswith("/"):
            path = path + "/"
    # rebuild canonical url (drop query/fragment for docs; query hashed later only if needed)
    # keep query? docs don't need query; strip to dedupe (except search/page params handled via relpath hash, but we drop here)
    # Preserve query only if it looks like pagination? For now strip query to avoid dupes.
    canon = f"{p.scheme}://{p.netloc}{path}"
    # normalize trailing slash: keep "/" for root, ensure directory urls end with "/"
    # sitemap uses trailing slash, so enforce it for consistency (except files)
    if not canon.endswith("/") and "." not in canon.rsplit("/", 1)[-1]:
        canon = canon + "/"
    return canon

def url_to_relpath(url):
    p = urlparse(url)
    host = p.netloc.lower()
    path = unquote(p.path)
    # strip query for filename, but hash it if meaningful
    query = p.query
    path = path.strip("/")
    # canonical: trailing /index already stripped in normalize, but guard again
    if path.endswith("/index"):
        path = path[:-len("/index")].strip("/")
    if not path:
        fname = "_index"
    else:
        # remove trailing / already, keep hierarchy
        fname = path
    # sanitize each segment
    parts = []
    for seg in fname.split("/"):
        seg = re.sub(r'[<>:"\\|?*\x00-\x1F]', "_", seg).strip()
        if len(seg) > 120:
            seg = seg[:100] + "_" + hashlib.md5(seg.encode()).hexdigest()[:8]
        if seg in ("", ".", ".."):
            seg = "_"
        parts.append(seg)
    rel = "/".join(parts) if parts else "_index"
    if query:
        qh = hashlib.md5(query.encode()).hexdigest()[:8]
        rel = rel + f"__q_{qh}"
    if host == MAIN_HOST:
        return Path(rel + ".md")
    else:
        return Path("_subdomains") / host / (rel + ".md")

def extract_main_content_html(html, base_url):
    """Strip nav/header/footer, keep main article. Fallback to body."""
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()
    # Cloudflare docs use <main id="main-content"> or <article>
    main = soup.find("main") or soup.find("article") or soup.find("div", {"id": "main-content"})
    if main:
        # remove nav/aside inside main that is TOC
        return str(main), soup.title.string.strip() if soup.title and soup.title.string else ""
    # fallback: body
    body = soup.find("body")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    if body:
        return str(body), title
    return html, title

def scrapegraph_markdown(html, url):
    try:
        return sg_convert_to_md(html, url)
    except Exception as e:
        # fallback html2text direct
        import html2text
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.body_width = 0
        return h.handle(html)

# ---------- fetch with Scrapling (sync -> thread) ----------
def scrapling_fetch_sync(url):
    t0 = time.time()
    page = Fetcher.get(url, stealthy_headers=True, follow_redirects=True, timeout=25)
    dt = time.time() - t0
    if page.status != 200:
        raise RuntimeError(f"scrapling status {page.status}")
    html = page.html_content
    if not html or len(html) < 500:
        raise RuntimeError("scrapling empty html")
    # links via css
    links = []
    try:
        for a in page.css("a"):
            href = a.attrib.get("href", "")
            if href:
                links.append(href)
    except Exception:
        pass
    # title
    title = ""
    try:
        t = page.css("title::text")
        if t:
            title = str(t[0]).strip()
    except Exception:
        pass
    if not title:
        try:
            h1 = page.css("h1::text")
            if h1:
                title = str(h1[0]).strip()
        except Exception:
            pass
    # text length check
    try:
        txt = page.text or ""
    except Exception:
        txt = ""
    return {"html": html, "links": links, "title": title, "text_len": len(txt), "elapsed": dt}

async def crawl4ai_fetch(url):
    crawler = await get_crawler()
    from crawl4ai import CrawlerRunConfig, CacheMode
    cfg = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        only_text=False,
        excluded_tags=["nav", "footer", "header", "aside", "script", "style"],
        wait_until="domcontentloaded",
        page_timeout=45000,
    )
    res = await crawler.arun(url=url, config=cfg)
    if not res or not res.success:
        raise RuntimeError(f"crawl4ai failed: {getattr(res, 'error_message', 'unknown')}")
    html = res.html or ""
    md = res.markdown or ""
    # res.links: dict with internal/external
    links = []
    try:
        internal = (res.links or {}).get("internal", []) if isinstance(res.links, dict) else []
        external = (res.links or {}).get("external", []) if isinstance(res.links, dict) else []
        for l in (internal + external):
            href = l.get("href") if isinstance(l, dict) else str(l)
            if href:
                links.append(href)
    except Exception:
        pass
    title = ""
    try:
        if res.metadata and isinstance(res.metadata, dict):
            title = res.metadata.get("title", "") or ""
    except Exception:
        pass
    return {"html": html, "markdown": md, "links": links, "title": title}

async def fetch_one(url):
    """Try Scrapling -> Crawl4AI -> httpx. Returns dict with markdown, html, title, links, method."""
    # 1) Scrapling
    try:
        r = await asyncio.to_thread(scrapling_fetch_sync, url)
        html = r["html"]
        main_html, parsed_title = extract_main_content_html(html, url)
        title = r["title"] or parsed_title or url
        md_body = scrapegraph_markdown(main_html, url)
        header = f"# {title}\n\n> Source: {url}\n\n"
        md = header + md_body
        if len(md.strip()) < 800:
            raise RuntimeError(f"scrapling thin content ({len(md)} chars), fallback to crawl4ai")
        return {"url": url, "title": title, "html": html, "markdown": md, "links": r["links"], "method": "scrapling+scrapegraph"}
    except Exception as e1:
        last_err = f"scrapling: {e1}"
    # 2) Crawl4AI
    try:
        r = await crawl4ai_fetch(url)
        html = r["html"]
        md_raw = r["markdown"]
        title = r["title"]
        if not title:
            _, parsed_title = extract_main_content_html(html, url) if html else ("", "")
            title = parsed_title or url
        # run scrapegraph convert on main html too for consistency, prefer crawl4ai markdown if longer
        try:
            main_html, _ = extract_main_content_html(html, url) if html else ("", title)
            md_sg = scrapegraph_markdown(main_html, url) if main_html else ""
        except Exception:
            md_sg = ""
        md_best = md_raw if len(md_raw or "") >= len(md_sg or "") else md_sg
        header = f"# {title}\n\n> Source: {url}\n\n"
        md = header + (md_best or "")
        if len(md.strip()) < 200:
            raise RuntimeError(f"crawl4ai thin content: {last_err}")
        return {"url": url, "title": title, "html": html, "markdown": md, "links": r["links"], "method": f"crawl4ai+scrapegraph ({last_err})"}
    except Exception as e2:
        last_err2 = f"{last_err} | crawl4ai: {e2}"
    # 3) httpx fallback
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=25, headers={"User-Agent": "Mozilla/5.0 (compatible; docs-crawler)"}) as c:
            resp = await c.get(url)
            resp.raise_for_status()
            html = resp.text
            main_html, parsed_title = extract_main_content_html(html, url)
            md_body = scrapegraph_markdown(main_html, url)
            title = parsed_title or url
            header = f"# {title}\n\n> Source: {url}\n\n"
            md = header + md_body
            soup = BeautifulSoup(html, "lxml")
            links = [a.get("href", "") for a in soup.find_all("a", href=True)]
            return {"url": url, "title": title, "html": html, "markdown": md, "links": links, "method": f"httpx+scrapegraph ({last_err2})"}
    except Exception as e3:
        raise RuntimeError(f"all fetchers failed for {url}: {last_err2} | httpx: {e3}")

# ---------- sitemap + llms discovery ----------
async def load_sitemap_urls():
    urls = set()
    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as c:
        r = await c.get(SITEMAP_INDEX)
        r.raise_for_status()
        import xml.etree.ElementTree as ET
        try:
            root = ET.fromstring(r.text)
            ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            # sitemap index?
            sitemaps = [e.find("s:loc", ns).text for e in root.findall("s:sitemap", ns) if e.find("s:loc", ns) is not None]
            if sitemaps:
                print(f"[sitemap] found {len(sitemaps)} sitemap files")
                for sm in sitemaps:
                    try:
                        rr = await c.get(sm, timeout=30)
                        rr.raise_for_status()
                        rt = ET.fromstring(rr.text)
                        locs = [e.find("s:loc", ns).text for e in rt.findall("s:url", ns) if e.find("s:loc", ns) is not None]
                        for u in locs:
                            n = normalize_url(u)
                            if n:
                                urls.add(n)
                        print(f"[sitemap] {sm}: {len(locs)} urls (total {len(urls)})")
                    except Exception as e:
                        print(f"[sitemap] failed {sm}: {e}")
            else:
                locs = [e.find("s:loc", ns).text for e in root.findall("s:url", ns) if e.find("s:loc", ns) is not None]
                if not locs:  # regex fallback
                    locs = re.findall(r"<loc>([^<]+)</loc>", r.text)
                for u in locs:
                    n = normalize_url(u)
                    if n:
                        urls.add(n)
                print(f"[sitemap] urlset: {len(locs)} urls (total {len(urls)})")
        except Exception as e:
            print(f"[sitemap] parse failed, regex fallback: {e}")
            for u in re.findall(r"<loc>([^<]+)</loc>", r.text):
                n = normalize_url(u)
                if n:
                    urls.add(n)
    return sorted(urls)

async def load_llms_urls():
    urls = set()
    llms_files = []
    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as c:
        for llms_url in [MAIN_LLMS, FULL_LLMS]:
            try:
                r = await c.get(llms_url, timeout=30)
                if r.status_code != 200:
                    print(f"[llms] {llms_url} -> {r.status_code}")
                    continue
                safe = llms_url.replace("https://", "").replace("/", "_")
                (OUT_ROOT / "_llms" / safe).write_text(r.text[:5000000], encoding="utf-8")
                llms_files.append(llms_url)
                print(f"[llms] saved {llms_url} ({len(r.text)} chars)")
                for m in re.findall(r"\(https://docs\.sarvam\.ai[^\)]+\)", r.text):
                    m = m.strip("()")
                    n = normalize_url(m)
                    if n:
                        urls.add(n)
                for m in re.findall(r"https://docs\.sarvam\.ai/[^\s\)\]]+", r.text):
                    m = m.rstrip(").,")
                    if m.endswith(".txt"):
                        continue
                    n = normalize_url(m)
                    if n:
                        urls.add(n)
            except Exception as e:
                print(f"[llms] failed {llms_url}: {e}")
    print(f"[llms] discovered {len(urls)} urls from llms.txt")
    return sorted(urls), llms_files

# ---------- main crawl ----------
async def main(max_pages=15000, concurrency=12):
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    # load state
    visited = {}
    failed = {}
    if STATE_FILE.exists():
        try:
            st = json.loads(STATE_FILE.read_text())
            visited = st.get("visited", {})
            failed = st.get("failed", {})
            print(f"[state] resumed: {len(visited)} visited, {len(failed)} failed")
        except Exception as e:
            print(f"[state] corrupt, starting fresh: {e}")
    # seed urls
    sitemap_urls = await load_sitemap_urls()
    llms_urls, llms_files = await load_llms_urls()
    seeds = []
    seen_seed = set()
    for u in sitemap_urls + llms_urls + [BASE_URL + "/"]:
        if u not in seen_seed:
            seen_seed.add(u)
            seeds.append(u)
    print(f"[seed] sitemap={len(sitemap_urls)} llms-derived={len(llms_urls)} total seeds={len(seeds)}")
    # BFS queue: prioritize seeds not yet visited
    queue = asyncio.Queue()
    queued = set()
    for u in seeds:
        if u not in visited and u not in queued:
            await queue.put((u, 0))
            queued.add(u)
    # also track subdomain stats
    stats = {"ok": 0, "fail": 0, "skipped_existing": 0, "by_method": {}, "by_host": {}}
    # resume counts
    stats["ok"] = len(visited)
    # open index file append
    existing_index_urls = set(visited.keys())
    idx_f = open(INDEX_FILE, "a", encoding="utf-8")

    sem = asyncio.Semaphore(concurrency)

    async def worker(wid):
        nonlocal stats
        while True:
            try:
                url, depth = queue.get_nowait()
            except asyncio.QueueEmpty:
                return
            if len(visited) >= max_pages and url not in visited:
                # cap total pages (fixed: previously used queue.qsize which broke smoke tests)
                queue.task_done()
                continue
            rel = url_to_relpath(url)
            fpath = OUT_ROOT / rel
            # skip if file exists and visited (resume)
            if url in visited and fpath.exists():
                stats["skipped_existing"] += 1
                queue.task_done()
                continue
            # skip if file exists on disk but not in state (previous run)
            if fpath.exists() and fpath.stat().st_size > 500 and url not in visited:
                visited[url] = {"file": str(rel), "skipped": True}
                queue.task_done()
                continue
            async with sem:
                try:
                    data = await fetch_one(url)
                    # save markdown
                    fpath.parent.mkdir(parents=True, exist_ok=True)
                    # frontmatter
                    fm = f"---\nurl: {url}\ntitle: {json.dumps(data['title'])[1:-1]}\nmethod: {data['method']}\nfetched_at: {datetime.now(timezone.utc).isoformat()}\n---\n\n"
                    (fpath).write_text(fm + data["markdown"], encoding="utf-8")
                    # save meta
                    meta_rel = Path("_meta") / (rel.with_suffix(".json") if rel.suffix == ".md" else Path(str(rel) + ".json"))
                    meta_path = OUT_ROOT / meta_rel
                    meta_path.parent.mkdir(parents=True, exist_ok=True)
                    meta = {"url": url, "file": str(rel), "title": data["title"], "method": data["method"], "fetched_at": datetime.now(timezone.utc).isoformat(), "html_len": len(data.get("html", "")), "md_len": len(data.get("markdown", "")), "depth": depth}
                    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
                    visited[url] = {"file": str(rel), "title": data["title"], "method": data["method"]}
                    idx_f.write(json.dumps({"url": url, "file": str(rel), "title": data["title"], "method": data["method"]}) + "\n")
                    if len(visited) % 20 == 0:
                        idx_f.flush()
                    stats["ok"] += 1
                    m = data["method"].split()[0]
                    stats["by_method"][m] = stats["by_method"].get(m, 0) + 1
                    host = urlparse(url).netloc
                    stats["by_host"][host] = stats["by_host"].get(host, 0) + 1
                    # enqueue discovered links (depth+1), only if depth < 6 for subdomains expansion + unlimited for main sitemap?
                    # Since seeds already cover sitemap, we expand all internal links to catch missing pages
                    for href in data.get("links", []):
                        n = normalize_url(href, base=url)
                        if not n:
                            continue
                        if n in visited or n in queued:
                            continue
                        # depth guard: main host unlimited depth (sitemap covers), subdomains max depth 4
                        nhost = urlparse(n).netloc
                        nd = depth + 1
                        if nhost != MAIN_HOST and nd > 4:
                            continue
                        if len(queued) + len(visited) >= max_pages:
                            break
                        queued.add(n)
                        await queue.put((n, nd))
                    if stats["ok"] % 100 == 0:
                        print(f"[progress] ok={stats['ok']} fail={stats['fail']} queue={queue.qsize()} methods={stats['by_method']} hosts={dict(list(stats['by_host'].items())[:5])}")
                        # checkpoint state
                        STATE_FILE.write_text(json.dumps({"visited": visited, "failed": failed, "updated": datetime.now(timezone.utc).isoformat()}, indent=2)[:20000000])
                except Exception as e:
                    failed[url] = str(e)[:500]
                    stats["fail"] += 1
                    if stats["fail"] % 50 == 0 or len(str(e)) < 200:
                        print(f"[fail] {url}: {e}")
                finally:
                    queue.task_done()
            # periodic state save
            if (stats["ok"] + stats["fail"]) % 200 == 0:
                try:
                    STATE_FILE.write_text(json.dumps({"visited": visited, "failed": failed, "updated": datetime.now(timezone.utc).isoformat()}))
                except Exception:
                    pass

    # launch workers as tasks draining queue dynamically (workers loop until empty, new items added during run)
    # Use N concurrent workers
    async def supervisor():
        tasks = [asyncio.create_task(worker(i)) for i in range(concurrency)]
        # wait until queue empty and workers done; queue may grow, so poll
        while True:
            await asyncio.sleep(2)
            if queue.empty():
                await asyncio.sleep(3)
                if queue.empty():
                    break
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    t0 = time.time()
    await supervisor()
    idx_f.close()
    # close crawler
    global _crawler
    if _crawler is not None:
        try:
            await _crawler.close()
        except Exception:
            pass
    STATE_FILE.write_text(json.dumps({"visited": visited, "failed": failed, "updated": datetime.now(timezone.utc).isoformat()}))
    manifest = {
        "base": BASE_URL,
        "total_seeds": len(seeds),
        "sitemap_count": len(sitemap_urls),
        "llms_files": llms_files,
        "visited": len(visited),
        "failed": len(failed),
        "stats": stats,
        "elapsed_sec": round(time.time() - t0, 1),
        "out_root": str(OUT_ROOT),
        "tools": ["scrapling (Fetcher)", "crawl4ai (AsyncWebCrawler fallback)", "scrapegraph-ai (cleanup_html/convert_to_md)"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    try:  # merge over existing manifest: preserves updater stamps (last_verified) across boot-time resume runs
        prev = json.loads(MANIFEST_FILE.read_text()) if MANIFEST_FILE.exists() else {}
        prev.update(manifest)
        manifest = prev
    except Exception as e:
        print(f"[manifest] merge skipped: {e}")
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2))
    print(f"[done] visited={len(visited)} failed={len(failed)} elapsed={manifest['elapsed_sec']}s")
    print(f"[done] manifest -> {MANIFEST_FILE}")
    # list sample
    print(f"[sample] {list(visited.items())[:3]}")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-pages", type=int, default=15000)
    ap.add_argument("--concurrency", type=int, default=12)
    args = ap.parse_args()
    asyncio.run(main(max_pages=args.max_pages, concurrency=args.concurrency))
