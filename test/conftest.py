
import os
import mysql.connector
import pytest
from dotenv import load_dotenv
from selenium import webdriver

load_dotenv()

@pytest.fixture
def database_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="knjizara",
        ssl_disabled=True
    )

    yield connection

    connection.close()


@pytest.fixture
def browser():
    driver = webdriver.Chrome()

    yield driver

    driver.quit()