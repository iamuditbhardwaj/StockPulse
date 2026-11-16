# StockPulse

### Stock Market Learning and Analysis Application

StockPulse is a Python-based stock market learning and analysis application built using FastAPI.

It allows users to explore historical market data, analyze price performance and trends, compare market instruments, manage multiple watchlists and generate downloadable stock analysis reports.

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

1. **Stock Explorer:** View available market instruments, their categories, currencies and historical OHLCV price data.

2. **Performance Analyzer:** Calculate starting price, ending price, highest price, lowest price, average price, price change and percentage return for a selected instrument and date range.

3. **Trend Analyzer:** Identify whether an instrument shows an uptrend, downtrend or sideways trend using historical price information.

4. **Stock Comparator:** Compare the performance of multiple instruments and analyze their percentage returns.

5. **Watchlist Management:** Create and manage multiple named watchlists, switch between them, add or remove instruments and delete watchlists.

6. **Report Generator:** Generate stock analysis reports containing performance and trend information.

7. **PDF and CSV Report Downloads:** Export generated analysis reports in PDF and CSV formats.

8. **Report History:** Save and retrieve previously generated analysis reports.

9. **Historical Data Management:** Download and locally store historical market data for the supported instruments.

The complete StockPulse application also includes a React-based frontend with interactive charts and analysis interfaces. The frontend source code is maintained separately and is not included in this backend-only GitHub repository.

## Technologies Used

- **Python:** Core programming language.
- **FastAPI:** Backend framework for building API endpoints.
- **yfinance:** Retrieves historical market data.
- **Pandas:** Supports historical market data processing.
- **ReportLab:** Generates downloadable PDF reports.
- **CSV:** Stores downloaded historical market data and supports CSV report exports.
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

This installs the Python packages required to run the application.

### 6. Download Historical Market Data

Run the following command from the project folder:

```bash
python -c "from modules.data_fetcher import refresh_stock_data; refresh_stock_data()"
```

This downloads one year of daily historical data for the seven supported instruments and saves it in `data/stocks.csv`.

Run this command whenever you want to manually refresh the historical dataset.

Historical data availability depends on the external data provider.

### 7. Run the Application

```bash
python -m uvicorn main:app --reload
```

### 8. Open the API Documentation

Visit the following address in your browser:

