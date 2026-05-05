import pandas as pd
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Database connection parameters
DB_URL = "mysql+mysqlconnector://user:password@localhost:3306/my_database"


def fetch_titanic_data(max_retries=10, sleep_time=10):
    engine = create_engine(DB_URL)
    attempt = 1

    # Retry logic to wait for MySQL initialization
    while attempt <= max_retries:
        try:
            print(f"Attempt {attempt}/{max_retries}: Connecting...")
            df = pd.read_sql("SELECT * FROM titanic", con=engine)
            return df
        except OperationalError:
            print(f"Database not ready. Waiting {sleep_time}s...")
            time.sleep(sleep_time)
            attempt += 1

    raise Exception("Could not connect to MySQL.")


if __name__ == "__main__":
    # Fetch data and print results
    try:
        titanic_df = fetch_titanic_data()
        print("\nData loaded successfully!")
        print(f"Total rows: {len(titanic_df)}")
        print("\nFirst 5 rows:")
        print(titanic_df.head())

        # Verify NULL handling for key columns
        print("\nNULL check:")
        print(titanic_df[['Age', 'Cabin', 'Embarked']].isnull().sum())
    except Exception as e:
        print(f"Error: {e}")