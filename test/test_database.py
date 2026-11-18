import pytest
import json
def test_book_count(database_connection):
    cursor = database_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM books")

    book_count = cursor.fetchone()

    assert book_count[0] == 20

    cursor.close()


def test_book_titles_are_not_empty(database_connection):
    cursor = database_connection.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM books
        WHERE book_title IS NULL
           OR TRIM(book_title) = ''
    """)

    empty_titles_count = cursor.fetchone()
    assert empty_titles_count[0] == 0

    cursor.close()


def test_book_prices_are_valid(database_connection):
    cursor = database_connection.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM books
        WHERE book_price IS NULL
           OR book_price <= 0
    """)

    invalid_prices_count = cursor.fetchone()
    assert invalid_prices_count[0] == 0

    cursor.close()


def test_book_titles_are_unique(database_connection):
    cursor = database_connection.cursor()
    cursor.execute("""
        SELECT book_title, COUNT(*)
        FROM books
        GROUP BY book_title
        HAVING COUNT(*) > 1
    """)

    duplicate_titles = cursor.fetchall()
    assert len(duplicate_titles) == 0

    cursor.close()


def test_json_matches_database(database_connection):
    with open("products_and_prices.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)

    cursor = database_connection.cursor()

    cursor.execute("""
        SELECT book_title, book_price
        FROM books
    """)

    database_data = cursor.fetchall()

    json_books = {
        book["title"]: round(float(book["price"]), 2)
        for book in json_data
    }

    database_books = {
        title: round(float(price), 2)
        for title, price in database_data
    }

    assert json_books == database_books

    cursor.close()