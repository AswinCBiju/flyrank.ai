import requests

response = requests.get(
    "https://books.toscrape.com/robots.txt",
    headers={"User-Agent": "FlyRankInternshipA9/1.0 (+https://github.com/yourname/scraper)"},
    timeout=5
)

print("Status code:", response.status_code)
print("Body:\n",response.text)


