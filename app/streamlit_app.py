# Library needed for the actual site
import streamlit as st

# Library needed for loading the model and data handling 
import joblib
import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Library needed fot the API calls
import requests

# Paths
MODEL_PATH = os.path.join("notebooks", "kmeans_model.pkl")
DATA_PATH = os.path.join("notebooks", "clean_cosmetics_data.csv")

# API URL
api_url = "http://localhost:8000/recommend"

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

# Load the trained K-Means model
@st.cache_data
def load_model():
    return joblib.load(MODEL_PATH)

kmeans = load_model()

# Precompute TF-IDF vectorizer for ingredients
@st.cache_data
def compute_tfidf():
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['ingredients_text'])
    return vectorizer, tfidf_matrix

vectorizer, tfidf_matrix = compute_tfidf()

# Recommendation function
def recommend_cosmetics(skin_type, label_filter, rank_filter, brand_filter, price_range, ingredient_input=None, num_recommendations=5):
    # Filter by Skin Type
    recommended_products = df[df[skin_type] == 1]

    # Filter by Label (Product Type)
    if label_filter != 'All':
        recommended_products = recommended_products[recommended_products['Label'] == label_filter]

    # Filter by Rank
    recommended_products = recommended_products[
        (recommended_products['Rank'] >= rank_filter[0]) & 
        (recommended_products['Rank'] <= rank_filter[1])
    ]

    # Filter by Brand
    if brand_filter != 'All':
        recommended_products = recommended_products[recommended_products['Brand'] == brand_filter]

    # Filter by Price Range
    recommended_products = recommended_products[
        (recommended_products['Price'] >= price_range[0]) & 
        (recommended_products['Price'] <= price_range[1])
    ]

    # Ingredient Similarity Matching
    if ingredient_input:
        input_vec = vectorizer.transform([ingredient_input])
        cosine_similarities = cosine_similarity(input_vec, tfidf_matrix).flatten()
        recommended_indices = cosine_similarities.argsort()[-num_recommendations:][::-1]
        ingredient_recommendations = df.iloc[recommended_indices]
        recommended_products = recommended_products[recommended_products.index.isin(ingredient_recommendations.index)]

    # Return top results
    return recommended_products[['Name', 'Label', 'Brand', 'Price', 'Rank']].sort_values(by='Rank', ascending=False).head(num_recommendations)

# Streamlit UI
st.title("Skincare Product Recommendation System")

st.sidebar.header("Input Parameters")

# User Inputs
skin_type = st.sidebar.selectbox("Select Skin Type", ["Dry", "Oily", "Combination", "Normal"])
label_filter = st.sidebar.selectbox("Select Product Type", ["All"] + df["Label"].unique().tolist())
brand_filter = st.sidebar.selectbox("Select Brand", ["All"] + df["Brand"].unique().tolist())
price_range = st.sidebar.slider("Select Price Range", min_value=int(df["Price"].min()), max_value=int(df["Price"].max()), value=(10, 100))
rank_filter = st.sidebar.slider("Select Rank Range", min_value=float(df["Rank"].min()), max_value=float(df["Rank"].max()), value=(4.0, 5.0))
ingredient_input = st.sidebar.text_input("Enter a Key Ingredient (Optional)")

if st.sidebar.button("Get Recommendation"):
    payload = {
        "skin_type": skin_type,
        "label_filter": label_filter,
        "rank_filter": rank_filter,
        "brand_filter": brand_filter,
        "price_range": price_range,
        "ingredient_input": ingredient_input,
        "num_recommendations": 5
    }

    response = requests.post(api_url, json=payload)
    results = response.json()["recommendations"]
    
    st.write("### Recommended Products")
    st.dataframe(results)
