import unittest
from scripts import enrich_leads

class TestEnrichLeads(unittest.TestCase):
    def test_enrich_lead_row(self):
        fake_row = {"Building":"Test", "Address":"123 Flatbush Ave", "Violation Descriptions":"Broken doors"}
        out = enrich_leads.enrich_lead_row(fake_row)
        self.assertIn("Property Manager Name", out)
        self.assertIn("AI Relevance Score", out)

if __name__ == "__main__":
    unittest.main()
