# ============================================================
# 📚 Book Recommendation Explorer — Final Clean Version
# ============================================================

import streamlit as st
import pandas as pd
import re
from pathlib import Path

# ============================================================
# Step 1 — Streamlit Setup & Dataset Load
# ============================================================

st.set_page_config(
    page_title="📚 Book Recommendation Explorer",
    page_icon="📖",
    layout="wide"
)

st.title("📚 Book Recommendation Explorer")
st.markdown("""
Explore books by cluster, rating, or price — based on the enriched dataset.
""")
st.caption("Three reader segments: affordable, mid-range, and premium.")

# --- Load dataset ---
data_path = Path("data") / "clean" / "books_clustered_final_enriched.csv"

try:
    df = pd.read_csv(data_path)
    st.success(f"✅ Dataset loaded successfully! Shape: {df.shape}")
    st.dataframe(df.head(5))
except FileNotFoundError:
    st.error("❌ Dataset not found. Please check your path: data/clean/books_clustered_final_enriched.csv")
    st.stop()

# ============================================================
# Step 2 — Sidebar Filters
# ============================================================

st.sidebar.header("🎛️ Filter Options")

# --- Genre filter (cleaned & consolidated) ---
genres_cleaned = (
    df["genre"]
    .dropna()
    .apply(lambda x: re.sub(r"[^A-Za-z& ]", "", str(x)).strip())
    .str.title()
)

genre_counts = genres_cleaned.value_counts()
valid_genres = genre_counts[genre_counts > 3].index.tolist()  # incluye solo géneros frecuentes

selected_genres = st.sidebar.multiselect(
    "Select genre(s):",
    options=sorted(valid_genres),
    default=sorted(valid_genres),
    key="genre_filter"
)

# --- Rating filter ---
min_rating = float(df["avg_rating"].min())
max_rating = float(df["avg_rating"].max())
rating_filter = st.sidebar.slider("Minimum average rating:", min_rating, max_rating, value=min_rating)

# --- Price filter ---
min_price = float(df["price"].min())
max_price = float(df["price"].max())
price_range = st.sidebar.slider("Price range (€):", min_price, max_price, (min_price, max_price))

# --- Cluster filter ---
clusters = sorted(df["cluster"].unique())
selected_clusters = st.sidebar.multiselect("Select cluster(s):", clusters, default=clusters)

# --- Apply filters ---
filtered_df = df[
    (df["genre"].isin(selected_genres)) &
    (df["avg_rating"] >= rating_filter) &
    (df["price"].between(price_range[0], price_range[1])) &
    (df["cluster"].isin(selected_clusters))
]

st.write(f"### 📚 Showing {filtered_df.shape[0]} books after filtering")
st.dataframe(filtered_df.head(10))

# ============================================================
# Step 3 — Book Explorer & Recommendations
# ============================================================

st.header("🔍 Book Explorer & Recommendations")

if not filtered_df.empty:
    selected_book = st.selectbox(
        "Select a book to explore:",
        filtered_df["title"].sort_values().unique(),
        key="book_selector"
    )

    book_info = filtered_df[filtered_df["title"] == selected_book].iloc[0]

    st.markdown(f"### **{book_info['title']}**")
    st.markdown(f"👤 Author: {book_info['author']}")
    st.markdown(f"⭐ Rating: {book_info['avg_rating']:.2f}")
    st.markdown(f"💶 Price: {book_info['price']:.2f} €")
    st.markdown(f"🏷️ Genre: {book_info['genre']}")
    st.markdown(f"🧩 Cluster: {book_info['cluster']}")

    if "cover_url" in book_info and isinstance(book_info["cover_url"], str):
        st.image(book_info["cover_url"], width=150)

    st.divider()
    st.subheader("📚 Similar Books (Same Cluster)")

    similar_books = (
        filtered_df[
            (filtered_df["cluster"] == book_info["cluster"]) &
            (filtered_df["title"] != book_info["title"])
        ]
        .sort_values("avg_rating", ascending=False)
        .head(5)
    )

    if not similar_books.empty:
        for _, row in similar_books.iterrows():
            st.markdown(f"**{row['title']}** — {row['author']}  |  ⭐ {row['avg_rating']:.2f}  |  💶 {row['price']:.2f} €")
    else:
        st.info("No similar books found in this cluster.")
else:
    st.warning("⚠️ Please adjust filters to see available books.")
