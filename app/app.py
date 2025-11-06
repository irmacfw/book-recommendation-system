# ============================================================
# Step 1 — Streamlit Setup & Dataset Load
# ============================================================

import streamlit as st
import pandas as pd
from pathlib import Path

# --- Page config ---
st.set_page_config(
    page_title="📚 Book Recommendation Explorer",
    page_icon="📖",
    layout="wide"
)

# --- Title & intro ---
st.title("📚 Book Recommendation Explorer")
st.markdown("""
Explore book clusters, genres, prices, and recommendations  
based on the **enriched dataset** (`books_clustered_final_enriched.csv`).
""")

# --- Load dataset ---
data_path = Path("data") / "clean" / "books_clustered_final_enriched.csv"
df = pd.read_csv(data_path)

st.success(f"✅ Dataset loaded successfully! Shape: {df.shape}")
st.dataframe(df.head(5))

# ============================================================
# Step 2 — Sidebar Filters
# ============================================================

st.sidebar.header("🎛️ Filter Options")

# --- Genre filter ---
# --- Genre filter (cleaned & consolidated) ---
import re

# Limpiar y normalizar valores de género
genres_cleaned = (
    df["genre"]
    .dropna()
    .apply(lambda x: re.sub(r"[^A-Za-z& ]", "", str(x)).strip())  # quita caracteres raros
    .str.title()
)

# Mantener solo los géneros más comunes (evitar outliers o strings raros)
genre_counts = genres_cleaned.value_counts()
valid_genres = genre_counts[genre_counts > 3].index.tolist()  # puedes ajustar el 3 si quieres incluir más

# Filtro
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
# Step 3–7 — Book Explorer First (Tabs Reordered)
# ============================================================

tab1, tab2 = st.tabs(["📚 Book Explorer", "📊 Dashboard"])

# ============================================================
# TAB 1 — Book Explorer & Recommendations (Default View)
# ============================================================
with tab1:
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
        st.warning("⚠️ Please select at least one genre or cluster to explore books.")

# ============================================================
# TAB 2 — Dashboard (Second)
# ============================================================
with tab2:
    st.header("📊 Dataset Dashboard")

    if not filtered_df.empty:
        avg_price = filtered_df["price"].mean()
        avg_rating = filtered_df["avg_rating"].mean()
        num_books = filtered_df.shape[0]
        num_genres = filtered_df["genre"].nunique()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📚 Books", f"{num_books}")
        col2.metric("📖 Genres", f"{num_genres}")
        col3.metric("⭐ Avg Rating", f"{avg_rating:.2f}")
        col4.metric("💶 Avg Price (€)", f"{avg_price:.2f}")

        st.subheader("🔹 K-Means Validation — Elbow & Silhouette")
        st.image("visualizations/kmeans_elbow_silhouette_combined.png", use_container_width=True)

        st.subheader("🔹 PCA Clusters (k = 2)")
        st.image("visualizations/pca_clusters_k2.png", use_container_width=True)

        st.subheader("🔹 Book Count by Genre (Filtered Data)")
        import matplotlib.pyplot as plt
        genre_counts = filtered_df["genre"].value_counts().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(8, 4))
        genre_counts.head(15).plot(kind="bar", ax=ax)
        ax.set_title("Top Genres (Filtered Data)")
        ax.set_xlabel("Genre")
        ax.set_ylabel("Count")
        st.pyplot(fig)

        st.subheader("📚 Cluster Summary — Detailed Genre Composition (k = 2)")
        cluster_genre_summary = (
            df.groupby(["cluster", "genre"])
            .agg(Count=("title", "count"),
                 Avg_Rating=("avg_rating", "mean"),
                 Avg_Price_EUR=("price", "mean"))
            .reset_index()
        )
        cluster_totals = cluster_genre_summary.groupby("cluster")["Count"].transform("sum")
        cluster_genre_summary["Proportion (%)"] = (cluster_genre_summary["Count"] / cluster_totals * 100).round(2)
        cluster_genre_summary = cluster_genre_summary.sort_values(["cluster", "Count"], ascending=[True, False])
        cluster_genre_top = cluster_genre_summary.groupby("cluster").head(8)

        st.dataframe(
            cluster_genre_top.rename(columns={
                "cluster": "Cluster",
                "genre": "Genre",
                "Count": "Count",
                "Proportion (%)": "Proportion (%)",
                "Avg_Rating": "Avg Rating",
                "Avg_Price_EUR": "Avg Price (€)"
            }),
            use_container_width=True
        )
    else:
        st.warning("⚠️ No data available for the selected filters.")
