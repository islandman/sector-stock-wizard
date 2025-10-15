import unittest
import pandas as pd
from utils.indicators import compute_rsi, compute_macd, compute_obv

class TestIndicators(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "Adj Close": [100, 102, 101, 103, 105, 104, 106],
            "Volume": [1000, 1100, 1050, 1200, 1300, 1250, 1400]
        })

    def test_rsi_output(self):
        rsi = compute_rsi(self.df["Adj Close"])
        self.assertIsInstance(rsi, pd.Series)
        self.assertTrue((rsi >= 0).all() and (rsi <= 100).all())

    def test_macd_output(self):
        macd, signal = compute_macd(self.df["Adj Close"])
        self.assertIsInstance(macd, float)
        self.assertIsInstance(signal, float)

    def test_obv_output(self):
        obv = compute_obv(self.df)
        self.assertIsInstance(obv, pd.Series)
        self.assertEqual(len(obv), len(self.df))

if __name__ == "__main__":
    unittest.main()
