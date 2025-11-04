# 📚 Book Recommendation System  
*Ironhack Data Analytics Bootcamp — Week 10 Project*  
*Author: Irma Fernández Wiechers*  

---

## 🎯 Project Overview

This project aims to build a **Book Recommendation System** using real data from **Goodreads** and **Google Books API**.  
It combines skills in **web scraping, data cleaning, enrichment, and clustering** — simulating a real-world end-to-end data science pipeline.

The system ultimately recommends books based on **content similarity** (e.g. rating, genre, author, and publication year).

---

## 🧭 Project Workflow

| Phase | Description | Output |
|:--|:--|:--|
| **1. Data Acquisition** | Scraped ~1000 books from Goodreads (Best Books Ever list) across 10 pages. | `books_clean.csv`, `books_clean_enriched_1000.csv` |
| **2. API Enrichment** | Used Google Books API to enrich missing metadata (genre, published year, price, cover URL). | `books_enriched.csv` |
| **3. Data Cleaning** | Removed duplicates, standardized text fields, and extracted numeric ratings. | `books_clean.csv` |
| **4. Data Combination** | Merged both datasets (web + API) into a final 1000-book dataset. | `books_final_1000.csv` |
| **5. Exploratory Analysis** | Visualized distribution of ratings, genres, prices, and publication years. | EDA plots |
| **6. Standardization** | Rounded numeric values, formatted text alignment, and verified structure. | `books_final_1000.csv` |
| **7. Feature Engineering** | (Next) Prepare features for clustering and model training. | `books_features.csv` |
| **8. Modeling & Deployment** | (Next) Build a Streamlit prototype for book recommendations. | `app/` |

---

## 🧩 Data Sources

| Source | Type | Description |
|:--|:--|:--|
| [Goodreads](https://www.goodreads.com/list/show/1.Best_Books_Ever) | Web scraping | Book titles, authors, ratings, links |
| [Google Books API](https://developers.google.com/books) | API | Genres, publication dates, cover URLs, prices |

---

## 🧠 Key Learnings

- Ethical web scraping and responsible request handling (`time.sleep`, headers)
- API integration with fallback logic and exception handling
- Data cleaning and standardization using `pandas`
- Combining heterogeneous sources into a unified dataset
- Visualization of real-world book data with `matplotlib` and `seaborn`
- Preparing for unsupervised learning (K-Means, PCA)

---

## 📁 Repository Structure
```
book-recommendation-system/
│
├── data/
│ ├── raw/ # Raw scraped and API data
│ └── clean/ # Cleaned and enriched datasets
│
├── notebooks/
│ ├── 01_web_scraping_goodreads.ipynb
│ ├── 02_web_scraping_goodreads_part2.ipynb
│ └── 03_book_features_clustering.ipynb
│
├── models/ # Trained models (future)
├── app/ # Streamlit deployment files (future)
├── utils/ # Helper scripts
├── functions.py # Reusable functions
├── config.yaml # Project configuration
└── README.md # (this notebook section)
```

---

## 📊 Current Output Summary (as of Notebook 02)

**First dataset:** (493, 9)  
**Second dataset:** (497, 8)  
✅ **Combined dataset shape:** (990, 8)  
👩‍💻 **Unique authors:** 614  

**Missing values summary:**

| Column | Missing Values |
|:--|--:|
| genre | 123 |
| price | 529 |
| currency | 529 |
| cover_url | 96 |

💾 **Final dataset:**  
`data/clean/books_final_1000.csv`

---

## 🚀 Next Steps (Notebook 03)

- Load and preprocess the final dataset  
- Perform feature extraction (numeric + text features)
- Apply **K-Means clustering** to group similar books  
- Visualize clusters using **PCA / t-SNE**
- Build a **content-based recommendation system**

---

## 🧑‍💻 Tech Stack

- **Python 3.11**
- **Libraries:** pandas, numpy, requests, BeautifulSoup, tqdm, matplotlib, seaborn, scikit-learn  
- **Deployment:** Streamlit (prototype stage)
- **Version Control:** Git / GitHub

---
---

## 🖥️ Project Presentation

You can explore the visual summary of this project in the following Google Slides presentation:

📎 **[Book Recommendation System — Presentation](https://docs.google.com/presentation/d/1E7G5gAWvXtJ8QqcWSpAUfGRWLJ3w96kZmLjyGypRF10/edit?usp=sharing)**

---

*The presentation summarizes the full pipeline: from data collection and enrichment to clustering insights and the upcoming Streamlit app for book exploration.*


## 💬 Author

**Irma Fernández Wiechers**  
Data Analyst | Ironhack Berlin 2025  
📍 Based in Germany 🇩🇪  
💼 Background: Insurance brokerage, anti-money laundering, and data analytics  
