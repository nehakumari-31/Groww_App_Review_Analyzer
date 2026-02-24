import pandas as pd
import re
import datetime
import os

def scrub_pii(text):
    if not isinstance(text, str):
        return text
    
    # 1. Emails
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    
    # 2. Phone Numbers (Intl, Formatted, 10-digit)
    # Matches +91-..., (555) 555-5555, 555-555-5555, 9876543210
    phone_pattern = r'(\+?\d{1,3}[\-\s\.]?)?(\(?\d{3}\)?[\-\s\.]?)?\d{3}[\-\s\.]?\d{4}\b'
    text = re.sub(phone_pattern, '[PHONE]', text)
    
    # 3. Account IDs (e.g., GROW12345, ACC998877)
    # Looking for alphanumeric codes starting with common ID prefixes
    # Uses negative lookahead to avoid matching "Transaction"
    acc_id_pattern = r'\b(?:GROW|ACC|ID|TXN)\d*[A-Z0-9]{5,}\b|\bTRANS(?!action)\w{4,}\b'
    text = re.sub(acc_id_pattern, '[ACCOUNT_ID]', text, flags=re.IGNORECASE)
    
    # 4. Contextual Names (Simple heuristic for "My name is [Name]" or "Regards, [Name]")
    name_markers = r'(?:[Mm]y name is|[Ii] am|[Rr]egards,|[Dd]ear|[Tt]hanks,|[Ss]incerely,)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
    matches = re.finditer(name_markers, text)
    for match in matches:
        name = match.group(1)
        if name:
            text = text.replace(name, '[NAME]')
    
    return text

def filter_by_date(df, weeks=12):
    if df.empty:
        return df
    
    # Convert review_date to datetime if it's not
    df['review_date'] = pd.to_datetime(df['review_date'], utc=True)
    
    # Calculate cutoff date
    cutoff_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(weeks=weeks)
    
    # Filter
    filtered_df = df[df['review_date'] >= cutoff_date]
    
    return filtered_df

def main():
    input_path = 'data/raw/groww_reviews_raw.csv'
    output_path = 'data/processed/groww_reviews_processed.csv'
    
    if not os.path.exists(input_path):
        print(f"No raw data found at {input_path}")
        return
    
    print(f"Loading raw reviews from {input_path}...")
    df = pd.read_csv(input_path)
    
    print(f"Initial count: {len(df)}")
    
    # 1. Date Filtering (8-12 weeks, we use 12 for the full range)
    df = filter_by_date(df, weeks=12)
    print(f"After date filtering (12 weeks): {len(df)}")
    
    # 2. PII Scrubbing
    print("Scrubbing PII...")
    df['review_text'] = df['review_text'].apply(scrub_pii)
    # Also scrub user names just in case
    df['user_name'] = df['user_name'].apply(scrub_pii)
    
    # Ensure processed directory exists
    os.makedirs('data/processed', exist_ok=True)
    
    # 3. Save processed data
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} processed reviews to {output_path}")

if __name__ == "__main__":
    main()
