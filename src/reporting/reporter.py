import json
import os
from datetime import datetime

def generate_email_draft(pulse):
    themes = ", ".join(pulse.get('key_themes', []))
    quotes = "\n".join([f"- \"{q}\"" for q in pulse.get('critical_quotes', [])])
    ideas = "\n".join([f"- {i}" for i in pulse.get('actionable_ideas', [])])
    
    date_str = datetime.now().strftime("%B %d, %Y")
    
    email_template = f"""
Subject: Weekly Groww Review Pulse - {date_str}

Hi Team,

Here is the weekly summary of customer feedback for the Groww app based on recent reviews.

Top Themes this week: {themes}

Voice of the Customer:
{quotes}

Product Improvement Ideas:
{ideas}

You can view the full interactive dashboard here: [Dashboard Link]

Best regards,
Groww Review Analyzer Bot
    """
    return email_template.strip()

def main():
    pulse_path = 'data/analysis/review_pulse.json'
    output_path = 'data/reporting/latest_report.json'
    
    if not os.path.exists(pulse_path):
        print(f"Analysis data not found at {pulse_path}")
        return

    with open(pulse_path, 'r') as f:
        pulse = json.load(f)
        
    report = {
        "email_draft": generate_email_draft(pulse),
        "generated_at": datetime.now().isoformat()
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=4)
        
    print(f"Gmail report generated successfully at {output_path}")
    print("-" * 30)
    print("EMAIL PREVIEW (≤250 words):")
    print(report["email_draft"])

if __name__ == "__main__":
    main()
