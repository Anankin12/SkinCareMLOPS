# Use a base image with Python 3.12.3 (Bullseye variant)
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Set the working directory to /workspace (repository root inside container)
WORKDIR /workspace

# Copy only the necessary directories:
# 1. The 'app' directory (includes main.py, requirements.txt, etc.)
# 2. The 'data/processed' directory (where your CSV files reside)
COPY app /workspace/app
COPY data/processed /workspace/data/processed

# Set the working directory to the app folder where main.py is located.
WORKDIR /workspace/app

# Install Python dependencies using the requirements file from app/
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the port for the Streamlit app
EXPOSE 8501

# Run the Streamlit app in headless mode.
CMD ["streamlit", "run", "--server.headless", "true", "main.py", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]
