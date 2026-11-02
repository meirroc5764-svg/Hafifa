from sqlalchemy import  MetaData, Table, Column, Integer, String, Float, Date, create_engine
from dotenv import load_dotenv
import os


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
engine = create_engine(DATABASE_URL)

metadata = MetaData()

air_quality = Table(
    "air_quality",
    metadata,

    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("date", Date),
    Column("city", String(100)),
    Column("PM2.5", Float),
    Column("NO2", Float),
    Column("CO2", Float)
)


def create_tables():
    metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()
    print("Tables created successfully!")