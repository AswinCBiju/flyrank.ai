# The Polite Scraper

A small scraping pipeline that downloads the first 3 catalogue pages of
[Books to Scrape](https://books.toscrape.com), visits all 60 book pages,
and turns messy HTML into clean, validated JSON — without crashing on a
broken page, and with an honest report at the end of every run.

## Target classification

**Site:** Books to Scrape (https://books.toscrape.com)

**Why this site:** It's a public sandbox built specifically for people to
practice scraping on — the site itself states this purpose, which is my
permission to scrape it.

**Scope:** Only the first 3 catalogue pages and the 60 book detail pages
linked from them. Nothing else.

**Data collected:** Publicly displayed book catalogue data — title, price,
availability, rating, description — plus provenance (source page, fetch time).

**robots.txt check:** Requested `https://books.toscrape.com/robots.txt`.
[Paste your actual result here — either the contents received, or
"received a 404 — no robots file found."]

I will not reuse this code on another site without checking its rules and
terms first.

## How to run it

```bash
git clone [your repo URL]
cd scraper
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 src/main.py
```

Outputs land in `output/books.json` (60 validated records) and
`output/run-report.json` (a summary of the run).

## Lane

Python 3.10+, using:
- `requests` for HTTP
- `BeautifulSoup` for HTML parsing
- `Pydantic` for schema validation

## Record schema

```json
{
  "title": "string",
  "product_url": "string (https URL, canonical identity)",
  "price_text": "string, original raw text e.g. '£51.77'",
  "price_gbp": "float, cleaned numeric value",
  "availability_text": "string",
  "rating_text": "string",
  "description": "string or null",
  "source_page": "string",
  "fetched_at": "ISO 8601 UTC timestamp"
}
```

## Politeness rules

- Every real request sends an identifying user-agent:
  `FlyRankInternshipA9/1.0 (+[your repo link])`
- Every request has a 5-second timeout
- At least 500ms delay between real (non-cached) requests
- Status code checked before parsing — only 200 proceeds
- Timeouts and 5xx errors get one retry; 404 and 403 are never retried
- All pages are cached locally after first fetch — development reads
  from cache, never re-hits the live site

## Sample run report

```json
{
  "start_time": "2026-09-17T12:41:30.127801+00:00",
  "duration_seconds": 2.53,
  "pages_fetched": 0,
  "cache_hits": 63,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 0,
  "failed_page_urls": []
}
```

## Why no browser was needed

All the data used here (title, price, availability, rating, description) is
present directly in the server-rendered HTML — nothing is loaded
client-side via JavaScript. A browser (e.g. Playwright) would only add
startup cost and memory overhead with no benefit for this particular site.

## Known limitation

A small number of book descriptions on the source site contain duplicated
preview text embedded directly in the raw HTML (verified by inspecting the
cached HTML directly — not a bug in this scraper). These are stored as-is
rather than post-processed, since the duplication originates server-side.

## Ethics note

This scraper only targets a public sandbox explicitly built for scraping
practice. In general: prefer an official API when one exists, never bypass
logins, paywalls, or explicit blocks, and collect only the data actually
needed. This code should not be pointed at another site without first
checking that site's robots.txt and terms of service.