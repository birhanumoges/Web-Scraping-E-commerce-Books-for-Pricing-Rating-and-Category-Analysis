import requests
from bs4 import BeautifulSoup
import time
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import importlib

cleaner = importlib.import_module("note_books.02_cleaner")
db = importlib.import_module("note_books.03_db")

clean_price = cleaner.clean_price
convert_rating = cleaner.convert_rating
insert_book = db.insert_book

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

headers_list = [
    {"User-Agent": "Mozilla/5.0"},
    {"User-Agent": "Chrome/91.0"},
    {"User-Agent": "Safari/537.36"},
]

def scrape_page(page):
    url = BASE_URL.format(page)
    headers = random.choice(headers_list)

    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'   # ✅ FIX
    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]
        price_text = book.find("p", class_="price_color").text
        rating_class = book.find("p")["class"]

        price = clean_price(price_text)
        rating = convert_rating(rating_class)

        insert_book(title, price, rating)
        print("Inserted:", title)

def scrape_all():
    for page in range(1, 51):
        scrape_page(page)
        time.sleep(random.uniform(1, 2))  # polite delay

if __name__ == "__main__":
    scrape_all()
