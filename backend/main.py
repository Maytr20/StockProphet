from fastapi import FastAPI
import yfinance as yf
import pandas as pd

app = FastAPI(title="My Stock App - Backend")

@app.get("/prices/{symbol}")
def get_prices(symbol: str, period: str = "1mo"):
    df = yf.download(symbol, period=period, auto_adjust=True)

    if df.empty:
        return {"error": "No data found"}

    # Flatten multi-index columns (common cause of JSON errors)
    df.columns = df.columns.map(str)

    df = df.reset_index()

    # Convert Timestamp → string
    df["Date"] = df["Date"].astype(str)

    # Convert numeric to Python float
    df = df.map(lambda v: float(v) if isinstance(v, (int, float)) else v)

    return df.to_dict(orient="records")
