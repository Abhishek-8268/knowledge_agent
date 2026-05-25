import os
from pathlib import Path

# Base project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration
DB_NAME = BASE_DIR / "ecommerce.db"

# Schema configuration
SCHEMA_PATH = BASE_DIR / "SCHEMA.md"

# Memory configuration
MEMORY_DIR = BASE_DIR / "memory_db"

# LLM Configuration
DEFAULT_MODEL = "llama-3.3-70b-versatile"
