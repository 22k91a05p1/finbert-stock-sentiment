import sqlalchemy
from sqlalchemy import create_engine, text
import pandas as pd

# 1. Connection Details
DB_USER = "user"
DB_PASS = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "stock_sentiment"

# 2. Connection String
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 3. THE MISSING FUNCTION
def get_db_engine():
    return create_engine(DATABASE_URL)

def init_db():
    engine = get_db_engine()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS sentiment_data (
        id SERIAL PRIMARY KEY,
        title TEXT,
        sentiment TEXT,
        confidence FLOAT,
        date TIMESTAMP
    );
    """
    with engine.connect() as conn:
        conn.execute(text(create_table_query))
        conn.commit()
        print("--- ✅ Database Table 'sentiment_data' is ready! ---")

if __name__ == "__main__":
    init_db()