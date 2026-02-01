import unittest
from scripts import outreach

class TestOutreach(unittest.TestCase):
    def test_sms_template(self):
        lead = {'Building': 'Lennox', 'Property Manager Name': 'Alex'}
        sms = outreach.SMS_TEMPLATE.format(Building=lead['Building'], Manager=lead['Property Manager Name'])
        self.assertIn('Lennox', sms)
        self.assertIn('Alex', sms)

    def test_email_template(self):
        lead = {'Building': 'Bolden', 'Property Manager Name': 'Chris'}
        email = outreach.EMAIL_TEMPLATE.format(Building=lead['Building'], Manager=lead['Property Manager Name'])
        self.assertIn('Bolden', email)
        self.assertIn('Chris', email)

if __name__ == "__main__":
    unittest.main()
