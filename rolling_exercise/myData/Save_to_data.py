from sqlalchemy import insert

from myData.data_connect import engine, air_quality, alert


def insert_all_data(df):
    records = df.to_dict(orient="records")

    try:
        with engine.begin() as connection:
            connection.execute(
                insert(air_quality),
                records
            )

        print(f"Inserted {len(records)} records successfully!")
    except Exception as e:
        print(f"the exception: {e}")


def insert_alert(df):
    records = df.to_dict(orient="records")
 
    try:
        with engine.begin() as connection:
            connection.execute(
                insert(alert),
                records
            )

        print(f"Inserted {len(records)} records successfully!")
    except Exception as e:
        print(f"the Exeption: {e}")
