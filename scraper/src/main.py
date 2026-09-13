import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone

USER_AGENT = "FlyRankInternshipA9/1.0 (+https://github.com/AswinCBiju/flyrank.ai/tree/master/scraper)"
TIME_OUT = 5
CACHE_DIR = "cache"
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

    for i, url in enumerate(book_urls, start=1):
        cache_filename = f"book-{i}.html"
        html = fetch_page(url, cache_filename)

        if html == None:
            print(f"Could not fetch {url}, skipping")
            continue

        record = extract_book_details(html, product_url=url, source_page=url)
        all_records.append(record)
    return all_records
     
def fetch_page(url, cache_filename, delay=0.5):
    os.makedirs(CACHE_DIR, exist_ok = True)
    cache_path = os.path.join(CACHE_DIR, cache_filename)

    print("Looking for cache at:", os.path.abspath(cache_path))
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            html = f.read()
        print(f"CACHE HIT  {cache_filename}  ({len(html)} bytes)")
        return html

    headers = {"user-agent": USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=TIME_OUT)
        response.encoding = response.apparent_encoding
    except requests.exceptions.RequestException as e:
        print(f"FETCH_FAILED {url} ({e})")
        return None
    
    status = response.status_code
    if status != 200:
        print(f"FETCH_FAILED {url} (status {status})")
        return None

    html = response.text


    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"FETCH      {cache_filename}  ({len(html)} bytes)")
    time.sleep(delay)

    return html

if __name__ == "__main__":
    url = "https://books.toscrape.com/catalogue/page-1.html"
    fetch_page(url, "catalogue-page-1.html")

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

    print(f"About to fetch {len(unique_links)} book pages")
    records = extract_all_book_details(unique_links)

    print(f"detail_pages={len(records)}")
    print(records[0])