import unittest

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from src.clustering import cluster_products


class TestClusterProducts(unittest.TestCase):

    def setUp(self):
        """
        Create a sample DataFrame for testing.
        """
        self.df = pd.DataFrame(
            {
                "ingredients_text": [
                    "tomato, onion, garlic",
                    "cheese, tomato sauce, basil",
                    "sugar, flour, butter",
                    "milk, eggs, vanilla",
                    "chicken, salt, pepper",
                ]
            }
        )

    def test_output_types(self):
        """
        Test that the function returns a DataFrame and a KMeans model.
        """
        df_result, matrix = cluster_products(self.df, n_clusters=2)

        self.assertIsInstance(df_result, pd.DataFrame)
        self.assertIsInstance(matrix, TfidfVectorizer)

    def test_cluster_column_created(self):
        """
        Test that the 'ingredient_cluster' column is created.
        """
        df_result, _ = cluster_products(self.df, n_clusters=2)
        self.assertIn("ingredient_cluster", df_result.columns)

    def test_correct_number_of_clusters(self):
        """
        Test that the number of unique clusters matches the requested n_clusters.
        """
        n_clusters = 3
        df_result, _ = cluster_products(self.df, n_clusters=n_clusters)
        unique_clusters = df_result["ingredient_cluster"].nunique()

        self.assertEqual(unique_clusters, n_clusters)


if __name__ == "__main__":
    unittest.main()
