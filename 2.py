import pyRofex
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import time

pyRofex.initialize(user="mricci7850",
                   password="cwjzkD2$",
                   account="REM7850",
                   environment=pyRofex.Environment.REMARKET)

futures_tickers = ["DLR/ABR23","DLR/JUN23","PAMP/ABR23","PAMP/JUN23","YPFD/ABR23","YPFD/JUN23","GGAL/ABR23","GGAL/JUN23"]
spot_tickers = ["USDARS=X","PAMP.BA","YPFD.BA","GGAL.BA"]

def futures_market_data(ticker):
    data = pyRofex.get_market_data(ticker=ticker)
    if len(data['marketData']['BI'])>0:
        BID = data['marketData']['BI'][0]['price']
    else:
        BID = None
    if len(data['marketData']['OF'])>0:
        ASK = data['marketData']['OF'][0]['price']
    else:
        ASK = None
    if data['marketData']['LA'] != None:
        LAST = data['marketData']['LA']['price']
        DATE = data['marketData']['LA']['date']
    else:
        LAST = None
        DATE = None
    if BID != None or ASK != None or LAST != None or DATE != None:
        return [BID,ASK,LAST,DATE]
    else:
        return [data['marketData']['CL']['price'],data['marketData']['CL']['date']]

print(futures_market_data(futures_tickers[0]))
your_dt = datetime.fromtimestamp(1678625407234/1000)  # using the local timezone
print(your_dt.strftime("%Y-%m-%d %H:%M:%S"))
#2023-03-13 01:07:35.770