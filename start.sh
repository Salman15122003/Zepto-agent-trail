#!/usr/bin/env bash

# Start Chrome in headless mode
google-chrome-stable --headless --no-sandbox --disable-dev-shm-usage &

# Start the FastAPI app using uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
