# StockPulse

### Stock Market Learning and Analysis Application

StockPulse is a Python-based stock market learning and analysis application built using FastAPI.

It allows users to explore historical market data, analyze price performance and trends, compare instruments, manage a watchlist and generate stock analysis reports.

The application retrieves one year of daily historical market data using the `yfinance` Python library. The downloaded data is stored locally in a CSV file, while JSON files are used for persistent storage of watchlist information and generated report history.

StockPulse currently supports seven market instruments:

- Reliance Industries (`RELIANCE.NS`)
- Tata Consultancy Services (`TCS.NS`)
- Infosys (`INFY.NS`)
- HDFC Bank (`HDFCBANK.NS`)
- NIFTY 50 (`^NSEI`)
- Gold Futures (COMEX) (`GC=F`)
- Silver Futures (COMEX) (`SI=F`)

## Features

1. **Stock Explorer:** View available market instruments, their categories, currencies and historical price data.
2. **Performance Analyzer:** Calculate starting price, ending price, highest price, lowest price, average price, price change and percentage return.
3. **Trend Analyzer:** Identify whether an instrument shows an uptrend, downtrend or sideways trend.
4. **Stock Comparator:** Compare the performance of two instruments and identify the better performer based on percentage return.
5. **Watchlist Management:** Add instruments to a personal watchlist, view saved instruments and remove them.
6. **Report Generator:** Generate analysis reports containing performance and trend information.
7. **Report History:** Save and retrieve previously generated analysis reports.

## Technologies Used

- **Python:** Core programming language.
- **FastAPI:** Backend framework for building API endpoints.
- **yfinance:** Python library used to retrieve historical market data.
- **CSV:** Stores downloaded historical market data.
- **JSON:** Stores watchlist information and generated report history.
- **Uvicorn:** Runs the FastAPI application server.
- **Git and GitHub:** Version control and project hosting.
- **Visual Studio Code:** Development environment.

## Installation and Setup

Follow these steps to run StockPulse locally.

**Important:** Run all commands from the root `StockPulse` project directory.

### 1. Clone the Repository

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the Project Folder

```bash
cd StockPulse
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

This installs FastAPI and yfinance.

### 6. Download Historical Market Data

Run the following command from the project folder:

```bash
python -c "from modules.data_fetcher import refresh_stock_data; refresh_stock_data()"
```

This downloads one year of daily historical data for the seven supported instruments and saves it in `data/stocks.csv`.

Run this command whenever you want to manually refresh the historical dataset.

### 7. Run the Application

```bash
python -m fastapi dev main.py
```

### 8. Open the API Documentation

Visit the following address in your browser:

[Open API Documentation](http://127.0.0.1:8000/docs)

## Project Structure

```text
StockPulse/
│
├── data/
│   ├── stocks.csv
│   ├── watchlist.json
│   └── report_history.json
│
├── modules/
│   ├── __init__.py
│   ├── data_fetcher.py
│   ├── performance_analyzer.py
│   ├── report_generator.py
│   ├── stock_comparator.py
│   ├── trend_analyzer.py
│   └── watchlist_manager.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

**Note:** The watchlist and report history JSON files store locally generated application data and are excluded from version control. The `stocks.csv` file contains the downloaded historical market data.

## API Endpoints

StockPulse provides the following API endpoints:

| Feature | Method | Endpoint |
|---|---|---|
| Home | GET | `/` |
| View Available Stocks | GET | `/stocks` |
| Search Stock | GET | `/stocks/{symbol}` |
| View Stock History | GET | `/stocks/{symbol}/history` |
| Performance Analysis | GET | `/stocks/{symbol}/performance` |
| Trend Analysis | GET | `/stocks/{symbol}/trend` |
| Compare Stocks | GET | `/compare/{symbol1}/{symbol2}` |
| View Watchlist | GET | `/watchlist` |
| Add Stock to Watchlist | POST | `/watchlist/{symbol}` |
| Remove Stock from Watchlist | DELETE | `/watchlist/{symbol}` |
| Generate Report | POST | `/reports/{symbol}` |
| View Report History | GET | `/reports/history` |

Interactive API documentation is available at `/docs` when the application is running.

## Testing and Validation

StockPulse was tested using the interactive Swagger UI provided by FastAPI at `/docs`.

The following test cases were performed:

| No. | Test Case | Expected Result | Status |
|---|---|---|---|
| 1 | Download historical market data | Download data for all seven supported instruments | Passed |
| 2 | View all available instruments | Display all seven instruments with their categories and currencies | Passed |
| 3 | Search for Reliance Industries | Display the correct instrument details | Passed |
| 4 | View Reliance historical data | Display historical OHLCV records | Passed |
| 5 | Analyze Reliance performance | Calculate performance metrics and percentage return | Passed |
| 6 | Analyze Reliance trend | Identify the trend and calculate the price range | Passed |
| 7 | Compare Reliance and TCS | Display their percentage returns and better performer | Passed |
| 8 | Add Reliance to the watchlist | Add the instrument successfully | Passed |
| 9 | View the watchlist | Display saved instruments | Passed |
| 10 | Remove an instrument from the watchlist | Remove the instrument successfully | Passed |
| 11 | Generate a Reliance analysis report | Generate and save the report | Passed |
| 12 | View report history | Retrieve the saved analysis report | Passed |
| 13 | Restart the application | Retain saved watchlist and report history data | Passed |
| 14 | Submit an unknown or blank stock symbol | Return an appropriate error response | Passed |

All listed test cases produced the expected results during testing.

## Limitations

- The application retrieves historical market data using the `yfinance` Python library and does not provide a continuously updating live-market feed.
- Historical data is limited to one year of daily records for the seven supported instruments.
- Market data must be refreshed manually using the data fetcher module.
- Historical data availability depends on the external data provider and the `yfinance` library.
- Gold and Silver Futures data represents international COMEX futures quoted in USD, while NIFTY 50 is measured in index points.
- Trend analysis uses a simplified comparison of starting and ending prices.
- The application currently provides backend functionality through FastAPI and does not yet include a graphical user interface.
- StockPulse is an educational project and does not provide financial or investment advice.

## Future Improvements

The following improvements can be considered for future versions of StockPulse:

- Develop a user-friendly frontend dashboard.
- Add interactive stock charts, graphs and candlestick visualizations.
- Explore integration of a reliable live-market data source.
- Introduce date-based filters for historical stock analysis.
- Improve trend and volatility analysis using additional analytical methods.
- Enhance report generation with detailed visual summaries.
- Expand support for additional stocks, indices and commodities.

## AI Assistance

AI tools were used during the development of StockPulse for concept explanations, programming guidance, debugging assistance and documentation preparation.

The application was developed and tested through practical implementation, with the aim of understanding the Python concepts and functionality used in the project.