import logging
import os
import sys

import pandas as pd
from scipy import sparse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
) 
logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.new_data_processing import DataProcessing


def cleaning_dataset(products_df: pd.DataFrame, review_df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Starting dataset cleaning...")

    try:
        data_processer = DataProcessing(products_df, review_df)
        data_processer.merge_dataframes()
        data_processer.nan_handler()
        data_processer.apply_processing()
        data_processer.water_or_silicone()

        logger.info("Dataset cleaning completed successfully.")
        return data_processer.merged_df

    except Exception as e:
        logger.error(f"Error during data cleaning: {e}", exc_info=True)
        raise


def training_pipeline():
    pass 


if __name__ == "__main__":

    INPUT_DATA_DIR = "data/raw"
    OUTPUT_DATA_DIR = "data/processed"
    TFIDF_MATRIX_DIR = "models"
    CLUSTERS = 3

    training_pipeline(INPUT_DATA_DIR, OUTPUT_DATA_DIR, TFIDF_MATRIX_DIR, CLUSTERS)