from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd 
import joblib

def cluster_products(df: pd.Dataframe, n_clusters: int) -> pd.Dataframe: 

    # converting text data to numerical data
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['ingredients_text'])

    # clustering the data
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(tfidf_matrix)
    df['ingredient_cluster'] = cluster_labels

    # Save the trained K-Means model
    joblib.dump(kmeans, "../models/kmeans_model.pkl")

    return df


