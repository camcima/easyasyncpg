import os

import pytest
from dotenv import load_dotenv

# Load .env file
load_dotenv()


@pytest.fixture(scope="module")
def db_config() -> dict:
    return {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
        "port": int(os.getenv("DB_PORT", "5432")),
    }
