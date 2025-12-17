import requests
import pandas as pd
import time
from datetime import datetime

def fetch_hot_posts(subreddit="wallstreetbets", limit=25, pages=3):
    """
    Fetches multiple pages of 'Hot' posts from a subreddit.
    """
    print(f"--- 📡 Connecting to r/{subreddit} (Fetching {pages} pages) ---")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    all_posts = []
    after_token = None # This is our bookmark for the next page

    for page in range(pages):
        # 1. Build the URL (add the 'after' bookmark if we have one)
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
        if after_token:
            url += f"&after={after_token}"

        try:
            # 2. Request Data
            response = requests.get(url, headers=headers)
            
            if response.status_code != 200:
                print(f"   ❌ Page {page+1} failed: {response.status_code}")
                break # Stop if Reddit blocks us

            data = response.json()
            
            # 3. Extract Posts
            current_batch = []
            for item in data['data']['children']:
                post = item['data']
                if post.get('stickied'): continue
                
                current_batch.append({
                    "title": post['title'],
                    "score": post['score'],
                    "url": post['url'],
                    "date": datetime.now() # In a real app, convert post['created_utc']
                })
            
            # 4. Add to main list
            all_posts.extend(current_batch)
            print(f"   ✅ Page {page+1}: Found {len(current_batch)} posts")

            # 5. Get the bookmark for the next loop
            after_token = data['data'].get('after')
            
            # If there is no next page, stop early
            if not after_token:
                break
                
            # 6. SLEEP! (Crucial to avoid getting banned)
            time.sleep(2) 

        except Exception as e:
            print(f"   ❌ Critical Error on page {page+1}: {e}")
            break

    print(f"🎉 Total fetched: {len(all_posts)} headlines from r/{subreddit}")
    return pd.DataFrame(all_posts)

# Test it immediately
if __name__ == "__main__":
    df = fetch_hot_posts("IndianStreetBets", pages=2)
    print(df.head())