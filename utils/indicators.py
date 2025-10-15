import yfinance as yf
import pandas as pd
import numpy as np

def fetch_data(ticker):
    df = yf.download(ticker, period="6mo", interval="1d")
    if df.empty:
        raise ValueError(f"No data found for ticker: {ticker}")
    
    df["Returns"] = df["Adj Close"].pct_change()
    df["MA_50"] = df["Adj Close"].rolling(window=50).mean()
    df["MA_200"] = df["Adj Close"].rolling(window=200).mean()
    df["Volatility"] = df["Returns"].rolling(window=20).std()
    df["RSI"] = compute_rsi(df["Adj Close"])
    df["MACD"], df["Signal"] = compute_macd(df["Adj Close"])
    df["OBV"] = compute_obv(df)
    df["OBV_trend"] = "up" if df["OBV"].iloc[-1] > df["OBV"].iloc[-20] else "down"
    return df


def fetch_backtest_data(ticker, period="1y"):
    df = yf.download(ticker, period=period, interval="1d")
    df["Returns"] = df["Adj Close"].pct_change()
    df["MA_50"] = df["Adj Close"].rolling(window=50).mean()
    df["MA_200"] = df["Adj Close"].rolling(window=200).mean()
    df["Volatility"] = df["Returns"].rolling(window=20).std()
    df["RSI"] = compute_rsi(df["Adj Close"])
    df["MACD"], df["Signal"] = compute_macd(df["Adj Close"])
    df["OBV"] = compute_obv(df)
    df["OBV_trend"] = df["OBV"].diff().apply(lambda x: "up" if x > 0 else "down")
    return df


def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = -delta.clip(upper=0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def compute_macd(series):
    ema12 = series.ewm(span=12, adjust=False).mean()
    ema26 = series.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal


def compute_obv(df):
    obv = [0]
    for i in range(1, len(df)):
        if df["Adj Close"].iloc[i] > df["Adj Close"].iloc[i - 1]:
            obv.append(obv[-1] + df["Volume"].iloc[i])
        elif df["Adj Close"].iloc[i] < df["Adj Close"].iloc[i - 1]:
            obv.append(obv[-1] - df["Volume"].iloc[i])
        else:
            obv.append(obv[-1])
    return pd.Series(obv, index=df.index)


def monte_carlo_simulation(df, num_simulations=100, days=30):
    last_price = df["Adj Close"].iloc[-1]
    returns = df["Returns"].dropna()
    mu = returns.mean()
    sigma = returns.std()

    simulations = []
    for _ in range(num_simulations):
        prices = [last_price]
        for _ in range(days):
            shock = np.random.normal(loc=mu, scale=sigma)
            prices.append(prices[-1] * (1 + shock))
        simulations.append(prices)
    return simulations
