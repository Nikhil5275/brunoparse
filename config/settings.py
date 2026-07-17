"""Global configuration for STARs RAG Agent"""
import os
from dotenv import load_dotenv

load_dotenv()

# GCP Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
BQ_DATASET = os.getenv("BQ_DATASET", "stars_data")

# Contract defaults
# DEFAULT_CONTRACT = "H1234"
# DEFAULT_YEAR = 2025

# Model configuration
ROUTER_MODEL = "gemini-2.0-flash"
POD_MODEL = "gemini-2.5-pro"
SYNTHESIZER_MODEL = "gemini-2.5-pro"
