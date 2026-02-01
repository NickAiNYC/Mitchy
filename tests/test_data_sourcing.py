import unittest
import pandas as pd
from scripts import data_sourcing

class TestDataSourcing(unittest.TestCase):
    def test_compute_tiers(self):
        df = pd.DataFrame({"Violations Count":[0,6,15], "Units":[10,100,220]})
        df2 = data_sourcing.compute_tiers(df)
        self.assertIn('Tier', df2.columns)
        self.assertEqual(list(df2['Tier']), [3,2,1])

if __name__ == "__main__":
    unittest.main()
