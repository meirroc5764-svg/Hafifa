from sqlalchemy import  MetaData, Table, Column, Integer, String, Float, Date, create_engine

# def connect_to_data():

DATABASE_URL = "postgresql+psycopg://admin:mypassword@localhost:5432/air_quality"

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