#!/usr/bin/env python3
"""Coder: scrape ONE Sarvam docs URL end-to-end.
Stack: Scrapling (fetch) -> Crawl4AI (JS fallback) -> ScrapeGraphAI (HTML->MD).
Usage: python3 coder_scrape.py https://docs.sarvam.ai/api/getting-started/quickstart [out.md]
Note: appending .md to any docs URL also returns clean Markdown (Fern).
"""
import sys, json, importlib.util, asyncio
from pathlib import Path
from bs4 import BeautifulSoup

def _tools():
    for c in [Path(__file__).resolve().parents[1] / "tools",
              Path("/data/opencode/sarvam/tools"),
              Path("/data/opencode/cloudflare/tools")]:
        if (c / "scrapegraph-ai" / "scrapegraphai" / "utils" / "convert_to_md.py").exists():
            return c
    import scrapegraphai
    return Path(scrapegraphai.__file__).parent
TOOLS = _tools()
def load(name, fp):
    spec = importlib.util.spec_from_file_location(name, fp)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
sg_md = load("sg_md", TOOLS / "scrapegraph-ai" / "scrapegraphai" / "utils" / "convert_to_md.py").convert_to_md
from scrapling import Fetcher

def scrapling_fetch(url):
    p = Fetcher.get(url, stealthy_headers=True, follow_redirects=True, timeout=25)
    if p.status != 200:
        raise RuntimeError(f"scrapling {p.status}")
    html = p.html_content
    links = [a.attrib.get("href", "") for a in p.css("a")]
    t = p.css("title::text")
    return html, links, str(t[0]).strip() if t else url

def main_html(html):
    soup = BeautifulSoup(html, "lxml")
    for t in soup(["script", "style", "noscript", "svg"]):
        t.decompose()
    main = soup.find("main") or soup.find("article") or soup.find("body")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    return str(main) if main else html, title

async def crawl4ai_fetch(url):
    from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
    from crawl4ai.async_webcrawler import BrowserConfig
    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as c:
        r = await c.arun(url=url, config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS))
        if not r.success:
            raise RuntimeError(r.error_message)
        return r.html, r.markdown

async def scrape(url):
    try:
        html, links, t = await asyncio.to_thread(scrapling_fetch, url)
        m, pt = main_html(html)
        md = sg_md(m, url)
        if len(md) < 500:
            raise RuntimeError("thin")
        return f"# {t or pt}\n\n> Source: {url}\n\n" + md, t or pt, "scrapling+scrapegraph"
    except Exception as e1:
        html, md_raw = await crawl4ai_fetch(url)
        m, pt = main_html(html)
        md_sg = sg_md(m, url) if m else ""
        best = md_raw if len(md_raw or "") >= len(md_sg) else md_sg
        return f"# {pt or url}\n\n> Source: {url}\n\n" + best, pt or url, f"crawl4ai+scrapegraph ({e1})"

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://docs.sarvam.ai/api/getting-started/quickstart"
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/sarvam_test.md"
    md, title, method = asyncio.run(scrape(url))
    Path(out).write_text(f"---\nurl: {url}\ntitle: {title}\nmethod: {method}\n---\n\n" + md)
    print(f"saved {out} ({len(md)} chars) via {method}")
