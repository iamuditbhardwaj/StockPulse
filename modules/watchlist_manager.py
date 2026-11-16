
import json
import csv
from pathlib import Path
from uuid import uuid4

WATCHLIST_FILE = Path(__file__).parent.parent / "data" / "watchlist.json"
STOCKS_FILE = Path(__file__).parent.parent / "data" / "stocks.csv"


def save_watchlists(data):
    WATCHLIST_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(WATCHLIST_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_watchlists():
    if not WATCHLIST_FILE.exists():
        data = {
            "watchlists": [
                {
                    "id": "default",
                    "name": "My Watchlist",
                    "stocks": []
                }
            ],
            "active_watchlist": "default"
        }
        save_watchlists(data)
        return data

    with open(WATCHLIST_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Migrate the old single-watchlist format.
    if "watchlists" not in data:
        old_stocks = data.get("watchlist", [])

        data = {
            "watchlists": [
                {
                    "id": "default",
                    "name": "My Watchlist",
                    "stocks": old_stocks
                }
            ],
            "active_watchlist": "default"
        }
        save_watchlists(data)

    return data


def get_watchlists():
    return load_watchlists()


def get_watchlist_by_id(watchlist_id):
    data = load_watchlists()

    for watchlist in data["watchlists"]:
        if watchlist["id"] == watchlist_id:
            return watchlist

    return None


def create_watchlist(name):
    name = name.strip()

    if not name:
        return None, "Watchlist name cannot be empty"

    data = load_watchlists()

    for watchlist in data["watchlists"]:
        if watchlist["name"].lower() == name.lower():
            return None, "A watchlist with this name already exists"

    new_watchlist = {
        "id": str(uuid4()),
        "name": name,
        "stocks": []
    }

    data["watchlists"].append(new_watchlist)

    if len(data["watchlists"]) == 1:
        data["active_watchlist"] = new_watchlist["id"]

    save_watchlists(data)

    return new_watchlist, "Watchlist created successfully"


def set_active_watchlist(watchlist_id):
    data = load_watchlists()

    for watchlist in data["watchlists"]:
        if watchlist["id"] == watchlist_id:
            data["active_watchlist"] = watchlist_id
            save_watchlists(data)
            return True

    return False


def delete_watchlist(watchlist_id):
    data = load_watchlists()

    if len(data["watchlists"]) <= 1:
        return "At least one watchlist must remain"

    for watchlist in data["watchlists"]:
        if watchlist["id"] == watchlist_id:
            data["watchlists"].remove(watchlist)

            if data["active_watchlist"] == watchlist_id:
                data["active_watchlist"] = data["watchlists"][0]["id"]

            save_watchlists(data)
            return "Watchlist deleted successfully"

    return "Watchlist not found"


def add_stock_to_watchlist(watchlist_id, symbol):
    if not symbol.strip():
        return "Stock symbol cannot be empty"

    symbol = symbol.strip().upper()
    data = load_watchlists()

    selected_watchlist = None

    for watchlist in data["watchlists"]:
        if watchlist["id"] == watchlist_id:
            selected_watchlist = watchlist
            break

    if selected_watchlist is None:
        return "Watchlist not found"

    for stock in selected_watchlist["stocks"]:
        if stock["symbol"].upper() == symbol:
            return "Stock already exists in watchlist"

    with open(STOCKS_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for record in reader:
            if record["symbol"].upper() == symbol:
                new_stock = {
                    "symbol": record["symbol"],
                    "company": record["company"]
                }

                selected_watchlist["stocks"].append(new_stock)
                save_watchlists(data)

                return "Stock added successfully"

    return "Stock not found"


def remove_stock_from_watchlist(watchlist_id, symbol):
    if not symbol.strip():
        return "Stock symbol cannot be empty"

    symbol = symbol.strip().upper()
    data = load_watchlists()

    for watchlist in data["watchlists"]:
        if watchlist["id"] == watchlist_id:

            for stock in watchlist["stocks"]:
                if stock["symbol"].upper() == symbol:
                    watchlist["stocks"].remove(stock)
                    save_watchlists(data)
                    return "Stock removed successfully"

            return "Stock not found in watchlist"

    return "Watchlist not found"


# Backward-compatible functions for the original API.

def get_watchlist():
    data = load_watchlists()
    active_id = data["active_watchlist"]

    for watchlist in data["watchlists"]:
        if watchlist["id"] == active_id:
            return watchlist["stocks"]

    return []


def add_stock(symbol):
    data = load_watchlists()
    return add_stock_to_watchlist(data["active_watchlist"], symbol)


def remove_stock(symbol):
    data = load_watchlists()
    return remove_stock_from_watchlist(data["active_watchlist"], symbol)
