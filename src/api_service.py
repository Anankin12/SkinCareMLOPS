from fastapi import FastAPI
import pandas as pd
import joblib
import os
from pydantic import BaseModel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Paths
MODEL_PATH = os.path.join("notebooks", "kmeans_model.pkl")
DATA_PATH = os.path.join("notebooks", "clean_cosmetics_data.csv")

# Load Data & Model **Once**
df = pd.read_csv(DATA_PATH)
kmeans = joblib.load(MODEL_PATH)

# **Compute TF-IDF only once at startup**
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['ingredients_text'])

# Initialize FastAPI
app = FastAPI()

# API Request Model
class RecommendationRequest(BaseModel):
    skin_type: str
    label_filter: str = "All"
    rank_filter: tuple[float, float] = (4.0, 5.0)
    brand_filter: str = "All"
    price_range: tuple[int, int] = (10, 100)
    ingredient_input: str = None
    num_recommendations: int = 5

# **Updated Recommendation Function**
def recommend_products(skin_type, label_filter, rank_filter, brand_filter, price_range, ingredient_input, num_recommendations):
    recommended_products = df[df[skin_type] == 1]

    if label_filter != 'All':
        recommended_products = recommended_products[recommended_products['Label'] == label_filter]

    recommended_products = recommended_products[
        (recommended_products['Rank'] >= rank_filter[0]) & 
        (recommended_products['Rank'] <= rank_filter[1])
    ]

    if brand_filter != 'All':
        recommended_products = recommended_products[recommended_products['Brand'] == brand_filter]

    recommended_products = recommended_products[
        (recommended_products['Price'] >= price_range[0]) & 
        (recommended_products['Price'] <= price_range[1])
    ]

    if ingredient_input:
        input_vec = vectorizer.transform([ingredient_input])  # ✅ Use precomputed vectorizer
        cosine_similarities = cosine_similarity(input_vec, tfidf_matrix).flatten()
        recommended_indices = cosine_similarities.argsort()[-num_recommendations:][::-1]
        ingredient_recommendations = df.iloc[recommended_indices]
        recommended_products = recommended_products[recommended_products.index.isin(ingredient_recommendations.index)]

    return recommended_products[['Name', 'Label', 'Brand', 'Price', 'Rank']].sort_values(by='Rank', ascending=False).head(num_recommendations).to_dict(orient='records')

# API Endpoint
@app.post("/recommend")
def get_recommendations(request: RecommendationRequest):
    recommendations = recommend_products(
        request.skin_type,
        request.label_filter,
        request.rank_filter,
        request.brand_filter,
        request.price_range,
        request.ingredient_input,
        request.num_recommendations
    )
    return {"recommendations": recommendations}
