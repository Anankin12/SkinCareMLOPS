import sys, os
# Add the parent directory to sys.path so that src can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import pytest
from src.inference import RecommendationEngine

def create_dummy_df():
    # Create a DataFrame with the necessary columns.
    data = {
        "secondary_category": ["Cosmetics", "Cosmetics", "Skincare"],
        "Principal_Ingredient": ["Water", "Water", "Silicone"],
        "skin_tone": ["Light", "Fair", "Light"],
        "skin_type": ["Normal", "Oily", "Normal"],
        "ingredients_cleaned": [
            "pure water natural", 
            "filtered water hydrating", 
            "silicone-based smooth"
        ],
        "rating": [4.5, 3.0, 5.0]
    }
    return pd.DataFrame(data)

def test_recommendations_match():
    """
    Test that the recommendation function returns matching products when there is a match.
    """
    df = create_dummy_df()
    engine = recommendation_engine(df)
    # Use parameters that should match at least the first row:
    # secondary_category "Cosmetics", ingredient_preference "Water", skin tone "Light", skin type "Normal"
    result = engine.recommendation_function("Cosmetics", "Water", "Light", "Normal", n_recommendations=5)
    
    # The function should return a non-empty DataFrame and include a similarity_score column.
    assert not result.empty, "Expected non-empty results when products match."
    assert "similarity_score" in result.columns, "Result should have a 'similarity_score' column."
    
    # Verify that every row in the result matches the filter criteria.
    for _, row in result.iterrows():
        assert row["secondary_category"].lower() == "cosmetics"
        assert row["Principal_Ingredient"].lower() == "water"
        assert row["skin_tone"].lower() == "light"
        assert row["skin_type"].lower() == "normal"

def test_recommendations_no_match():
    """
    Test that the recommendation function returns an empty DataFrame when no products match.
    """
    df = create_dummy_df()
    engine = recommendation_engine(df)
    # Use parameters that are unlikely to match any row.
    result = engine.recommendation_function("Skincare", "Water", "Dark", "Dry", n_recommendations=5)
    
    # The function should return an empty DataFrame.
    assert result.empty, "Expected empty results when no products match the criteria."

def test_recommendation_limit():
    """
    Test that the recommendation function returns no more than the requested number of recommendations.
    """
    # Create a DataFrame with two matching rows.
    data = {
        "secondary_category": ["Cosmetics", "Cosmetics"],
        "Principal_Ingredient": ["Water", "Water"],
        "skin_tone": ["Light", "Light"],
        "skin_type": ["Normal", "Normal"],
        "ingredients_cleaned": ["water fresh", "water pure"],
        "rating": [4.0, 5.0]
    }
    df = pd.DataFrame(data)
    engine = recommendation_engine(df)
    
    # Request only 1 recommendation.
    result = engine.recommendation_function("Cosmetics", "Water", "Light", "Normal", n_recommendations=1)
    assert len(result) == 1, "Should return exactly 1 recommendation when n_recommendations is set to 1."
