# 📊 Sector-Aware Stock Buy/Sell Wizard

A comprehensive stock analysis tool that provides intelligent buy/sell recommendations based on sector-specific rules and technical indicators.

## 🚀 Features

- **Sector-Specific Analysis**: Different rules for Tech, Energy, and Consumer Staples sectors
- **Technical Indicators**: RSI, MACD, Moving Averages, OBV, and Volatility analysis
- **Interactive Streamlit Dashboard**: User-friendly web interface
- **Command Line Interface**: Batch processing for multiple stocks
- **Backtesting Mode**: Historical analysis and performance testing
- **Monte Carlo Simulation**: Risk assessment and forecasting
- **Decision Logging**: Track and export trading decisions

## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit** - Web dashboard
- **yfinance** - Stock data fetching
- **pandas** - Data manipulation
- **matplotlib** - Charting
- **scikit-learn** - Machine learning utilities

## 📈 Supported Sectors

- **Technology**: Growth-focused rules with RSI and momentum indicators
- **Energy**: Volatility-aware analysis for commodity stocks
- **Consumer Staples**: Conservative rules for stable dividend stocks

## 🎯 Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Run Streamlit Dashboard
```bash
streamlit run app.py
```

### Command Line Usage
```bash
# Single stock analysis
python cli.py --ticker AAPL --sector tech

# Batch analysis
python cli.py --batch data/sample_tickers.csv --sector tech
```

## 📊 Technical Indicators

- **RSI (Relative Strength Index)**: Momentum oscillator
- **MACD**: Moving Average Convergence Divergence
- **Moving Averages**: 50-day and 200-day MA
- **OBV (On-Balance Volume)**: Volume-based indicator
- **Volatility**: 20-day rolling standard deviation

## 🔧 Configuration

Rules are defined in `rules/rules.yaml` and can be customized for different sectors:

```yaml
tech:
  buy_rules:
    - name: "RSI Oversold"
      condition: "RSI < 35"
    - name: "Golden Cross"
      condition: "MA_50 > MA_200"
```

## 📁 Project Structure

```
stock-wizard/
├── app.py                 # Streamlit dashboard
├── cli.py                 # Command line interface
├── utils/
│   ├── indicators.py      # Technical indicators
│   └── rules_engine.py    # Rule evaluation
├── rules/
│   ├── rules.yaml         # Sector-specific rules
│   └── override_reasons.yaml
├── tests/                 # Unit tests
└── logs/                  # Decision logs
```

## 🎨 Screenshots

The dashboard provides:
- Interactive stock analysis
- Real-time rule evaluation
- Historical backtesting
- Monte Carlo simulations
- Decision logging and export

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Not financial advice. Always do your own research before making investment decisions.