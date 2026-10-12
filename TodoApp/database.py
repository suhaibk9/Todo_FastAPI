from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "todosApp.db"
DEFAULT_DB_URL = f"sqlite:///{DEFAULT_DB_PATH}"

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)
if SQLALCHEMY_DATABASE_URL in ("sqlite:///./todosApp.db", "sqlite:///todosApp.db"):
    SQLALCHEMY_DATABASE_URL = DEFAULT_DB_URL

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
