import unittest
from utils.rules_engine import evaluate_rule

class TestRuleEngine(unittest.TestCase):

    def setUp(self):
        self.indicators = {
            "RSI": 28,
            "MA_50": 105,
            "MA_200": 100,
            "MACD": 1.2,
            "Signal": 0.8,
            "OBV_trend": "up",
            "Volatility": 0.02
        }

    def test_rsi_rule(self):
        rule = {"name": "RSI Oversold", "condition": "RSI < 30"}
        self.assertTrue(evaluate_rule(rule, self.indicators))

    def test_ma_cross_rule(self):
        rule = {"name": "Golden Cross", "condition": "MA_50 > MA_200"}
        self.assertTrue(evaluate_rule(rule, self.indicators))

    def test_macd_rule(self):
        rule = {"name": "MACD Bullish", "condition": "MACD > Signal"}
        self.assertTrue(evaluate_rule(rule, self.indicators))

    def test_obv_rule(self):
        rule = {"name": "OBV Rising", "condition": "OBV_trend == 'up'"}
        self.assertTrue(evaluate_rule(rule, self.indicators))

    def test_invalid_rule(self):
        rule = {"name": "Broken Rule", "condition": "nonexistent > 0"}
        self.assertFalse(evaluate_rule(rule, self.indicators))

if __name__ == "__main__":
    unittest.main()
