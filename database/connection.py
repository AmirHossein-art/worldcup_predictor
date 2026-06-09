from dotenv import load_dotenv

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

print(
    "DATABASE_URL FOUND:",
    DATABASE_URL is not None
)

if DATABASE_URL:

    DB_MODE = "NEON"

    engine = create_engine(
        DATABASE_URL,
        echo=False
    )

else:

    DB_MODE = "LOCAL"

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")


    DATABASE_URL = (
        f"postgresql+psycopg2://"
        f"{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


    engine = create_engine(
        DATABASE_URL,
        echo=False
    )

print(
    f"========== DATABASE MODE: {DB_MODE} =========="
)   

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()

if DB_MODE == "NEON":
    print("Connected to Neon PostgreSQL")

else:
    print(
        f"Connected to Local PostgreSQL ({DB_NAME})"
    )