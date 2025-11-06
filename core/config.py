from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    # 30 minutes by default
    INTERVAL_MINUTES = int(os.getenv("INTERVAL_MINUTES", 30))
    DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/pricewatcher.db")
