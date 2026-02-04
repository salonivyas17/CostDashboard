import os

# Use environment variable names; set these in your shell or deployment (never commit values).
DATABASE_URL = os.getenv("DATABASE_URL")
BLOB_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
