FROM python:3.10.12

RUN apt-get update && apt-get install -y make

WORKDIR /app

COPY requirements.txt .

# create data directories
RUN mkdir -p data/raw data/processed 
RUN pip install --no-cache-dir -r requirements.txt

COPY data/raw/ data/raw/
COPY requirements.txt .
COPY makefile .

# Copy the application code
COPY src/ ./src/
COPY pipelines/ ./pipelines/
COPY pages/ ./pages/
COPY homepage.py .

# Expose Streamlit's default port
EXPOSE 8501

CMD ["make", "containerpipeline"]