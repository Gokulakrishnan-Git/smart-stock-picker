# Smart Monthly Stock Picker (SMP) - Streamlit App

import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime

# Thresholds for scoring fundamentals
THRESHOLDS = {
    'ROE': 15,
    'ROCE': 15,
    'DebtEquity': 0.5,
    'CurrentRatio': 1.5,
    'ProfitGrowth': 15,
    'SalesGrowth': 10,
    'PE': 25
}

# Example: Add tickers from NSE
TICKERS = [
    'RELIANCE.NS', 'INFY.NS', 'TCS.NS', 'HDFCBANK.NS', 'ITC.NS',
    'LT.NS', 'ASIANPAINT.NS', 'MARUTI.NS', 'ULTRACEMCO.NS', 'NESTLEIND.NS'
]

# Simulated fundamentals (replace with real API/scraper later)
def fetch_fundamentals(ticker):
    return {
        'Ticker': ticker,
        'ROE': 18,
        'ROCE': 17,
        'DebtEquity': 0.3,
        'CurrentRatio': 2.0,
        'ProfitGrowth': 20,
        'SalesGrowth': 12,
        'PE': 22
    }

# Score stocks based on fundamentals
def score_stock(fundamentals):
    score = 0
    for key, threshold in THRESHOLDS.items():
        value = fundamentals.get(key, None)
        if value is not None:
            if key == 'DebtEquity':
                if value < threshold:
                    score += 1
            else:
                if value > threshold:
                    score += 1
    fundamentals['Score'] = score
    return fundamentals

# Suggest investment allocations
def suggest_investments(scored_data, monthly_amount):
    top_stocks = scored_data.sort_values(by='Score', ascending=False).head(3)
    investment_per_stock = monthly_amount / len(top_stocks)

    suggestions = []
    for _, row in top_stocks.iterrows():
        current_price = yf.Ticker(row['Ticker']).history(period='1d')['Close'].iloc[-1]
        quantity = int(investment_per_stock // current_price)
        suggestions.append({
            'Ticker': row['Ticker'],
            'Score': row['Score'],
            'Price': round(current_price, 2),
            'Buy Qty': quantity,
            'Total': round(quantity * current_price, 2)
        })
    return suggestions

# Streamlit App
st.set_page_config(page_title="Smart Stock Picker", layout="centered")
st.title("📈 Smart Monthly Stock Picker")
st.write("Pick fundamentally strong stocks to invest in every month.")

# Budget input
monthly_budget = st.number_input("Enter your monthly investment amount (₹):", min_value=1000, value=5000, step=500)

# Fetch & score stocks
if st.button("📊 Score and Suggest Investments"):
    with st.spinner("Fetching and scoring stocks..."):
        data = []
        for ticker in TICKERS:
            fundamentals = fetch_fundamentals(ticker)
            scored = score_stock(fundamentals)
            data.append(scored)

        df = pd.DataFrame(data)
        st.subheader("Stock Scores")
        st.dataframe(df[['Ticker', 'Score']].sort_values(by='Score', ascending=False), use_container_width=True)

        suggestions = suggest_investments(df, monthly_budget)
        st.subheader("Suggested Investments")
        st.table(pd.DataFrame(suggestions))

        # Save log
        log_entry = pd.DataFrame(suggestions)
        log_entry['Date'] = datetime.today().strftime('%Y-%m-%d')
        log_entry.to_csv('investment_log.csv', mode='a', index=False, header=False)
        st.success("✅ Investment log updated in 'investment_log.csv'")
