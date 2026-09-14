from bs4 import BeautifulSoup

with open("cache/book-1.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
desc_heading = soup.select_one("#product_description")
desc_paragraph = desc_heading.find_next_sibling("p")

print("RAW HTML OF THE <p> TAG:")
print(desc_paragraph.prettify())