from utils.data_processing import DataProcessing
import unittest
import pandas as pd


class TestDataProcessing(unittest.TestCase):
    
    def setUp(self):
        data = {'Ingredients': [
            "Water, Dimethicone, Glycerin",
            "Cyclopentasiloxane, Alcohol, Water",
            "Visit the website for details",
            "No info available",
            "Cyclohexasiloxane, Dimethicone"
        ]}
        self.df = pd.DataFrame(data)
        self.processor = DataProcessing(self.df)
    
    def test_process_ingredients(self):
        result = self.processor.process_ingredients("Water, Dimethicone, Glycerin")
        expected = ["water", "dimethicone", "glycerin"]
        self.assertEqual(result, expected)
    
    def test_ingredients_to_string(self):
        ingredients_list = ["water", "dimethicone", "glycerin"]
        result = self.processor.ingredients_to_string(ingredients_list)
        expected = "water dimethicone glycerin"
        self.assertEqual(result, expected)
    
    def test_apply_processing(self):
        self.processor.apply_processing()
        expected_values = [
            "water dimethicone glycerin",
            "cyclopentasiloxane alcohol water",
            "visit the website for details",
            "no info available",
            "cyclohexasiloxane dimethicone"
        ]
        self.assertListEqual(self.processor.df['ingredients_text'].tolist(), expected_values)
    
    def test_water_or_silicone(self):
        self.processor.apply_processing()
        self.processor.water_or_silicone()
        expected_water = [True, True, False, False, False]
        expected_silicone = [True, True, False, False, True]
        self.assertListEqual(self.processor.df['water_based'].tolist(), expected_water)
        self.assertListEqual(self.processor.df['silicone_based'].tolist(), expected_silicone)
    
    def test_dropping_no_ingredients(self):
        result_df = self.processor.dropping_no_ingredients()
        expected_ingredients = [
            "Water, Dimethicone, Glycerin",
            "Cyclopentasiloxane, Alcohol, Water",
            "Cyclohexasiloxane, Dimethicone"
        ]
        self.assertListEqual(result_df['Ingredients'].tolist(), expected_ingredients)

if __name__ == "__main__":
    unittest.main()