[Open API Documentation](http://127.0.0.1:8000/docs)

FastAPI provides interactive Swagger documentation for exploring and testing the available endpoints.

## Project Structure

```text
StockPulse/
│
├── data/
│   └── stocks.csv
│
├── modules/
│   ├── __init__.py
│   ├── data_fetcher.py
│   ├── performance_analyzer.py
│   ├── report_generator.py
│   ├── report_exporter.py
│   ├── stock_comparator.py
│   ├── trend_analyzer.py
│   └── watchlist_manager.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

**Note:** `stocks.csv` contains the historical market dataset. The application creates or updates local JSON files for watchlist information and report history as required. These locally generated application files are not included in the GitHub repository.

## API Endpoints

StockPulse provides the following API endpoints:

### General and Stock Data

| Feature | Method | Endpoint |
|---|---|---|
| Home | GET | `/` |
| View Available Stocks | GET | `/stocks` |
| Search Stock | GET | `/stocks/{symbol}` |
| View Stock History | GET | `/stocks/{symbol}/history` |

### Performance and Trend Analysis

| Feature | Method | Endpoint |
|---|---|---|
| Performance Analysis | GET | `/stocks/{symbol}/performance` |
| Trend Analysis | GET | `/stocks/{symbol}/trend` |
| Compare Two Stocks | GET | `/compare/{symbol1}/{symbol2}` |

### Watchlist Management

| Feature | Method | Endpoint |
|---|---|---|
| View Default Watchlist | GET | `/watchlist` |
| Add to Default Watchlist | POST | `/watchlist/{symbol}` |
| Remove from Default Watchlist | DELETE | `/watchlist/{symbol}` |
| View All Watchlists | GET | `/watchlists` |
| Create a Watchlist | POST | `/watchlists` |
| View a Specific Watchlist | GET | `/watchlists/{watchlist_id}` |
| Set Active Watchlist | PUT | `/watchlists/{watchlist_id}/active` |
| Delete a Watchlist | DELETE | `/watchlists/{watchlist_id}` |
| Add Stock to a Watchlist | POST | `/watchlists/{watchlist_id}/stocks/{symbol}` |
| Remove Stock from a Watchlist | DELETE | `/watchlists/{watchlist_id}/stocks/{symbol}` |

### Report Management

| Feature | Method | Endpoint |
|---|---|---|
| Generate Analysis Report | POST | `/reports/{symbol}` |
| View Report History | GET | `/reports/history` |
| Download Report | GET | `/reports/{symbol}/download?format=pdf` |
| Download Report | GET | `/reports/{symbol}/download?format=csv` |

Interactive API documentation is available at `/docs` when the application is running.

## Testing and Validation

StockPulse was tested using the interactive Swagger UI provided by FastAPI at `/docs`, along with the application's frontend interfaces.

The following test cases were performed:

| No. | Test Case | Expected Result | Status |
|---|---|---|---|
| 1 | Download historical market data | Download data for all seven supported instruments | Passed |
| 2 | View all available instruments | Display all seven instruments with their categories and currencies | Passed |
| 3 | Search for Reliance Industries | Display the correct instrument details | Passed |
| 4 | View Reliance historical data | Display historical OHLCV records | Passed |
| 5 | Analyze Reliance performance | Calculate performance metrics and percentage return | Passed |
| 6 | Analyze Reliance trend | Identify the trend and calculate the price range | Passed |
| 7 | Compare instruments | Display comparative performance information | Passed |
| 8 | Add an instrument to a watchlist | Add the instrument successfully | Passed |
| 9 | Create and switch between watchlists | Manage multiple named watchlists | Passed |
| 10 | View saved watchlists | Display saved instruments and watchlist information | Passed |
| 11 | Remove an instrument from a watchlist | Remove the instrument successfully | Passed |
| 12 | Generate an analysis report | Generate and save the report | Passed |
| 13 | Download a PDF report | Generate and download the PDF file | Passed |
| 14 | Download a CSV report | Generate and download the CSV file | Passed |
| 15 | View report history | Retrieve previously generated reports | Passed |
| 16 | Restart the application | Retain saved watchlist and report history data | Passed |
| 17 | Submit an unknown or blank stock symbol | Return an appropriate error response | Passed |

All listed test cases produced the expected results during project testing.

## Limitations

- The application retrieves historical market data using the `yfinance` Python library and does not provide a continuously updating live-market feed.
- Historical data is limited to approximately one year of daily records for the seven supported instruments.
- Market data must be refreshed manually using the data fetcher module.
- Historical data availability depends on the external data provider and the `yfinance` library.
- Gold and Silver Futures data represents international COMEX futures quoted in USD, while NIFTY 50 is measured in index points.
- Trend analysis uses a simplified comparison of historical starting and ending prices.
- The GitHub repository contains the Python backend; the React frontend is maintained separately.
- StockPulse is an educational project and does not provide financial or investment advice.

## Future Improvements

The following improvements can be considered for future versions of StockPulse:

- Include the React frontend source code in the main repository.
- Explore integration of a reliable live-market data source.
- Improve trend and volatility analysis using additional analytical methods.
- Expand historical data coverage and support additional stocks, indices and commodities.
- Enhance report generation with more detailed visual summaries.
- Introduce additional learning resources and educational features.

## AI Assistance

AI tools were used during the development of StockPulse for concept explanations, programming guidance, debugging assistance and documentation preparation.

The application was developed and tested through practical implementation, with the aim of understanding the Python concepts, technologies and functionality used in the project.