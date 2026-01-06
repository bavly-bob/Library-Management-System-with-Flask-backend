import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-change-me"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f"sqlite:///{BASE_DIR / 'library.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False