# ticker_downloader.py

from nsetools import Nse

def fetch_nse_tickers():
    nse = Nse()
    stock_codes = nse.get_stock_codes()

    if not stock_codes:
        print("Failed to fetch stock codes. Please check your internet or try again later.")
        return

    tickers = list(stock_codes.keys())[1:]  # skip the 'SYMBOL' key
    tickers = [ticker + ".NS" for ticker in tickers]

    with open("nse_tickers.txt", "w") as f:
        for t in tickers:
            f.write(t + "\n")

    print(f"✅ Saved {len(tickers)} NSE tickers to 'nse_tickers.txt'.")

if __name__ == "__main__":
    fetch_nse_tickers()
