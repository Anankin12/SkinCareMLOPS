import os
import requests
from zipfile import ZipFile
from io import BytesIO

def download_and_extract_kaggle_dataset(dataset_url, download_dir="data"):
    """
    Downloads and extracts a Kaggle dataset from a public URL.

    Args:
        dataset_url (str): Public URL of the Kaggle dataset zip file.
        download_dir (str): Directory where the dataset will be saved and extracted.
    """
    try:
        # Ensure the download directory exists
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        print(f"Downloading dataset from: {dataset_url}")
        response = requests.get(dataset_url, stream=True)
        response.raise_for_status()  # Check if the request was successful
        
        # Extract the zip file in memory
        with ZipFile(BytesIO(response.content)) as zip_file:
            print(f"Extracting files to: {download_dir}")
            zip_file.extractall(download_dir)
        
        print(f"Dataset downloaded and extracted successfully to '{download_dir}'")
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the dataset: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Public URL to the Kaggle dataset ZIP file
    dataset_url = "https://www.kaggle.com/datasets/nadyinky/sephora-products-and-skincare-reviews/download?datasetVersionNumber=1"

    # Call the function to download and extract the dataset
    download_and_extract_kaggle_dataset(dataset_url)
