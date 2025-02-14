import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer


def cluster_products(df: pd.DataFrame, n_clusters: int) -> pd.DataFrame:

    # converting text data to numerical data
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(df["ingredients_text"])

    # clustering the data
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(tfidf_matrix)
    df["ingredient_cluster"] = cluster_labels

    return df, tfidf_matrix
