import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError, HttpUrl
from typing import Optional
import json

USER_AGENT = "FlyRankInternshipA9/1.0 (+https://github.com/AswinCBiju/flyrank.ai/tree/master/scraper)"
TIME_OUT = 5
CACHE_DIR = "cache"
stats = {"fetched": 0, "cache_hits": 0}

class Book(BaseModel):
    title: str
    product_url: HttpUrl
    price_text: str
    price_gbp: float
    availability_text: str
    rating_text: str
    description: Optional[str] = None
    source_page: str
    fetched_at: str

def parse_price(price_text):
    cleaned_price = price_text.replace("£","").strip()
    try:
        return float(cleaned_price)
    except ValueError as e:
        print(f"FAILED TO PARSE PRICE: {repr(price_text)} -> cleaned: {repr(cleaned_price)}")
        raise
def find_next_page(html, page_url):
    soup = BeautifulSoup(html, "html.parser")
    next_link = soup.select_one("li.next a")

    if next_link is None:
        return None

    href = next_link.get("href")
    return urljoin(page_url, href)

def extract_book_links(html, page_url):
    soup = BeautifulSoup(html, "html.parser")
    links = []

    for article in soup.select("article.product_pod h3 a"):
        href = article.get("href")
        absolute_url = urljoin(page_url, href)
        links.append(absolute_url)
    return links

def discover_all_book_links(max_pages):
    all_links = []
    page_url = "https://books.toscrape.com/catalogue/page-1.html"
    page_num = 1

    while page_url is not None and page_num <= max_pages:
        cache_filename = f"catalogue-page-{page_num}.html"
        html = fetch_page(page_url, cache_filename)

        if html is None:
            print(f"Could not fetch {page_url}, stopping crawl")
            break

        links = extract_book_links(html, page_url)
        all_links.extend(links)

        page_url = find_next_page(html, page_url)
        page_num += 1

    return all_links

def extract_book_details(html, product_url, source_page):
    soup = BeautifulSoup(html, "html.parser")
    product_area = soup.select_one("div.product_main")

    title = product_area.select_one("h1").get_text(strip=True)
    price_text = product_area.select_one("p.price_color").get_text(strip=True)
    availability_text = product_area.select_one("p.availability").get_text(strip=True)
    rating_tag = product_area.select_one("p.star-rating")
    rating_classes = rating_tag.get("class")
    rating_text = [c for c in rating_classes if c != "star-rating"][0]

    description_tag = soup.select_one("#product_description")
    if description_tag != None:
        description = description_tag.find_next_sibling("p").get_text(strip=True)
    else:
        description = None

    return {
         "title": title,
        "product_url": product_url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": datetime.now(timezone.utc).isoformat()
    }

def extract_all_book_details(book_urls):
    all_records = []
    failed_pages = []

    for i, url in enumerate(book_urls, start=1):
        cache_filename = f"book-{i}.html"
        html = fetch_page(url, cache_filename)

        if html == None:
            print(f"Could not fetch {url}, skipping")
            failed_pages.append(url)
            continue

        record = extract_book_details(html, product_url=url, source_page=url)
        all_records.append(record)
    return all_records, failed_pages

def validate_record(raw_record):
    try:
        price_gbp = parse_price(raw_record["price_text"])
    except (ValueError,KeyError) as e:
        return None, f"could not parse price: {e}"

    try:
        book = Book(
            title=raw_record["title"],
            product_url=raw_record["product_url"],
            price_text=raw_record["price_text"],
            price_gbp=price_gbp,
            availability_text=raw_record["availability_text"],
            rating_text=raw_record["rating_text"],
            description=raw_record["description"],
            source_page=raw_record["source_page"],
            fetched_at=raw_record["fetched_at"]
        )
    except ValidationError as e:
        return None, str(e)

    return book, None

def validate_and_store(raw_records):
    seen = set()
    valid_books = []
    errors = []

    for raw in raw_records:
        book, error = validate_record(raw)

        if error:
            errors.append({"record": raw, "reason": error})
            continue

        url = str(book.product_url)
        if url in seen:
            continue
        seen.add(url)

        valid_books.append(book.model_dump(mode="json"))

    os.makedirs("output", exist_ok=True)

    with open("output/books.json", "w", encoding="utf-8") as f:
        json.dump(valid_books, f, indent=2)

    with open("output/errors.json", "w", encoding="utf-8") as f:
        json.dump(errors, f, indent=2)

    return valid_books, errors
            
def fetch_page(url, cache_filename, delay=0.5, max_retries=1):
    os.makedirs(CACHE_DIR, exist_ok = True)
    cache_path = os.path.join(CACHE_DIR, cache_filename)

    print("Looking for cache at:", os.path.abspath(cache_path))
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            html = f.read()
        print(f"CACHE HIT  {cache_filename}  ({len(html)} bytes)")
        stats["cache_hits"] += 1
        return html

    headers = {"user-agent": USER_AGENT}
    attempt = 0

    while attempt <= max_retries:
        attempt += 1
        try:
            response = requests.get(url, headers=headers, timeout=TIME_OUT)
        except requests.exceptions.Timeout:
            print(f"FETCH_FAILED {url} (timeout, attempt {attempt})")
            if attempt <= max_retries:
                time.sleep(1)
                continue
            return None
        except requests.exceptions.RequestException as e:
            print(f"FETCH_FAILED {url} ({e})")
            return None

        status = response.status_code

        if status == 200:
            response.encoding = "utf-8"
            html = response.text
            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"FETCH      {cache_filename}  ({len(html)} bytes)")
            stats["fetched"] += 1
            time.sleep(delay)
            return html

        if status in (404, 403):
            print(f"FETCH_FAILED {url} (status {status}, not retrying)")
            return None

        if status >= 500:
            print(f"FETCH_FAILED {url} (status {status}, attempt {attempt})")
            if attempt <= max_retries:
                time.sleep(1)
                continue
            return None

        print(f"FETCH_FAILED {url} (status {status})")
        return None

    return None

def run_report(start_time, pages_fetched, cache_hits, valid_count, invalid_count, failed_pages):
    duration = time.time() - start_time

    report = {
        "start_time": datetime.fromtimestamp(start_time, tz=timezone.utc).isoformat(),
        "duration_seconds": round(duration, 2),
        "pages_fetched": pages_fetched,
        "cache_hits": cache_hits,
        "valid_records": valid_count,
        "invalid_records": invalid_count,
        "failed_pages": len(failed_pages),
        "failed_page_urls": failed_pages,
    }

    os.makedirs("output", exist_ok=True)
    with open("output/run-report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return report

if __name__ == "__main__":
    start_time = time.time()

    all_links = discover_all_book_links(3)
    seen = set()
    unique_links = []
    for link in all_links:
        if link not in seen:
            seen.add(link)
            unique_links.append(link)

    print(f"catalogue_pages={3}")
    print(f"discovered={len(all_links)}")
    print(f"unique_urls={len(unique_links)}")

    raw_records, failed_pages = extract_all_book_details(unique_links)
    print(f"detail_pages={len(raw_records)}")

    valid_books, errors = validate_and_store(raw_records)
    print(f"valid_records={len(valid_books)}")
    print(f"invalid_records={len(errors)}")

    report = run_report(
        start_time=start_time,
        pages_fetched=stats["fetched"],
        cache_hits=stats["cache_hits"],
        valid_count=len(valid_books),
        invalid_count=len(errors),
        failed_pages=failed_pages,
    )
    print("run-report.json written:", report)