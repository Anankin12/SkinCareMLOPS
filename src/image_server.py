from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Define the directory where cached images are stored
CACHE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "cached_images"))

@app.route('/images/<path:filename>')
def serve_image(filename):
    """Serve an image from the cached_images directory."""
    return send_from_directory(CACHE_DIR, filename)

if __name__ == '__main__':
    # Allow external access (change port if needed)
    app.run(host='0.0.0.0', port=8000, debug=True)
