import pandas as pd
from src.database import get_db_engine

def check_data():
    print("--- 🕵️ CHECKING DATABASE ---")
    engine = get_db_engine()
    
    # Read the table directly into a DataFrame
    try:
        df = pd.read_sql("SELECT * FROM sentiment_data", engine)
        if df.empty:
            print("The table is empty.")
        else:
            print(f"✅ Found {len(df)} rows in the database:\n")
            print(df[['date', 'sentiment', 'title']].to_string(index=False))
            print("\nSUCCESS: Data is safely stored in PostgreSQL!")
            
    except Exception as e:
        print(f"❌ Error reading database: {e}")

if __name__ == "__main__":
    check_data()