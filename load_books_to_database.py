import os
from dotenv import load_dotenv
import json
import mysql.connector
load_dotenv()
with open("products_and_prices.json","r", encoding="utf-8") as fajl:
    data_from_json=json.load(fajl)
connection=mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("DB_PASSWORD"),
    database="knjizara",
    
)
cursor=connection.cursor()
query="INSERT INTO  books(book_title,book_price)  VALUES(%s,%s)"

data_for_database=[(book["title"],book["cena"]) for book in data_from_json]
cursor.executemany(query,data_for_database)
connection.commit()
cursor.close()
connection.close()

    
