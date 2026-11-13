import json
import csv
from pathlib import Path

WATCHLIST_FILE = Path(__file__).parent.parent / "data" / "watchlist.json"

def load_watchlist():

    if not WATCHLIST_FILE.exists():
        return {"watchlist": []}

    with open(WATCHLIST_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data

def save_watchlist(data):

    with open(WATCHLIST_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def add_stock(symbol):

    symbol = symbol.upper()

    # Load existing watchlist
    data = load_watchlist()

    # Check for duplicate stock
    for stock in data["watchlist"]:
        if stock["symbol"] == symbol:
            return "Stock already exists in watchlist"

    # Load available stocks from CSV
    stocks_file = Path(__file__).parent.parent / "data" / "stocks.csv"


    with open(stocks_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for record in reader:
            if record["symbol"].upper() == symbol:

                new_stock = {
                    "symbol": record["symbol"],
                    "company": record["company"]
                }

                data["watchlist"].append(new_stock)

                save_watchlist(data)

                return "Stock added successfully"

    return "Stock not found"

def get_watchlist():

    data = load_watchlist()

    return data["watchlist"]

def remove_stock(symbol):

    symbol = symbol.upper()

    data = load_watchlist()

    for stock in data["watchlist"]:

        if stock["symbol"] == symbol:

            data["watchlist"].remove(stock)

            save_watchlist(data)

            return "Stock removed successfully"

    return "Stock not found in watchlist"

