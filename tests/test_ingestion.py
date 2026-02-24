import unittest
import pandas as pd
from src.ingestion.cleaner import scrub_pii, filter_by_date
import datetime

class TestIngestion(unittest.TestCase):
    
    def test_scrub_pii_email(self):
        sample_text = "Contact me at test@example.com for more info."
        expected_text = "Contact me at [EMAIL] for more info."
        self.assertEqual(scrub_pii(sample_text), expected_text)
        
    def test_scrub_pii_phone_complex(self):
        # International
        self.assertEqual(scrub_pii("Call +91-9988776655"), "Call [PHONE]")
        # Formatted US/General
        self.assertEqual(scrub_pii("My number is (123) 456-7890"), "My number is [PHONE]")
        # Dotted
        self.assertEqual(scrub_pii("Contact 555.555.5555"), "Contact [PHONE]")

    def test_scrub_pii_account_id(self):
        self.assertEqual(scrub_pii("My ID is GROW12345"), "My ID is [ACCOUNT_ID]")
        self.assertEqual(scrub_pii("Transaction ACC998877"), "Transaction [ACCOUNT_ID]")
        self.assertEqual(scrub_pii("Ref ID: trans_abc123"), "Ref ID: [ACCOUNT_ID]")

    def test_scrub_pii_contextual_names(self):
        self.assertEqual(scrub_pii("Regards, Neha Kumari"), "Regards, [NAME]")
        self.assertEqual(scrub_pii("Dear John Doe,"), "Dear [NAME],")
        self.assertEqual(scrub_pii("My name is Rajesh"), "My name is [NAME]")

    def test_filter_by_date(self):
        # Create sample dataframe
        now = datetime.datetime.now(datetime.timezone.utc)
        old_date = now - datetime.timedelta(weeks=20)
        recent_date = now - datetime.timedelta(weeks=4)
        
        data = {
            'user_name': ['User1', 'User2'],
            'review_text': ['old', 'recent'],
            'review_date': [old_date, recent_date]
        }
        df = pd.DataFrame(data)
        
        # Filter (12 weeks)
        filtered_df = filter_by_date(df, weeks=12)
        
        self.assertEqual(len(filtered_df), 1)
        self.assertEqual(filtered_df.iloc[0]['review_text'], 'recent')

if __name__ == '__main__':
    unittest.main()
