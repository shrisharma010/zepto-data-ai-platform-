import os
import re
import sqlite3
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Constants
BASE_URL = "https://books.toscrape.com/catalogue/category/books/"
CATEGORIES = {
    "Travel": "travel_2",
    "Mystery": "mystery_3",
    "Classics": "classics_6",
    "Historical Fiction": "historical-fiction_4"
}
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
GBP_TO_INR = 105.50
DB_PATH = "books.db"
OUTPUT_MD = "data_pipeline/sql_results.md"

def scrape_category(name, slug):
    """Scrapes all books from a given category across multiple pagination pages."""
    url = f"{BASE_URL}{slug}/index.html"
    rows = []
    while url:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        response.encoding = "utf-8"  # Ensure currency/special symbols load accurately
        
        soup = BeautifulSoup(response.text, "html.parser")
        for pod in soup.select("article.product_pod"):
            title = pod.h3.a["title"]
            price_str = pod.select_one("p.price_color").text.strip()
            star_elem = pod.select_one("p.star-rating")
            star_rating = star_elem["class"][1] if star_elem else None
            availability = pod.select_one("p.availability").text.strip()
            
            rows.append({
                "title": title,
                "price": price_str,
                "star_rating": star_rating,
                "availability": availability,
                "category": name,
            })
            
        # Check for next page
        nxt = soup.select_one("li.next a")
        url = urljoin(url, nxt["href"]) if nxt else None
        time.sleep(0.3)
    return rows

def parse_price(s):
    """Extracts numeric float value from a price string."""
    m = re.search(r"[\d.]+", str(s))
    return float(m.group()) if m else None

def main():
    print("--- STEP 1.1: Scraping Data ---")
    all_rows = []
    for name, slug in CATEGORIES.items():
        print(f"Scraping category: {name}...")
        all_rows.extend(scrape_category(name, slug))
        
    df = pd.DataFrame(all_rows)
    
    # Assertions for scraping constraints
    assert len(df) >= 60, f"Collected only {len(df)} rows, expected >= 60"
    assert df["category"].nunique() >= 3, f"Collected {df['category'].nunique()} categories, expected >= 3"
    print(f"Successfully scraped {len(df)} rows across {df['category'].nunique()} categories.")

    print("\n--- STEPS 1.2 & 1.3: Cleaning & Converting Data ---")
    df["price_gbp"] = df["price"].apply(parse_price)
    
    # Impute numeric failures using column median
    median_price = df["price_gbp"].median()
    df["price_gbp"] = df["price_gbp"].fillna(median_price)

    # Map star ratings and drop unmappable ones
    df["rating"] = df["star_rating"].map(RATING_MAP)
    df = df.dropna(subset=["rating"])
    
    # Handle stock availability status and convert to boolean
    df["in_stock"] = df["availability"].str.contains("in stock", case=False)
    df["rating"] = df["rating"].astype(int)
    df["in_stock"] = df["in_stock"].astype(bool)

    # Currency conversion: GBP to INR
    df["price_inr"] = (df["price_gbp"] * GBP_TO_INR).round(2)

    print("\n--- STEPS 1.4 & 1.5: Normalized Database & SQL Queries ---")
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create normalized schema
    cursor.execute("""
    CREATE TABLE categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        price_gbp REAL,
        price_inr REAL,
        rating INTEGER CHECK (rating BETWEEN 1 AND 5),
        in_stock INTEGER,
        category_id INTEGER NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    );
    """)

    # Insert categories & map IDs
    cat_map = {}
    for cat in df["category"].unique():
        cursor.execute("INSERT INTO categories (category_name) VALUES (?);", (cat,))
        cat_map[cat] = cursor.lastrowid

    # Insert books records
    for _, row in df.iterrows():
        cat_id = cat_map[row["category"]]
        cursor.execute("""
        INSERT INTO books (title, price_gbp, price_inr, rating, in_stock, category_id)
        VALUES (?, ?, ?, ?, ?, ?);
        """, (
            row["title"],
            row["price_gbp"],
            row["price_inr"],
            row["rating"],
            1 if row["in_stock"] else 0,
            cat_id
        ))
    conn.commit()

    # Define 5 distinct queries covering SELECT/WHERE, ORDER BY, LIMIT, DISTINCT, BETWEEN, IN, and JOIN
    queries = {
        "q1_high_rated_in_stock": """
            SELECT title, price_gbp, rating 
            FROM books 
            WHERE rating >= 4 AND in_stock = 1;
        """,
        "q2_top_expensive": """
            SELECT title, price_gbp 
            FROM books 
            ORDER BY price_gbp DESC 
            LIMIT 10;
        """,
        "q3_distinct_ratings": """
            SELECT DISTINCT rating 
            FROM books 
            ORDER BY rating DESC;
        """,
        "q4_price_between": """
            SELECT title, price_gbp 
            FROM books 
            WHERE price_gbp BETWEEN 20 AND 40;
        """,
        "q5_category_join": """
            SELECT b.title, c.category_name, b.price_inr 
            FROM books b 
            JOIN categories c ON b.category_id = c.category_id 
            WHERE c.category_name IN ('Travel', 'Mystery');
        """
    }

    # Execute and write text output to sql_results.md
    os.makedirs(os.path.dirname(OUTPUT_MD), exist_ok=True)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("# SQL Query Results for Module 1 Data Pipeline\n\n")
        for name, sql in queries.items():
            res_df = pd.read_sql(sql, conn)
            f.write(f"## Query: `{name}`\n")
            f.write("```sql\n" + sql.strip() + "\n```\n")
            f.write("**Output Table:**\n```text\n" + res_df.to_string(index=False) + "\n```\n\n")
    print(f"Saved all SQL results successfully to {OUTPUT_MD}")

    print("\n--- STEP 1.6: Pandas Equivalence Verification ---")
    # Verify SQL JOIN via pandas read_sql and DataFrame merge matching using pd.testing.assert_frame_equal
    sql_df = pd.read_sql(queries["q5_category_join"], conn)
    
    books_data = pd.read_sql("SELECT * FROM books", conn)
    cats_data = pd.read_sql("SELECT * FROM categories", conn)
    
    merged_df = books_data.merge(cats_data, on="category_id")
    filtered_df = merged_df[merged_df["category_name"].isin(["Travel", "Mystery"])]
    pandas_result = filtered_df[["title", "category_name", "price_inr"]].reset_index(drop=True)
    
    sql_sorted = sql_df.sort_values("title").reset_index(drop=True)
    pandas_sorted = pandas_result.sort_values("title").reset_index(drop=True)

    pd.testing.assert_frame_equal(sql_sorted, pandas_sorted, check_dtype=False)
    print("Verification Passed: Pandas merge matches SQLite JOIN output perfectly!")

    conn.close()

if __name__ == "__main__":
    main()