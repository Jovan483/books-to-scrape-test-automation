import pytest
import mysql.connector
def test_invalid_book_price_detected(database_connection):
    cursor=database_connection.cursor()
    cursor.execute(" INSERT INTO books(book_title,book_price) VALUES(%s,%s)",
                    ("Neagtiv Test Book", -10.00)

    )
    cursor.execute("""SELECT book_price,book_title
                    FROM books
                    WHERE book_price < 0 
                    """)
    data_books=cursor.fetchall()
    
    assert data_books!=[]
    
    database_connection.rollback()
    cursor.execute("""
    SELECT *
    FROM books
    WHERE book_title = %s
    """, ("NegativeTest Book",))

    result = cursor.fetchall()

    assert result == []
    cursor.close()


def test_book_title_cannot_be_null(database_connection):
    with pytest.raises(mysql.connector.errors.IntegrityError):
        cursor=database_connection.cursor()
        cursor.execute(""" INSERT INTO books (book_title, book_price)  
                            VALUES(%s,%s)
                             """,(None,10.00))
        cursor.close()


def test_duplicate_book_titles_detected(database_connection):
    cursor=database_connection.cursor()
    cursor.executemany(""" INSERT INTO books(book_title, book_price)
                        VALUES(%s,%s)
                          """,[
                              ("Duplicate Test Book",10.00),
                              ("Duplicate Test Book",15.00)
                              ])
    cursor.execute(""" SELECT book_title,COUNT(*)
                        FROM books
                        GROUP BY book_title
                        HAVING COUNT(*)>1
                    """)
    duplicates=cursor.fetchall()
    assert duplicates!=[]
    database_connection.rollback()
    cursor.close()