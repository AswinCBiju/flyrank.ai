## Target classification

**Site:** Books to Scrape (https://books.toscrape.com)

**Why this site:** Books to Scrape is a public sandbox explicitly built for people to
practice web scraping on. The site's own homepage states it exists for this purpose,
which is my permission to scrape it.

**Scope:** I will fetch only the first 3 catalogue pages (page-1.html through
page-3.html) and the 60 individual book pages linked from them. No other pages or
sites are touched.

**Data collected:** For each book — title, product URL, price, availability text,
star rating, description, plus provenance fields (source page and fetch timestamp).
This is publicly displayed product-catalogue data, not personal or private information.

**robots.txt check:** Requested `https://books.toscrape.com/robots.txt` on 09/09/26.
Result: "Received a 404 — no robots
file found. This is not permission by itself, just the absence of a rule."

**Why this is appropriate here:** The target is a sandbox designed for scraping
practice, my scope is limited to a small, publicly visible slice of it, and I'm
following politeness rules (identifying user-agent, delay, timeout, caching).

I will not reuse this code on another site without checking its rules and terms first.