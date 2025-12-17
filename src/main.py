import pandas as pd
from src.etl.scraper import fetch_hot_posts
from src.model.sentiment import analyze_sentiment
from src.database import get_db_engine

def run_pipeline():
    print("--- 🚀 STARTING GLOBAL PIPELINE ---")
    
    # 1. DEFINE MARKETS
    # We will grab data from both USA (WallStreetBets) and India (IndianStreetBets)
    subreddits = ["wallstreetbets", "IndianStreetBets"]
    
    all_posts = []

    # 2. COLLECT DATA (Loop through each market)
    for market in subreddits:
        print(f"\n--- 🌍 Fetching from r/{market} ---")
    
        market_data = fetch_hot_posts(subreddit=market, limit=25, pages=3)
        
        if not market_data.empty:
            # Add a "Market" tag so we know where it came from
            market_data['source'] = market
            all_posts.append(market_data)

    if not all_posts:
        print("No data found from any market. Exiting.")
        return

    # Combine USA and India data into one list
    full_data = pd.concat(all_posts)
    
    print(f"\n--- 🧠 ANALYZING SENTIMENT ({len(full_data)} items) ---")
    
    # 3. APPLY AI
    results = []
    for index, row in full_data.iterrows():
        title = row['title']
        label, score = analyze_sentiment(title)
        
        # Add a tag to the title so we see it in the dashboard
        # e.g. "[ISB] Tata Motors is flying"
        display_title = f"[{row['source']}] {title}"
        
        print(f"  [{label.upper()}] {display_title[:60]}...") 
        results.append({
            "title": display_title, # We save the tag in the title column
            "sentiment": label,
            "confidence": score,
            "date": row['date']
        })

    final_df = pd.DataFrame(results)

    # 4. SAVE TO DATABASE
    print("\n--- 💾 SAVING TO DATABASE ---")
    try:
        engine = get_db_engine()
        final_df.to_sql("sentiment_data", engine, if_exists="append", index=False)
        print(f"✅ Success! Saved {len(final_df)} global rows to the database.")
    except Exception as e:
        print(f"❌ Error saving to database: {e}")

if __name__ == "__main__":
    run_pipeline()