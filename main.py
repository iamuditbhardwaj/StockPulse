import csv
from pathlib import Path
from fastapi import FastAPI, HTTPException
from modules.performance_analyzer import calculate_performance

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

@app.get("/stocks/{symbol}/performance")
def get_stock_performance(symbol: str):

    records = load_stock_data()

    closing_prices = []

    for record in records:
        if record["symbol"].upper() == symbol.upper():
            closing_prices.append(float(record["close"]))

    if not closing_prices:
        raise HTTPException(
            status_code=404,
            detail="Stock or historical data not found"
        )

    try:
        result = calculate_performance(closing_prices)
        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )