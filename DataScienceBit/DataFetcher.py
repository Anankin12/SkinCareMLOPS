import kagglehub

# Download latest version
path = kagglehub.dataset_download("sephora-products-and-skincare-reviews")

print("Path to dataset files:", path)