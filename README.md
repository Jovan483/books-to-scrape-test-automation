# Books to Scrape – QA Automation Project

## Project Overview

This project demonstrates a QA automation workflow using data collected from the [Books to Scrape](https://books.toscrape.com/) website.

The project covers data collection, database storage, backend testing, UI testing, and negative testing.

The main goal is to verify data accuracy and consistency across different application layers.

## Technologies Used

- Python 3.12
- Requests
- BeautifulSoup
- MySQL
- MySQL Connector
- Pytest
- Selenium WebDriver
- python-dotenv

## Project Structure

```text
Projekat1/
│
├── .gitignore
├── README.md
├── scrape_books.py
├── load_books_to_database.py
├── products_and_prices.json
│
└── test/
    ├── conftest.py
    ├── test_database.py
    ├── test_negative.py
    └── test_ui.py
```

## Project Workflow

### 1. Data Collection

- Sends HTTP requests to the Books to Scrape website.
- Uses BeautifulSoup to extract book titles and prices.
- Saves the collected data in JSON format.

### 2. Data Storage

- Imports the JSON data into a MySQL database.
- Stores book titles and prices in the `books` table.

### 3. Backend Testing

Uses Pytest to verify:

- Number of books in the database.
- Book titles are not empty.
- Book prices are valid.
- Duplicate book titles are detected.
- JSON data matches database records.

### 4. UI Testing

Uses Selenium WebDriver to verify:

- Website response status.
- Number of books displayed.
- Book titles and prices.
- Consistency between UI data and database records.
- Book detail pages.
- Navigation between pages.

### 5. Negative Testing

Tests how the database handles invalid data, including:

- Negative book prices.
- NULL book titles.
- Duplicate book titles.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Projekat1
```

### 2. Install dependencies

```bash
pip install requests beautifulsoup4 mysql-connector-python pytest selenium python-dotenv
```

### 3. Configure MySQL

Create a MySQL database named `knjizara` and prepare a table named `books` with the following columns:

- `book_title`
- `book_price`

### 4. Configure environment variables

Create a `.env` file in the project root directory:

```text
DB_PASSWORD=your_mysql_password
```

Replace the example value with your local MySQL password.

The `.env` file is excluded from Git tracking and should never be committed.

## Running the Project

### Run the scraper

```bash
python scrape_books.py
```

### Import data into MySQL

```bash
python load_books_to_database.py
```

### Run all tests

```bash
pytest test
```

### Run individual test modules

```bash
pytest test/test_database.py
pytest test/test_negative.py
pytest test/test_ui.py
```

## Test Results

The current test suite contains **16 automated tests**:

- 5 backend tests
- 3 negative tests
- 8 UI tests

Latest execution result:

```text
16 passed in 88.08s
```

## Notes

- MySQL must be running before executing database tests.
- Chrome browser is required for Selenium UI tests.
- The `.env` file must be configured locally before running database tests.
- Generated cache files and folders are excluded through `.gitignore`.

## Author

QA Automation Portfolio Project