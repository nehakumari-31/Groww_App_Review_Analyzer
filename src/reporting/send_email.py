import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

def send_gmail(recipient_email):
    report_path = 'data/reporting/latest_report.json'
    
    if not os.path.exists(report_path):
        print(f"Report not found at {report_path}. Run reporter.py first.")
        return

    with open(report_path, 'r') as f:
        report = json.load(f)
    
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD") # Must be an App Password
    
    if not gmail_user or not gmail_password:
        print("Error: GMAIL_USER or GMAIL_APP_PASSWORD not set in .env")
        return

    # Create Message
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = recipient_email
    msg['Subject'] = f"Weekly Groww Review Pulse - {os.path.basename(report_path)}"
    
    msg.attach(MIMEText(report['email_draft'], 'plain'))
    
    try:
        # Create SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() # Enable security
        server.login(gmail_user, gmail_password)
        text = msg.as_string()
        server.sendmail(gmail_user, recipient_email, text)
        server.quit()
        print(f"Email successfully sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python send_email.py <recipient_email>")
    else:
        send_gmail(sys.argv[1])
