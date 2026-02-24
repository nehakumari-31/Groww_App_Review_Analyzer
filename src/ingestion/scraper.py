import pandas as pd
from google_play_scraper import Sort, reviews
from app_store_scraper import AppStore
import datetime
import os

def fetch_google_play_reviews(app_id='com.nextbillion.groww', count=200):
    print(f"Fetching Google Play reviews for {app_id} (Limit: {count})...")
    result, _ = reviews(
        app_id,
        lang='en',
        country='in',
        sort=Sort.NEWEST,
        count=count
    )
    
    df = pd.DataFrame(result)
    # Rename columns to match a standard format
    df = df[['userName', 'content', 'score', 'at', 'reviewId']]
    df.columns = ['user_name', 'review_text', 'rating', 'review_date', 'review_id']
    df['source'] = 'google_play'
    return df

def fetch_app_store_reviews(app_name='groww-stocks-mutual-fund-ipo', app_id=1404871703):
    print(f"Fetching App Store reviews for {app_name} ({app_id})...")
    groww = AppStore(country='in', app_name=app_name, app_id=app_id)
    groww.review(how_many=2000) # Fetch a good number
    
    df = pd.DataFrame(groww.reviews)
    if df.empty:
        return pd.DataFrame(columns=['user_name', 'review_text', 'rating', 'review_date', 'review_id', 'source'])
    
    # Rename columns to match a standard format
    df = df[['userName', 'review', 'rating', 'date', 'title']]
    df.columns = ['user_name', 'review_text', 'rating', 'review_date', 'review_title']
    df['source'] = 'app_store'
    df['review_id'] = df.index # App Store doesn't always provide a stable ID in this library
    return df

def main():
    # Ensure data directories exist
    os.makedirs('data/raw', exist_ok=True)
    
    # Fetch reviews
    try:
        gp_reviews = fetch_google_play_reviews()
    except Exception as e:
        print(f"Error fetching Google Play reviews: {e}")
        gp_reviews = pd.DataFrame()
        
    try:
        as_reviews = fetch_app_store_reviews()
    except Exception as e:
        print(f"Error fetching App Store reviews: {e}")
        as_reviews = pd.DataFrame()
        
    # Combine and save
    all_reviews = pd.concat([gp_reviews, as_reviews], ignore_index=True)
    
    output_path = 'data/raw/groww_reviews_raw.csv'
    all_reviews.to_csv(output_path, index=False)
    print(f"Saved {len(all_reviews)} reviews to {output_path}")

if __name__ == "__main__":
    main()
