#!/usr/bin/env python3
"""
Test script to verify the stock-wizard fixes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.indicators import fetch_data, fetch_backtest_data
from utils.rules_engine import load_rules, evaluate_rules

def test_data_fetching():
    """Test that data fetching works correctly"""
    print("🧪 Testing data fetching...")
    
    try:
        # Test fetch_data
        df = fetch_data("AAPL")
        print(f"✅ fetch_data works - got {len(df)} rows")
        print(f"   Columns: {list(df.columns)}")
        print(f"   Latest RSI: {df['RSI'].iloc[-1]:.2f}")
        
        # Test fetch_backtest_data
        df_backtest = fetch_backtest_data("AAPL", "3mo")
        print(f"✅ fetch_backtest_data works - got {len(df_backtest)} rows")
        
        return True
    except Exception as e:
        print(f"❌ Data fetching failed: {e}")
        return False

def test_rules_engine():
    """Test that rules engine works correctly"""
    print("\n🧪 Testing rules engine...")
    
    try:
        rules = load_rules()
        print(f"✅ Rules loaded - sectors: {list(rules.keys())}")
        
        # Test with sample data
        sample_indicators = {
            'RSI': 30.0,
            'MA_50': 150.0,
            'MA_200': 140.0,
            'MACD': 0.5,
            'Signal': 0.3,
            'Volatility': 0.02,
            'OBV_trend': 'up'
        }
        
        buy_results = evaluate_rules(rules['tech']['buy_rules'], sample_indicators)
        sell_results = evaluate_rules(rules['tech']['sell_rules'], sample_indicators)
        
        print(f"✅ Rules evaluation works")
        print(f"   Buy rules: {len(buy_results)} rules evaluated")
        print(f"   Sell rules: {len(sell_results)} rules evaluated")
        
        return True
    except Exception as e:
        print(f"❌ Rules engine failed: {e}")
        return False

def test_integration():
    """Test the full integration"""
    print("\n🧪 Testing full integration...")
    
    try:
        # Get real data
        df = fetch_data("AAPL")
        latest_data = df.iloc[-1]
        
        indicators = {
            'RSI': latest_data['RSI'],
            'MA_50': latest_data['MA_50'],
            'MA_200': latest_data['MA_200'],
            'MACD': latest_data['MACD'],
            'Signal': latest_data['Signal'],
            'Volatility': latest_data['Volatility'],
            'OBV_trend': latest_data['OBV_trend']
        }
        
        rules = load_rules()
        buy_results = evaluate_rules(rules['tech']['buy_rules'], indicators)
        sell_results = evaluate_rules(rules['tech']['sell_rules'], indicators)
        
        buy_pass = all(r["passed"] for r in buy_results)
        sell_pass = any(r["passed"] for r in sell_results)
        
        decision = "BUY" if buy_pass and not sell_pass else "SELL" if sell_pass else "HOLD"
        
        print(f"✅ Full integration works")
        print(f"   AAPL decision: {decision}")
        print(f"   Buy pass: {buy_pass}, Sell pass: {sell_pass}")
        
        return True
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Running Stock Wizard Fix Tests")
    print("=" * 50)
    
    tests = [
        test_data_fetching,
        test_rules_engine,
        test_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The fixes are working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
