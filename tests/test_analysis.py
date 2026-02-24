import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
import json
from src.analysis.analyzer import GrowwAnalyzer

class TestAnalysis(unittest.TestCase):
    
    @patch('src.analysis.analyzer.Groq')
    def test_groww_review_pulse_json_structure(self, mock_groq):
        # Setup mock
        mock_client = MagicMock()
        mock_groq.return_value = mock_client
        
        # Mock response for generate_pulse
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content=json.dumps({
                "key_themes": ["KYC", "Payments", "Onboarding"],
                "critical_quotes": ["Quote 1", "Quote 2", "Quote 3"],
                "actionable_ideas": ["Idea 1", "Idea 2", "Idea 3"]
            })))
        ]
        mock_client.chat.completions.create.return_value = mock_response
        
        # Run analyzer
        analyzer = GrowwAnalyzer()
        df = pd.DataFrame({'review_text': ['test review 1', 'test review 2'], 'theme': ['kyc', 'payments']})
        pulse = analyzer.generate_pulse(df)
        
        # Verify structure
        self.assertIn("key_themes", pulse)
        self.assertIn("critical_quotes", pulse)
        self.assertIn("actionable_ideas", pulse)
        self.assertEqual(len(pulse["key_themes"]), 3)
        self.assertEqual(pulse["key_themes"][0], "KYC")

if __name__ == '__main__':
    unittest.main()
