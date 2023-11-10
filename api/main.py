description = """ This API helps you query data from a MySQL database.
The data are available from the Binance API

## Queries
* Get marche from the table
* Save a new marche crypto bot in the table
"""

from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
import uvicorn

app = FastAPI(
    title='Projet OPA Crypto API',
    description=description,
    version="0.0.1",
    contact={}
)

class MarcheSchema(BaseModel):
    id: int
    date_time: str
    symbol: str
    priceChange: float
    priceChangePercent: float
    weightedAvgPrice: float
    prevClosePrice: float
    lastPrice: float
    lastQty: float
    bidPrice: float
    bidQty: float
    askPrice: float
    askQty: float
    openPrice: float
    highPrice: float
    lowPrice: float
    volume: float
    quoteVolume: float
    openTime: float
    closeTime: float
    firstId: int
    lastId: int
    count: int


######
## Database info
########
mydb = mysql.connector.connect(host='localhost',
                               port='3306',
                               database='cryptobot',
                               user='root',
                               password='Password')


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}

@app.get("/")
async def root():
    return ResponseModel("message", "Hello World")

# @validate
# Get all marches
@app.get("/marches")
async def get_marches():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM cryptobot.botmarche")
    result = cursor.fetchall()
    return ResponseModel(result, "All marches received.")

# Get an marche by symbol
@app.get("/marche/{symbol}")
async def get_marche(symbol: str):
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM cryptobot.botmarche WHERE symbol = '{symbol}'")
    result = cursor.fetchone()
    return ResponseModel(result, f"symbol = {symbol} received.")

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")