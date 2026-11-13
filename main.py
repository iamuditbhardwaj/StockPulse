import csv
from pathlib import Path
from fastapi import FastAPI, HTTPException
from modules.performance_analyzer import calculate_performance
from modules.trend_analyzer import calculate_trend
from modules.stock_comparator import compare_stocks
from modules.watchlist_manager import add_stock, get_watchlist, remove_stock

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

@app.get("/stocks/{symbol}/trend")
def get_stock_trend(symbol: str):

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
        result = calculate_trend(closing_prices)
        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@app.get("/compare/{symbol1}/{symbol2}")
def compare_stock_performance(symbol1: str, symbol2: str):

    # Prevent comparing the same stock
    if symbol1.upper() == symbol2.upper():
        raise HTTPException(
            status_code=400,
            detail="Please provide two different stock symbols"
        )

    records = load_stock_data()

    closing_prices1 = []
    closing_prices2 = []

    # Collect closing prices for both stocks
    for record in records:
        current_symbol = record["symbol"].upper()

        if current_symbol == symbol1.upper():
            closing_prices1.append(float(record["close"]))

        if current_symbol == symbol2.upper():
            closing_prices2.append(float(record["close"]))

    # Check whether both stocks exist
    if not closing_prices1:
        raise HTTPException(
            status_code=404,
            detail=f"No historical data found for {symbol1.upper()}"
        )

    if not closing_prices2:
        raise HTTPException(
            status_code=404,
            detail=f"No historical data found for {symbol2.upper()}"
        )

    # Calculate and compare performance
    try:
        result1 = calculate_performance(closing_prices1)
        result2 = calculate_performance(closing_prices2)

        comparison = compare_stocks(
            symbol1.upper(),
            result1,
            symbol2.upper(),
            result2
        )

        return comparison

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

@app.get("/watchlist")
def view_watchlist():

    return {
        "watchlist": get_watchlist()
    }

@app.post("/watchlist/{symbol}")
def add_stock_to_watchlist(symbol: str):

    result = add_stock(symbol)

    if result == "Stock already exists in watchlist":
        raise HTTPException(status_code=400, detail=result)

    if result == "Stock not found":
        raise HTTPException(status_code=404, detail=result)

    return {
        "message": result
    }

@app.delete("/watchlist/{symbol}")
def delete_stock_from_watchlist(symbol: str):

    result = remove_stock(symbol)

    if result == "Stock not found in watchlist":
        raise HTTPException(status_code=404, detail=result)

    return {
        "message": result
    }