import os
import time
import requests

USER_AGENT = "FlyRankInternshipA9/1.0 (+https://github.com/AswinCBiju/flyrank.ai/tree/master/scraper)"
TIME_OUT = 5
CACHE_DIR = "cache"

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

