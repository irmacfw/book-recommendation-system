# ============================================================
# Utility Functions — Book Recommendation System
# ============================================================

# ============================================================
# functions.py — Common utilities for the Book Recommendation System
# ============================================================

# --- Core Libraries ---
import os
import sys
import time
import random
from pathlib import Path
from time import sleep
from tqdm import tqdm

# --- Data Handling ---
import pandas as pd
import numpy as np
import yaml

# --- Web & APIs ---
import requests
from bs4 import BeautifulSoup

# --- Visualization (for reusable plots if needed) ---
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# ⚙️ Configuration Management
# ============================================================

def load_config(config_path: Path) -> dict:
    """
    Load YAML configuration file.
    """
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ============================================================
# 📁 File Management
# ============================================================

def ensure_directories(paths: dict) -> None:
    """
    Ensure that all directories defined in config exist,
    always relative to the project root (one level above notebooks).
    """
    from pathlib import Path
    project_root = Path(__file__).resolve().parents[1]  # go one level up (root)
    for path_str in paths.values():
        full_path = project_root / path_str
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Ensured directory: {full_path}")

def save_dataset(df: pd.DataFrame, output_path: Path) -> None:
    """
    Save a cleaned dataset to CSV with UTF-8 encoding.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"💾 Dataset saved successfully → {output_path}")

    
# ============================================================
# 🌐 Web Scraping Helpers
# ============================================================

def fetch_html(url: str, sleep_time: float = 2.0) -> str:
    """
    Send a GET request to a URL and return the HTML content as text.
    Adds a small delay to avoid overloading the server.
    """
    import time
    import requests

    print(f"🌍 Fetching URL: {url}")
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    time.sleep(sleep_time)
    print("✅ HTML fetched successfully!")
    return response.text


def save_html(content: str, output_path: Path) -> None:
    """
    Save raw HTML content to a file (UTF-8 encoded).
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"💾 HTML saved → {output_path}")


def parse_html(content: str):
    """
    Parse HTML content with BeautifulSoup.
    """
    from bs4 import BeautifulSoup
    return BeautifulSoup(content, "html.parser")

# ============================================================
# 📚 Goodreads Parsing Helpers
# ============================================================

def extract_books_from_soup(soup) -> pd.DataFrame:
    """
    Extract book information (title, author, rating, link, cover) from Goodreads list page.
    """
    import pandas as pd

    books = []

    rows = soup.select("tr[itemtype='http://schema.org/Book']")
    print(f"📖 Found {len(rows)} books on the page")

    for row in rows:
        # --- Title ---
        title_tag = row.select_one("a.bookTitle")
        title = title_tag.text.strip() if title_tag else None

        # --- Link ---
        link = "https://www.goodreads.com" + title_tag["href"] if title_tag else None

        # --- Author ---
        author_tag = row.select_one("a.authorName")
        author = author_tag.text.strip() if author_tag else None

        # --- Rating ---
        rating_tag = row.select_one("span.minirating")
        rating = rating_tag.text.strip().split(" — ")[0] if rating_tag else None

        # --- Cover Image ---
        cover_tag = row.select_one("img.bookSmallImg")
        cover_url = cover_tag["src"] if cover_tag else None

        # --- Placeholders for now ---
        genre = None
        price = None
        published_year = None

        books.append({
            "title": title,
            "author": author,
            "rating": rating,
            "link": link,
            "cover_url": cover_url,
            "genre": genre,
            "price": price,
            "published_year": published_year
        })

    df = pd.DataFrame(books)
    print(f"✅ Extracted {len(df)} books into DataFrame")
    return df


