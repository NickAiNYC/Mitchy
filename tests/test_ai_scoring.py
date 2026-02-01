import unittest
import pandas as pd
import os
from scripts import ai_scoring

class TestAIScoring(unittest.TestCase):
    def test_train_model(self):
        # Write dummy conversion data
        df = pd.DataFrame({
            "Urgency Score":[10,25,45],
            "AI Relevance Score":[2,7,9],
            "Conversion":[0,1,1]
        })
        df.to_csv("enriched_leads.csv", index=False)
        ai_scoring.train_model("enriched_leads.csv")
        self.assertTrue(os.path.exists("ai_lead_model.pkl"))

if __name__ == "__main__":
    unittest.main()
