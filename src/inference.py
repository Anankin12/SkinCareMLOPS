import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class recommendation_engine:

    def __init__(self, df):
        self.df = df

    def recommendation_function(self, 
                                secondary_category, 
                                ingredient_preference,
                                skintone,
                                skintype,
                                n_recommendations=5):
        """
        Recommends products based on the user's preferences and the similarity of the products' attributes.
        """ 
        
        category_df = self.df[self.df['secondary_category'].str.lower() == secondary_category.lower()]
        filtered_df = category_df[category_df['Principal_Ingredient'].str.lower() == ingredient_preference.lower()]

        # 2. Further filter by user attributes.
        
        filtered_df = filtered_df[filtered_df['skin_tone'].str.lower() == skintone.lower()]
        filtered_df = filtered_df[filtered_df['skin_type'].str.lower() == skintype.lower()]
        

        if filtered_df.empty:
            return "No products found with the specified preferences."

        # Reset index to ensure alignment with tfidf_matrix
        filtered_df = filtered_df.reset_index(drop=True)

        filtered_df['composite_text'] = (filtered_df['ingredients_cleaned'] + " " + filtered_df['skin_tone'].fillna('') + " " + 
                                         filtered_df['skin_type'].fillna('') + " " + filtered_df['Principal_Ingredient'].fillna(''))
        
         # 6 Build the TF-IDF matrix on the composite text.
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(filtered_df['composite_text'])
        print(tfidf_matrix.shape)

        # 7. Build the user query from provided user attributes.
        
        if ingredient_preference.lower() == "water":
            query_text = "water aqua hydrosol"
        else:
            query_text = "silicone cyclopentasiloxane dimethicone"
        
        for attr in [query_text, skintone, skintype, ingredient_preference]:
            query_text += " " + attr
        
        input_vector = vectorizer.transform([query_text])

        # Get indices of the filtered products (assumes df and tfidf_matrix are aligned)
        valid_indices = filtered_df.index
        
        # Compute cosine similarity scores between the query and the filtered products
        similarity_scores = cosine_similarity(input_vector, tfidf_matrix[valid_indices]).flatten()
        filtered_df['similarity_score'] = similarity_scores
        filtered_df.sort_values(by=['similarity_score', 'rating'], ascending=[False, False])

        return filtered_df.head(n_recommendations)
        