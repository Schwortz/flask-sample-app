# run.py
# Entry point for the Flask sample app.
# Run with: python run.py (after: pip install -r requirements.txt)
# Listens on 0.0.0.0; the port comes from the PORT environment variable
# and defaults to 5001.
import os

from app import app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001)) # Default to 5000 if PORT env var is not set
    app.run(host='0.0.0.0', port=port)
