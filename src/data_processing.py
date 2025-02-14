import string

import pandas as pd


class DataProcessing:

    water_keywords = ["water"]
    silicone_keywords = [
        "cyclopentasiloxane",
        "cyclohexasiloxane",
        "dimethicone",
        "silicone",
    ]

    def __init__(self, df):
        self.df = df

    def process_ingredients(self, ingredient_str):

        ingredient_str = ingredient_str.lower()
        # Split by comma
        ingredients_list = ingredient_str.split(",")

        ingredients_list = [
            ingredient.strip().translate(str.maketrans("", "", string.punctuation))
            for ingredient in ingredients_list
        ]
        return ingredients_list

    def ingredients_to_string(self, ingredients_list):
        return " ".join(ingredients_list)

    def apply_processing(self):
        """
        Applies the processing functions to the specified column of the DataFrame.
        """
        self.df["Processed_Ingredients"] = self.df["Ingredients"].apply(
            self.process_ingredients
        )
        self.df["ingredients_text"] = self.df["Processed_Ingredients"].apply(
            self.ingredients_to_string
        )

    def water_or_silicone(self):
        """
        Creates two new columns in the DataFrame, one for water-based products and one for silicone-based products.
        return 2 boolean columns
        """
        self.df["water_based"] = self.df["Processed_Ingredients"].apply(
            lambda ingredients: any(
                keyword in ingredients for keyword in self.water_keywords
            )
        )

        self.df["silicone_based"] = self.df["Processed_Ingredients"].apply(
            lambda ingredients: any(
                keyword in ingredients for keyword in self.silicone_keywords
            )
        )

    def dropping_no_ingredients(self) -> pd.DataFrame:
        """
        Drops the rows that contain 'visit the' or 'no info' in the 'Ingredients' column.
        return the final DataFrame
        """

        placeholder_mask = self.df["Ingredients"].str.contains(
            "visit the", case=False, na=False
        )
        no_info_mask = self.df["Ingredients"].str.contains(
            "no info", case=False, na=False
        )

        # Combine both masks using the OR operator
        combined_mask = placeholder_mask | no_info_mask

        df_clean = self.df[~combined_mask].reset_index(drop=True)

        return df_clean
