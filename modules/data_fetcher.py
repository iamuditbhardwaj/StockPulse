
import csv
import yfinance as yf
from pathlib import Path


DATA_FILE = Path(__file__).parent.parent / "data" / "stocks.csv"


INSTRUMENTS = {
    "RELIANCE.NS": {
        "company": "Reliance Industries",
        "asset_type": "Indian Equity",
        "currency": "INR"
    },
    "TCS.NS": {
        "company": "Tata Consultancy Services",
        "asset_type": "Indian Equity",
        "currency": "INR"
    },
    "INFY.NS": {
        "company": "Infosys",
        "asset_type": "Indian Equity",
        "currency": "INR"
    },
    "HDFCBANK.NS": {
        "company": "HDFC Bank",
        "asset_type": "Indian Equity",
        "currency": "INR"
    },
    "^NSEI": {
        "company": "NIFTY 50",
        "asset_type": "Market Index",
        "currency": "Index Points"
    },
    "GC=F": {
        "company": "Gold Futures (COMEX)",
        "asset_type": "Commodity Futures",
        "currency": "USD"
    },
    "SI=F": {
        "company": "Silver Futures (COMEX)",
        "asset_type": "Commodity Futures",
        "currency": "USD"
    }
}


def refresh_stock_data():

    symbols = list(INSTRUMENTS.keys())

    print("Downloading historical market data...")

    data = yf.download(
        symbols,
        period="1y",
        interval="1d",
        group_by="ticker",
        auto_adjust=False,
        progress=False,
        threads=False
    )

    if data.empty:
        raise ValueError("No market data was downloaded")

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "date", "symbol", "company",
        "asset_type", "currency",
        "open", "high", "low", "close", "volume"
    ]

    total_records = 0

    with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for symbol, details in INSTRUMENTS.items():

            instrument_data = data[symbol]

            valid_data = instrument_data.dropna(
                subset=["Open", "High", "Low", "Close"]
            )

            for date, record in valid_data.iterrows():

                writer.writerow({
                    "date": date.strftime("%Y-%m-%d"),
                    "symbol": symbol,
                    "company": details["company"],
                    "asset_type": details["asset_type"],
                    "currency": details["currency"],
                    "open": round(float(record["Open"]), 2),
                    "high": round(float(record["High"]), 2),
                    "low": round(float(record["Low"]), 2),
                    "close": round(float(record["Close"]), 2),
                    "volume": int(record["Volume"])
                })

                total_records += 1

    print("Market data saved successfully!")
    print("Total records:", total_records)
    print("File location:", DATA_FILE)
