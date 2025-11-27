from fastapi import FastAPI
import yfinance as yf
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="My Stock App - Backend")

# Allow all origins for testing (you can restrict later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <- for development, use ["http://localhost:5500"] or similar
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
