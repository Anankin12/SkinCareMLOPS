# Use the same base image as in the testing setup devcontainer.json
FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# Set the working directory inside the container
WORKDIR /workspace

# Copy dependency files for caching
COPY requirements.txt ./

# Run package updates and install dependencies
RUN if [ -f requirements.txt ]; then \
      pip install --no-cache-dir -r requirements.txt; \
    fi && \
    pip install streamlit

# Copy the rest of your application code
COPY . .

# Expose the port on which your app will run
EXPOSE 8501

# Run the Streamlit app in headless mode (prevents email prompt)
CMD ["streamlit", "run", "--server.headless", "true", "homepage.py", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]
