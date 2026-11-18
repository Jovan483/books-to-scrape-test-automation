
import requests
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
def test_status_code():
    response=requests.get("https://books.toscrape.com/")
    assert response.status_code==200


def test_homepage_displays_20_books(browser):
    browser.get("https://books.toscrape.com/")
    br_knjige=browser.find_elements(By.CSS_SELECTOR,".product_pod")
    assert len(br_knjige)==20


def test_book_prices_match_database(browser, database_connection):
    browser.get("https://books.toscrape.com/")

    prices_elements = browser.find_elements(By.CSS_SELECTOR, ".price_color")
    all_prices = []

    for price in prices_elements:
        book_price = price.text.replace("£", "")
        book_price = float(book_price)
        all_prices.append(book_price)

    cursor = database_connection.cursor()
    cursor.execute("SELECT book_price FROM books")

    database_prices = cursor.fetchall()
    prices_from_db = []

    for price in database_prices:
        prices_from_db.append(float(price[0]))

    cursor.close()

    assert sorted(prices_from_db) == sorted(all_prices)


def test_book_titles_match_database(browser, database_connection):
    browser.get("https://books.toscrape.com/")

    books = browser.find_elements(By.CSS_SELECTOR, ".product_pod")
    website_titles = []

    for book in books:
        title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")

        website_titles.append(title)

    cursor = database_connection.cursor()
    cursor.execute("SELECT book_title FROM books")

    database_titles = cursor.fetchall()
    titles_from_db = []

    for title in database_titles:
        titles_from_db.append(title[0])

    cursor.close()

    assert sorted(titles_from_db) == sorted(website_titles)


def test_book_titles_and_prices_match_database(browser, database_connection):
    browser.get("https://books.toscrape.com/")

    books = browser.find_elements(By.CSS_SELECTOR, ".product_pod")
    website_books = {}

    for book in books:
        title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")

        price = book.find_element(By.CSS_SELECTOR, ".price_color").text

        price = float(price.replace("£", ""))
        website_books[title] = price

    cursor = database_connection.cursor()
    cursor.execute("SELECT book_title, book_price FROM books")

    database_data = cursor.fetchall()
    database_books = {}

    for book in database_data:
        title = book[0]
        price = float(book[1])
        database_books[title] = price

    cursor.close()

    assert website_books == database_books



def test_all_books_are_visible(browser):
    browser.get("https://books.toscrape.com/")
    books=browser.find_elements(By.CSS_SELECTOR,".product_pod")


    for book in books:
        assert book.is_displayed()

        title = book.find_element(By.CSS_SELECTOR, "h3 a")
        price = book.find_element(By.CSS_SELECTOR, ".price_color")

        assert title.is_displayed()
        assert price.is_displayed()
        assert price.text.startswith("£")
        assert title.get_attribute("title").strip()!=""
        
        link=title.get_attribute("href")
        assert link !=""
        assert link.startswith("https://")



def test_book_details_match_homepage(browser):

    browser.get("https://books.toscrape.com/")
    books = browser.find_elements(By.CSS_SELECTOR, ".product_pod")

    all_titles= []
    all_prices = []
    all_links = []

    for book in books:

        title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
        all_titles.append(title)

        price = book.find_element(By.CSS_SELECTOR, ".price_color").text
        all_prices.append(price)

        href = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("href")
        all_links.append(href)

    
    for i in range(len(all_links)):

        browser.get(all_links[i])

        
        title_on_page = browser.find_element(By.CSS_SELECTOR, "h1").text

        assert all_titles[i] == title_on_page

        
        stvarna_cena = browser.find_element(By.CSS_SELECTOR, ".price_color").text

        assert all_prices[i] == stvarna_cena


def test_open_new_page(browser):
    browser.get("https://books.toscrape.com/")
    all_books_page1=browser.find_elements(By.CSS_SELECTOR,".product_pod")
    next_button=browser.find_element(By.CSS_SELECTOR,"li.next a")

    titles_page1 = []

    for book in all_books_page1:
        title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
        titles_page1.append(title)

    next_button.click()

    assert "catalogue/page-2.html" in browser.current_url

    all_books_page2=browser.find_elements(By.CSS_SELECTOR,".product_pod")

    assert len(all_books_page2)==20

    for book in all_books_page2:
        assert book.is_displayed()

    titles_page2=[]
    for book in all_books_page2:
        title=book.find_element(By.CSS_SELECTOR,"h3 a").get_attribute("title")
        titles_page2.append(title)
    assert titles_page1!=titles_page2