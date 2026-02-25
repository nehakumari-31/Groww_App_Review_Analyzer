import pandas as pd
import json
import os
from groq import Groq
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

class GrowwAnalyzer:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        self.themes = ["onboarding", "KYC", "payments", "statements", "withdrawals", "others"]

    def classify_reviews(self, reviews_df):
        print("Classifying reviews into themes...")
        # To save tokens and time, we'll process in small batches or summarize
        # For this implementation, we will classify each review using a focused prompt
        
        classifications = []
        for index, row in reviews_df.iterrows():
            text = row['review_text'][:500] # Limit text length
            prompt = f"""
            Task: Classify this app review into exactly ONE of the following themes:
            Themes: {', '.join(self.themes)}
            
            Review: "{text}"
            
            Return ONLY the theme name in lowercase.
            """
            
            try:
                response = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=self.model,
                    temperature=0,
                    max_tokens=10
                )
                theme = response.choices[0].message.content.strip().lower()
                # Ensure it's in our list
                if theme not in self.themes:
                    theme = "others"
                classifications.append(theme)
            except Exception as e:
                print(f"Error classifying review {index}: {e}")
                classifications.append("others")
                time.sleep(1) # Simple rate limit handling
                
        reviews_df['theme'] = classifications
        return reviews_df

    def generate_pulse(self, df):
        print("Generating Groww Review Pulse...")
        
        # 1. Key Themes (Top 3 by volume)
        theme_counts = df['theme'].value_counts().head(3).to_dict()
        
        # 2. Critical Quotes & Actionable Ideas (Using LLM to summarize the whole batch)
        # We'll take a representative sample of reviews to generate these
        sample_reviews = df.sample(min(20, len(df)))['review_text'].tolist()
        formatted_reviews = "\n- ".join(sample_reviews)
        
        prompt = f"""
        Analyze these app reviews for 'Groww' and generate a "Review Pulse" report.
        
        Reviews:
        {formatted_reviews}
        
        Return a JSON object with exactly these keys:
        1. "key_themes": [List of 3 main themes confirmed from data]
        2. "critical_quotes": [List of 3 impactful, anonymized customer quotes]
        3. "actionable_ideas": [List of 3 specific product improvement ideas]
        
        Ensure the response is valid JSON.
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            pulse_data = json.loads(response.choices[0].message.content)
            return pulse_data
        except Exception as e:
            print(f"Error generating pulse: {e}")
            return {
                "key_themes": list(theme_counts.keys()),
                "critical_quotes": ["Error generating quotes"],
                "actionable_ideas": ["Error generating ideas"]
            }

def main():
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY not found in environment.")
        return

    input_path = 'data/processed/groww_reviews_processed.csv'
    output_dir = 'data/analysis'
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(input_path):
        print(f"No processed data found at {input_path}")
        return
        
    df = pd.read_csv(input_path)
    
    # For verification, we might want to sample if the file is massive
    # df = df.sample(min(50, len(df))) 
    
    analyzer = GrowwAnalyzer()
    
    # Classify all reviews (or use df.head(N) for testing)
    processed_df = analyzer.classify_reviews(df.copy())
    
    # Generate Pulse
    pulse = analyzer.generate_pulse(processed_df)
    
    # Save results
    with open(f"{output_dir}/review_pulse.json", "w") as f:
        json.dump(pulse, f, indent=4)
        
    processed_df.to_csv(f"{output_dir}/categorized_reviews.csv", index=False)
    
    print(f"Analysis complete. Results saved to {output_dir}")

if __name__ == "__main__":
    main()
