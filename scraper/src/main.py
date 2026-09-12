import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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

