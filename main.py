from fastapi import FastAPI

app = FastAPI(title="StockPulse")

@app.get("/")
def home():
    return {
        "message": "Welcome to StockPulse",
        "project": "Stock Market Learning and Analysis"
    }