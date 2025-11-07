# 📚 Book Recommendation System  
*Ironhack Data Analytics Bootcamp — Week 10 Project*  
*Author: Irma Fernández Wiechers*  

---

## 🎯 Project Overview

This project aims to build a **Book Recommendation System** using real data from **Goodreads**, **Google Books API**, and **Kaggle’s Goodbooks-10 dataset.** .  
It combines skills in **web scraping, data cleaning, enrichment, and clustering** — simulating a real-world end-to-end data analytics and machine learning workflow.

The goal was to discover natural groupings among books based on ratings, genres, and prices, and make them interactive through a Streamlit app.

---

## 🧭 Project Workflow

| Phase | Description | Output |
|:--|:--|:--|
| **1. Data Acquisition** | Scraped 1,190 books from Goodreads (“Best Books Ever” list). | `books_clean.csv` |
| **2. API Enrichment** | Retrieved missing metadata (genre, price, cover) via Google Books API. | `books_clean_1000.csv` |
| **3. Kaggle Merge** | Merged with *goodbooks-10* dataset to fill missing ratings and prices. | `books_clean_enriched_1000.csv` |
| **4. Cleaning & Standardization** | Removed duplicates, imputed missing prices with median (8.99 EUR), and formatted text fields. | `books_clean_final_1000.csv` |
| **5. Feature Preparation** | Selected numerical features (`avg_rating`, `price`) and scaled them with StandardScaler. | `X_scaled.npy` |
| **6. Clustering (K-Means + PCA)** | Applied **K-Means** with k = 2–10; selected **k = 3** using Elbow & Silhouette methods. Reduced to 2D with **PCA** for visualization. | `books_clustered_final_enriched.csv` |
| **7. Insights & Interpretation** | Identified three reader segments: *Mainstream and affordable*,  *mid-range market*, combining both fiction and non-fiction titles, and *premium* and niche titles.| `cluster_summary.csv` |
| **8. Streamlit Deployment** | Built an interactive **Streamlit app** to explore clusters, analyze features, and get recommendations. | `/app/app.py` |

---

## 🧩 Data Sources

| Source | Type | Description |
|:--|:--|:--|
| [Goodreads](https://www.goodreads.com/list/show/1.Best_Books_Ever) | Web scraping | Book titles, authors, ratings, links |
| [Google Books API](https://developers.google.com/books) | API | Genres, prices, publication year, cover images |
| [Kaggle: goodbooks-10k](https://www.kaggle.com/datasets/zygmunt/goodbooks-10k) | Dataset | Used to fill missing rating and price values |

---

## 📊 Key Results

- **Optimal K = 3**, showing  separation between *Mainstream and affordable*,  *mid-range market*, combining both       fiction and non-fiction titles and *premium* and niche titles
- **PCA visualization** confirmed distinct group patterns in 2D space.  
- **Cluster 0:** mainstream and affordable (avg. price  €8.28 and average ratings 3.87 ★.  
- **Cluster 1:** mid-range market  (avg. price  €8.89 and average ratings 4.19 ★.
- **Cluster 2:** premium  (avg. price  €43.61 and average ratings 4.21 ★.
- **Streamlit App:** enables interactive exploration of clusters, prices, ratings, and recommendations.

---

## 🧠 Key Learnings

- Practical **web scraping** and **API enrichment** workflow  
- Combining **heterogeneous data sources** (web + API + Kaggle)  
- **Data cleaning**, **missing value imputation**, and **feature scaling**  
- Applying **unsupervised learning** (K-Means) and **dimensionality reduction** (PCA)  
- Building a **Streamlit app** for visualization and user interaction  
- Translating analytical results into **data-driven insights**  
---

## 📁 Repository Structure
```
book-recommendation-system/
│
├── app/
│   └── app.py        # Streamlit app
│
├── data/
│   ├── raw/          
│   └── clean/                                 
│                                
│
├── notebooks/
│   ├── 01_web_scraping_goodreads.ipynb
│   ├── 02_web_scraping_goodreads.ipynb
│   ├── 03_book_features_clustering.ipynb
│   ├── 04_book_enrichment_goodreads.ipynb
│   ├── 05_streamlit_app.ipynb
│   └── functions.py
│
│
├── visualizations/                            # Plots and figures for presentation
│
├── config.yaml                                # Project configuration (paths, constants)
├── pyproject.toml                             # Dependencies and environment setup
├── requirements                               # Streamlit app
├── uv.lock                                    # Environment lock file
└── README.md                                  # Project documentation

```
---

## 🖥️ Streamlit App

🚀 Explore the live prototype here:  
👉 [**Book Recommendation Explorer**](https://book-recommendation-system-3epf6uhaz4gnjlz99fnd9o.streamlit.app/) — built with Streamlit, showing book clusters based on rating and price.

The app allows users to:
- Explore clusters visually  
- Filter books by rating, genre, or price  
- Get book recommendations based on similarity  

---

## 📊 Presentation Slides

📎 **[Book Recommendation System — Final Presentation](https://docs.google.com/presentation/d/1E7G5gAWvXtJ8QqcWSpAUfGRWLJ3w96kZmLjyGypRF10/edit?usp=sharing)**  

Includes the full pipeline:  
→ from data collection & enrichment  
→ to clustering, insights, and Streamlit deployment.

---

## 💬 Author

**Irma Fernández Wiechers**  
Data Analyst | Ironhack Berlin 2025  
📍 Based in Germany 🇩🇪  
💼 Background: Insurance brokerage, AML investigation, and data analytics  

