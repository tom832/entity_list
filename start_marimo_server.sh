#!/bin/bash
source .env
echo "Starting Marimo server..."
marimo run main.py --host 0.0.0.0 --port 12718 --token-password=$TOKEN_PASSWORD