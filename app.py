import streamlit as st
from utils.indicators import fetch_data, fetch_backtest_data, monte_carlo_simulation
from utils.rules_engine import load_rules, evaluate_rules
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import yaml
import os

def load_override_reasons(path="rules/override_reasons.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)["override_reasons"]

def log_and_export(ticker, sector, buy_pass, sell_pass, override, reason):
    timestamp = datetime.now()
    with open("logs/decisions.log", "a") as f:
        f.write(f"
[{timestamp}] {ticker} | Sector={sector} | BUY_PASS={buy_pass} | SELL_PASS={sell_pass} | Override={override} | Reason={reason}
")
    row = {
        "Timestamp": timestamp,
        "Ticker": ticker,
        "Sector": sector,
        "Buy_Pass": buy_pass,
        "Sell_Pass": sell_pass,
        "Override": override,
        "Reason": reason
    }
    csv_path = "logs/decisions.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])
    df.to_csv(csv_path, index=False)

def plot_indicators(df, ticker):
    st.subheader(f"📉 Price & Indicators for {ticker}")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["Adj Close"], label="Price", color="black")
    ax.plot(df["MA_50"], label="MA 50", linestyle="--")
    ax.plot(df["MA_200"], label="MA 200", linestyle=":")
    ax.set_title(f"{ticker} Price with Moving Averages")
    ax.legend()
    st.pyplot(fig)
    st.line_chart(df[["RSI"]].dropna(), height=150)
    st.line_chart(df[["MACD", "Signal"]].dropna(), height=150)

st.title("📊 Sector-Aware Stock Buy/Sell Wizard")
rules = load_rules()
sectors = list(rules.keys())
selected_sector = st.selectbox("Select sector:", sectors)
tickers = st.text_area("Enter tickers (comma-separated):", "AAPL,MSFT,TSLA").split(",")
backtest_mode = st.checkbox("Enable Backtest Mode")
period = st.selectbox("Backtest period:", ["3mo", "6mo", "1y"]) if backtest_mode else None

for ticker in [t.strip().upper() for t in tickers if t.strip()]:
    st.header(f"📈 Analysis for {ticker} ({selected_sector})")
    if backtest_mode:
        df = fetch_backtest_data(ticker, period)
        plot_indicators(df, ticker)
        signals = []
        for date, row in df.iterrows():
            indicators = {
                'RSI': row['RSI'],
                'MA_50': row['MA_50'],
                'MA_200': row['MA_200'],
                'MACD': row['MACD'],
                'Signal': row['Signal'],
                'Volatility': row['Volatility'],
                'OBV_trend': row['OBV_trend']
            }
            buy_pass = all(evaluate_rule(r, indicators) for r in rules[selected_sector]["buy_rules"])
            sell_pass = any(evaluate_rule(r, indicators) for r in rules[selected_sector]["sell_rules"])
            signals.append({"Date": date, "Buy": buy_pass, "Sell": sell_pass})
        st.dataframe(pd.DataFrame(signals))
    else:
        try:
            df = fetch_data(ticker)
            # Get the latest indicators for rule evaluation
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
            plot_indicators(df, ticker)
            buy_results = evaluate_rules(rules[selected_sector]["buy_rules"], indicators)
            sell_results = evaluate_rules(rules[selected_sector]["sell_rules"], indicators)
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {str(e)}")
            continue
        st.subheader("✅ Buy Rule Evaluation")
        for r in buy_results:
            st.write(f"{r['name']}: {'✅ PASS' if r['passed'] else '❌ FAIL'}")
        st.subheader("🚫 Sell Rule Evaluation")
        for r in sell_results:
            st.write(f"{r['name']}: {'✅ PASS' if r['passed'] else '❌ FAIL'}")
        buy_pass = all(r["passed"] for r in buy_results)
        sell_pass = any(r["passed"] for r in sell_results)
        st.subheader("🧠 System Recommendation")
        if buy_pass and not sell_pass:
            st.success("System recommends: BUY")
        elif sell_pass:
            st.error("System recommends: SELL")
        else:
            st.warning("System recommends: HOLD")
        override = st.radio("Do you want to override the system?", ["No", "Yes"])
        reason = st.selectbox("Select your override reason:", load_override_reasons()) if override == "Yes" else "None"
        if st.button(f"Log Decision for {ticker}"):
            log_and_export(ticker, selected_sector, buy_pass, sell_pass, override, reason)
            st.success("✅ Decision logged and exported.")
        if st.checkbox("Run Monte Carlo Simulation"):
            sims = monte_carlo_simulation(df)
            st.subheader(f"📈 Monte Carlo Simulation ({len(sims)} paths, 30 days)")
            fig, ax = plt.subplots(figsize=(10, 4))
            for sim in sims:
                ax.plot(sim, alpha=0.2, color="blue")
            ax.set_title(f"{ticker} - 30-Day Monte Carlo Forecast")
            st.pyplot(fig)
