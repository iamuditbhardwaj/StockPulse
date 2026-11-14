import json
from pathlib import Path
from datetime import datetime

from modules.performance_analyzer import calculate_performance
from modules.trend_analyzer import calculate_trend

HISTORY_FILE = Path(__file__).parent.parent / "data" / "report_history.json"

def generate_report(symbol, company, closing_prices):

    # Calculate performance
    performance = calculate_performance(closing_prices)

    # Calculate trend
    trend = calculate_trend(closing_prices)

    # Get report generation date
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create report
    report = {
        "symbol": symbol,
        "company": company,
        "report_date": report_date,
        "performance": performance,
        "trend_analysis": trend
    }

    return report

def load_report_history():

    if not HISTORY_FILE.exists():
        return {"reports": []}

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data

def save_report_history(data):

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def add_report_to_history(report):

    data = load_report_history()

    data["reports"].append(report)

    save_report_history(data)

    return "Report saved successfully"
