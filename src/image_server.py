# image_server.py
from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)

# Define the absolute path to the cached_images directory
CACHE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "cached_images"))

@app.route('/images/<path:filename>')
def serve_image(filename):
    """Serve an image from the cached_images directory."""
    file_path = os.path.join(CACHE_DIR, filename)
    if not os.path.isfile(file_path):
        abort(404)  # Return 404 if the file doesn't exist
    return send_from_directory(CACHE_DIR, filename)

if __name__ == '__main__':
    # Allow external access
    app.run(host='0.0.0.0', port=8000, debug=True)
132