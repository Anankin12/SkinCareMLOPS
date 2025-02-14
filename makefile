# Variables
INPUT_DATA_PATH=data/raw
OUTPUT_DATA_PATH=data/processed
MODEL_PATH=models
IMAGE_NAME=mlops_webapp
CONTAINER_NAME=mlops_container
PYTHON=python3


# Create virtual environment
venv:
	$(PYTHON) -m venv venv && source venv/bin/activate

# Install dependencies
install:
	pip install -r requirements.txt


# Format code (e.g., Black, isort)
format:
	black pages/ src/ pipelines/ homepage.py && isort pages/ src/ pipelines/ homepage.py

# Run linter (e.g., flake8)
lint:
	pylint pages/ src/ pipelines/ homepage.py

# Run unit tests
test:
	pytest src/tests/

# Create directories if they don't exist
init:
	mkdir -p $(INPUT_DATA_PATH) $(OUTPUT_DATA_PATH) $(MODEL_PATH)

# Process raw data and generate final dataset and Generate TF-IDF matrix
train:
	$(PYTHON) pipelines/training_pipeline.py

webapp:
	streamlit run homepage.py

# # Build the web app container
# build:
# 	docker build -t $(IMAGE_NAME) .

# # Run the web app
# run:
# 	docker run --rm -p 8501:8501 -v $(PWD)/$(DATA_PATH):/app/data -v $(PWD)/$(MODEL_PATH):/app/models $(IMAGE_NAME)


# Full pipeline
containerpipeline: train webapp
