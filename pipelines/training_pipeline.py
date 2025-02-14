import logging
import os
import shutil
import sys

import kagglehub
import pandas as pd
from scipy import sparse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("pipeline.log")],
)
logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.clustering import cluster_products
from src.data_processing import DataProcessing


def load_data(raw_data_dir: str):
    logger.info("Starting data download from KaggleHub...")

    try:
        path = kagglehub.dataset_download("kingabzpro/cosmetics-datasets")
        logger.info(f"Files downloaded to: {path}")

        # Move files to raw_data_dir
        files = os.listdir(path)
        logger.info(f"Files found: {files}")

        for csv in files:
            full_file_path = os.path.join(path, csv)
            logger.info(
                f"Checking {full_file_path}... Is file: {os.path.isfile(full_file_path)}"
            )
            if os.path.isfile(full_file_path):
                shutil.move(full_file_path, os.path.join(raw_data_dir, csv))
                logger.info(f"Moved {csv} to {raw_data_dir}")

    except Exception as e:
        logger.error(f"Error loading data: {e}", exc_info=True)


def cleaning_dataset(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Starting dataset cleaning...")

    try:
        data_processer = DataProcessing(df)

        data_processer.apply_processing()  # Process ingredient strings
        data_processer.water_or_silicone()  # Add water/silicone-based columns
        df_clean = data_processer.dropping_no_ingredients()  # Drop invalid rows

        logger.info("Dataset cleaning completed successfully.")
        return df_clean

    except Exception as e:
        logger.error(f"Error during data cleaning: {e}", exc_info=True)
        raise


def train_pipeline(
    raw_data_dir: str, processed_data_dir: str, matrix_dir: str, n_clusters: int
):
    logger.info("Starting training pipeline...")

    try:
        # # Load data
        # load_data(raw_data_dir)

        # Read and process the data
        data_path = os.path.join(raw_data_dir, "cosmetics.csv")
        if not os.path.exists(data_path):
            logger.error(f"Data file {data_path} not found!")
            return

        logger.info(f"Reading raw data from {data_path}")
        df = pd.read_csv(data_path)
        df_clean = cleaning_dataset(df)

        # Cluster data
        logger.info("Starting product clustering...")
        df_clustered, tfidf_matrix = cluster_products(df_clean, n_clusters)
        logger.info("Product clustering completed.")

        # Save processed data
        processed_file = os.path.join(processed_data_dir, "clean_cosmetics_data.csv")
        matrix_file = os.path.join(matrix_dir, "tfidf_matrix.npz")

        df_clustered.to_csv(processed_file, index=False, sep=";")
        sparse.save_npz(matrix_file, tfidf_matrix)

        logger.info(f"Processed data saved to {processed_file}")
        logger.info(f"TF-IDF matrix saved to {matrix_file}")
        logger.info("Training pipeline completed successfully.")

    except Exception as e:
        logger.error(f"Error in training pipeline: {e}", exc_info=True)


if __name__ == "__main__":

    raw_data_dir = "data/raw"
    processed_data_dir = "data/processed"
    matrix_dir = "models"
    n_clusters = 3

    train_pipeline(raw_data_dir, processed_data_dir, matrix_dir, n_clusters)
