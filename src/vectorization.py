from sklearn.feature_extraction.text import TfidfVectorizer
import ast

class Vectorizer:

    def __init__(self, df):
        self.df = df 

    
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
    

    def preprocessing(self, columns_to_vectorize): 
        """
        Preprocesses the DataFrame by dropping duplicates and resetting the index
        """
        self.df.drop_duplicates(subset=['product_id'], inplace=True)
        self.df.reset_index(drop=True, inplace=True)

        self.df['column_to_vectorize'] = self.df[columns_to_vectorize].values.tolist()
        
        self.df['attributes_cleaned'] = self.df['column_to_vectorize'].apply(self.ingredients_to_string)
        self.df.drop(columns=['column_to_vectorize'], axis=1, inplace=True)
    
    def vectorization(self): 
        """
        Vectorizes the text data in the DataFrame using the TF-IDF method.
        """
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.tfidf_matrix = vectorizer.fit_transform(self.df['attributes_cleaned'])
        