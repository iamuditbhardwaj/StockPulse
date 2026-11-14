import csv
from pathlib import Path
from fastapi import FastAPI, HTTPException
from modules.performance_analyzer import calculate_performance
from modules.trend_analyzer import calculate_trend
from modules.stock_comparator import compare_stocks
from modules.watchlist_manager import add_stock, get_watchlist, remove_stock
from modules.report_generator import (
    generate_report,
    add_report_to_history,
    load_report_history
)

app = FastAPI(title="StockPulse")

DATA_FILE = Path(__file__).parent / "data" / "stocks.csv"

def load_stock_data():
    try:
        with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            required_columns = [
                "date", "symbol", "company",
                "open", "high", "low", "close", "volume"
            ]

            if not reader.fieldnames or not all(
                column in reader.fieldnames for column in required_columns
            ):
                raise HTTPException(
                    status_code=500,
                    detail="Invalid stock data file structure"
                )

            stock_data = list(reader)

            for record in stock_data:
                for column in required_columns:
                    if not record[column] or not record[column].strip():
                        raise HTTPException(
                            status_code=500,
                            detail="Stock data contains incomplete records"
                        )

        return stock_data

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Stock data file not found"
        )

    except PermissionError:
        raise HTTPException(
            status_code=500,
            detail="Permission denied while reading stock data"
        )

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

    symbol = symbol.strip().upper()

    if not symbol.strip():
        raise HTTPException(
            status_code=400,
            detail="Stock symbol cannot be empty"
        )

    records = load_stock_data()

    for record in records:
        if record["symbol"].upper() == symbol:

            return {
                "symbol": record["symbol"],
                "company": record["company"],
                "message": "Stock found successfully"
            }

    raise HTTPException(
    status_code=404,
    detail="Stock not found"
    )

@app.get("/stocks/{symbol}/history")
def get_stock_history(symbol: str):

    symbol = symbol.strip().upper()

    if not symbol.strip():
        raise HTTPException(
            status_code=400,
            detail="Stock symbol cannot be empty"
        )

    records = load_stock_data()

    history = []

    for record in records:
        if record["symbol"].upper() == symbol:
            history.append(record)

    if len(history) == 0:
        raise HTTPException(
            status_code=404,
            detail="No historical data found for this stock"
        )

    return {
        "symbol": symbol,
        "total_records": len(history),
        "history": history
    }

@app.get("/stocks/{symbol}/performance")
def get_stock_performance(symbol: str):

    symbol = symbol.strip().upper()

    if not symbol.strip():
        raise HTTPException(
            status_code=400,
            detail="Stock symbol cannot be empty"
        )

    records = load_stock_data()

    closing_prices = []

    for record in records:
        if record["symbol"].upper() == symbol:
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

    symbol = symbol.strip().upper()

    if not symbol.strip():
        raise HTTPException(
            status_code=400,
            detail="Stock symbol cannot be empty"
        )

    records = load_stock_data()

    closing_prices = []

    for record in records:
        if record["symbol"].upper() == symbol:
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

    symbol1 = symbol1.strip().upper()
    symbol2 = symbol2.strip().upper()

    if not symbol1.strip() or not symbol2.strip():
        raise HTTPException(
            status_code=400,
            detail="Both stock symbols are required"
        )

    # Prevent comparing the same stock
    if symbol1 == symbol2:
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

        if current_symbol == symbol1:
            closing_prices1.append(float(record["close"]))

        if current_symbol == symbol2:
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

    if result == "Stock symbol cannot be empty":
        raise HTTPException(
            status_code=400,
            detail=result
        )

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

    if result == "Stock symbol cannot be empty":
        raise HTTPException(
            status_code=400,
            detail=result
        )

    if result == "Stock not found in watchlist":
        raise HTTPException(status_code=404, detail=result)

    return {
        "message": result
    }

@app.post("/reports/{symbol}")
def create_stock_report(symbol: str):

    symbol = symbol.strip().upper()

    if not symbol.strip():
        raise HTTPException(
            status_code=400,
            detail="Stock symbol cannot be empty"
        )

    records = load_stock_data()

    closing_prices = []
    company = None

    # Collect stock information
    for record in records:
        if record["symbol"].upper() == symbol:

            company = record["company"]
            closing_prices.append(float(record["close"]))

    # Check whether stock exists
    if not closing_prices:
        raise HTTPException(
            status_code=404,
            detail="Stock or historical data not found"
        )

    # Generate report
    try:
        report = generate_report(
            symbol,
            company,
            closing_prices
        )

        add_report_to_history(report)

        return report

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@app.get("/reports/history")
def get_report_history():

    history = load_report_history()

    return history