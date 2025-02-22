import ast
import pandas as pd

class DataProcessing:

    columns_to_drop = ['variation_desc', 'sale_price_usd', 'value_price_usd', 'child_max_price', 'child_min_price',            
                       'helpfulness','review_title','tertiary_category','highlights','variation_value',            
                       'variation_type', 'size','total_feedback_count','total_neg_feedback_count',   
                       'total_pos_feedback_count','submission_time', 'limited_edition',            
                       'sephora_exclusive','child_count', 'brand_id', 'online_only', 'new', 
                       'out_of_stock', 'reviews', 'is_recommended', 'review_text']

    critical_columns = ['ingredients', 'author_id', 'rating', 
                        'product_name', 'brand_name', 'price_usd','secondary_category']
    
    user_attribute_columns = ['skin_tone', 'eye_color', 'skin_type', 'hair_color']

    water_keywords = ['water', 'aqua', 'hydrosol']

    silicone_keywords = ['cyclopentasiloxane', 'cyclohexasiloxane', 'dimethicone',
                         'trimethicone', 'amodimethicone', 'vinyl dimethicone', 
                         'cetyl dimethicone', 'phenyl trimethicone','silicone']
    
    category_map = {
        "Cosmetics": ["Moisturizers", "Treatments", "Cleansers", "Masks", "Lip Balms & Treatments", "Sunscreen", "Self Tanners"],
        "Eye Care": ["Eye Care"],
        "Random": ["Mini Size", "Value & Gift Sets", "Wellness", "High Tech Tools", "Shop by Concern"]
    }


    def __init__(self, products_df, reviews_df):
        self.products_df = products_df
        self.reviews_df = reviews_df

    
    def cols_to_use(self):
        """
        Returns the columns to use from the products_df and reviews_df DataFrames
        """
        cols_to_use = self.products_df.columns.difference(self.reviews_df.columns)
        cols_to_use = list(cols_to_use)
        cols_to_use.append('product_id')
        return cols_to_use
    

    def merge_dataframes(self):
        """
        Merges the products_df and reviews_df DataFrames on the 'product_id' column and drop unnecessary columns
        """
        cols_to_use = self.cols_to_use()
        self.merged_df = pd.merge(self.reviews_df, self.products_df[cols_to_use], how='outer', on=['product_id', 'product_id'])
        self.merged_df.drop(columns=self.columns_to_drop, inplace=True, axis=1)
        self.merged_df.drop_duplicates(subset=['product_id'], inplace=True)
    

    def nan_handler(self):
        """
        Fills NaN values in the DataFrame with empty strings
        """
        self.merged_df.dropna(subset=self.critical_columns, how='any', inplace=True)

        for col in self.user_attribute_columns:
            self.merged_df[col].fillna('Unknown', inplace=True)
        
        self.merged_df.drop(columns=['primary_category'], axis=1, inplace=True)
    
    
    def ingredients_to_string(self, ingredients_list):
        """
        Convert a string representation of a list into a single string.
        
        Parameters:
            val (str): A string that represents a list, e.g., "['Water, Butylene Glycol, ...']".
            
        Returns:
            str: A single string with all the list items joined by a space.
        """
        try:
            items = ast.literal_eval(ingredients_list)

            if isinstance(items, list):
                return " ".join(items)
            else:
                return ingredients_list
            
        except Exception as e:
            return ingredients_list
    

    def apply_processing(self):
        """
        Applies the processing functions to the specified column of the DataFrame.
        """
        self.merged_df['ingredients_cleaned'] = self.merged_df['ingredients'].apply(self.ingredients_to_string)
        self.merged_df.drop(columns=['ingredients'], axis=1, inplace=True)

    def classify_ingredient(self, ingredients):
        """
        Classifies the principal ingredient of a product as either water-based or silicone-based.
        """

        ingredients = ingredients.lower()
        if any(keyword in ingredients for keyword in self.water_keywords):
            return "Water"
        elif any(keyword in ingredients for keyword in self.silicone_keywords):
            return "Silicone"
        return None

    def water_or_silicone(self):
        """
        Creates two new columns in the DataFrame, one for water-based products and one for silicone-based products.
        return 2 boolean columns
        """
        self.merged_df["Principal_Ingredient"] = self.merged_df['ingredients'].apply(self.classify_ingredient)
    
    
    def category_classification(self):
        """
        Creates a new column in the DataFrame, that classifies the product into a category.
        return 1 column
        """
        self.merged_df["secondary_category"] = self.merged_df["secondary_category"].apply(
        lambda cat: next((group for group, items in self.category_map.items() if cat in items), "Other")
    )

    

    

    
