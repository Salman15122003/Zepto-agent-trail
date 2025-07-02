#!/usr/bin/env bash

# Only start FastAPI — Chrome is managed by undetected_chromedriver
uvicorn main:app --host 0.0.0.0 --port 8000
