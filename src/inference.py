import pandas as pd


def find_similar_products(df: pd.DataFrame, product_id: int, n: int) -> pd.DataFrame:

    pass


def recommendation(
    df: pd.DataFrame, skin_type: str, ingredient: str, n: int
) -> pd.DataFrame:
    """
    Recommend n items to a user based on the highest predicted rating
    """
    # Start filtering based on skin type
    recommended_products = df[df[skin_type] == 1]
    recommended_products = recommended_products[recommended_products[ingredient] == 1]

    # Sort by predicted rating
    recommended_products = recommended_products.sort_values(by="Rank", ascending=False)

    return recommended_products[:n]
