import csv
from pathlib import Path
from fastapi import FastAPI

app = FastAPI(title="StockPulse")

DATA_FILE = Path(__file__).parent / "data" / "stocks.csv"
def load_stock_data():
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        stock_data = list(reader)

    return stock_data

@app.get("/")
def home():
    return {
        "message": "Welcome to StockPulse",
        "project": "Stock Market Learning and Analysis"
    }

@app.get("/stocks")
def get_stocks():

    records = load_stock_data()

    unique_stocks = {}

    for record in records:
        symbol = record["symbol"]

        if symbol not in unique_stocks:
            unique_stocks[symbol] = {
                "symbol": symbol,
                "company": record["company"]
            }

    return list(unique_stocks.values())

@app.get("/stocks/{symbol}")
def search_stock(symbol: str):

    records = load_stock_data()

    for record in records:
        if record["symbol"].upper() == symbol.upper():

            return {
                "symbol": record["symbol"],
                "company": record["company"],
                "message": "Stock found successfully"
            }

    return {
        "message": "Stock not found"
    }

@app.get("/stocks/{symbol}/history")
def get_stock_history(symbol: str):

    records = load_stock_data()

    history = []

    for record in records:
        if record["symbol"].upper() == symbol.upper():
            history.append(record)

    if len(history) == 0:
        return {
            "message": "No historical data found for this stock"
        }

    return {
        "symbol": symbol.upper(),
        "total_records": len(history),
        "history": history
    }