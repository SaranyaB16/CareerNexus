#!/usr/bin/env bash
set -e

# CareerNexus One-Click Runner
cd "$(dirname "$0")"

# Activate virtual environment
source .venv/bin/activate

# Start development server
echo "🚀 Starting CareerNexus server on http://127.0.0.1:8000 ..."
echo "📖 Swagger API Docs: http://127.0.0.1:8000/docs"
uvicorn backend.main:app --reload --port 8000
