import logging
import os
import sys
import pandas as pd


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
) 
logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data_processing import DataProcessing


def data_loading(input_data_dir: str) -> tuple:
    """
    Load the raw data from the input directory.
    return: tuple of DataFrames
    """
    
    files = os.listdir(input_data_dir)
    reviews_files = [f for f in files if "reviews" in f]

    try:
        products_df = pd.read_csv(os.path.join(input_data_dir, "product_info.csv"))
        reviews_l = []
        for review_file in reviews_files:
            partial_review_df = pd.read_csv(os.path.join(input_data_dir, review_file), index_col=0, 
                                            dtype={'author_id': 'str'}, low_memory=False)
            
            reviews_l.append(partial_review_df)

        review_df = pd.concat(reviews_l, axis=0)

        logger.info("Data loading completed successfully.")
        return products_df, review_df

    except Exception as e:
        logger.error(f"Error during data loading: {e}", exc_info=True)
        raise

def cleaning_dataset(products_df: pd.DataFrame, review_df: pd.DataFrame) -> pd.DataFrame:

    """
    Clean the dataset by merging the products and reviews DataFrames, handling NaN values,
    classifying the products as water-based or silicone-based, and applying the necessary processing.
    return: cleaned DataFrame
    """

    logger.info("Starting dataset cleaning...")

    try:
        data_processer = DataProcessing(products_df, review_df)
        data_processer.merge_dataframes()
        data_processer.nan_handler()
        data_processer.water_or_silicone()
        data_processer.category_classification()
        data_processer.apply_processing()

        logger.info("Dataset cleaning completed successfully.")
        return data_processer.merged_df

    except Exception as e:
        logger.error(f"Error during data cleaning: {e}", exc_info=True)
        raise

def training_pipeline(input_data_dir: str, output_data_dir: str) -> None:
    """
    Run the training pipeline by loading the data, cleaning the dataset, and saving the cleaned data.
    """
    
    logger.info("Starting training pipeline...")
    try:
        products_df, review_df = data_loading(input_data_dir)
        cleaned_df = cleaning_dataset(products_df, review_df)
        cleaned_df.to_csv(os.path.join(output_data_dir, "cleaned_data.csv"), index=False, sep=";")
        logger.info("Training pipeline completed successfully.")

    except Exception as e:
        logger.error(f"Error during training pipeline: {e}", exc_info=True)
        raise

if __name__ == "__main__":

    INPUT_DATA_DIR = "data/raw"
    OUTPUT_DATA_DIR = "data/processed"

    training_pipeline(INPUT_DATA_DIR, OUTPUT_DATA_DIR)