import requests
from bs4 import BeautifulSoup
import json

response = requests.get("https://books.toscrape.com")
document = BeautifulSoup(response.text, "html.parser")

books = document.find_all("article", class_="product_pod")

book_list = []

for book in books:
    title = book.h3.a["title"]
    price = book.find("p", class_="price_color").text
    price = price.replace("Â£", "")
    price_number = float(price)

    book_data = {
        "title": title,
        "price": price_number
    }

    book_list.append(book_data)

with open("products_and_prices.json", "w", encoding="utf-8") as file:
    json.dump(book_list, file, indent=4, ensure_ascii=False)

print(book_list)