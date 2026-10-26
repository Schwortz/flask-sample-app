# run.py
import os

import uvicorn

from app import app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))  # Default to 5001 if PORT env var is not set
    uvicorn.run(app, host='0.0.0.0', port=port)
