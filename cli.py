import argparse
import pandas as pd
from utils.indicators import fetch_data
from utils.rules_engine import load_rules, evaluate_rules
from datetime import datetime

def evaluate_ticker(ticker, sector, rules):
    try:
        df = fetch_data(ticker)
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
        buy = evaluate_rules(rules[sector]["buy_rules"], indicators)
        sell = evaluate_rules(rules[sector]["sell_rules"], indicators)
        buy_pass = all(r["passed"] for r in buy)
        sell_pass = any(r["passed"] for r in sell)
        decision = "BUY" if buy_pass and not sell_pass else "SELL" if sell_pass else "HOLD"
        print(f"{ticker}: {decision}")
        return {
            "Timestamp": datetime.now(),
            "Ticker": ticker,
            "Sector": sector,
            "Buy_Pass": buy_pass,
            "Sell_Pass": sell_pass,
            "Decision": decision
        }
    except Exception as e:
        print(f"Error evaluating {ticker}: {str(e)}")
        return {
            "Timestamp": datetime.now(),
            "Ticker": ticker,
            "Sector": sector,
            "Buy_Pass": False,
            "Sell_Pass": False,
            "Decision": "ERROR"
        }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", help="Single ticker")
    parser.add_argument("--batch", help="CSV file with tickers")
    parser.add_argument("--sector", required=True, help="Sector name")
    args = parser.parse_args()

    rules = load_rules()
    results = []

    if args.ticker:
        results.append(evaluate_ticker(args.ticker, args.sector, rules))
    elif args.batch:
        df = pd.read_csv(args.batch)
        for ticker in df["Ticker"]:
            results.append(evaluate_ticker(ticker, args.sector, rules))

    pd.DataFrame(results).to_csv("logs/cli_decisions.csv", index=False)

if __name__ == "__main__":
    main()
