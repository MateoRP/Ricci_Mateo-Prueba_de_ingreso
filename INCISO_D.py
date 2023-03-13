import time
import pandas as pd
import pyRofex
from datetime import datetime
import numpy as np
import yfinance as yf

"INCISO D - TASAS IMPLÍCITAS TOMADORAS Y COLOCADORAS EN TIEMPO REAL"

#Inicializa la conexión con ecosistema de REMARKET
pyRofex.initialize(user="mricci7850",
                   password="cwjzkD2$",
                   account="REM7850",
                   environment=pyRofex.Environment.REMARKET)

#Creo el dataframe donde almacenaré los datos recolectados y procesados.
prices = pd.DataFrame(columns=["SPOT","BID","BID rate", "ASK","ASK rate", "TIME","DAYS TILL MAT.","ARBITRAGE"])

#A partir del contrato de futuro "ticker", devuelve el ticker de su stock subyacente.
def what_spot(ticker):
    if ticker in ["DLR/ABR23","DLR/JUN23"]:
        return "USDARS=X"
    elif ticker in ["PAMP/ABR23","PAMP/JUN23"]:
        return "PAMP.BA"
    elif ticker in ["YPFD/ABR23","YPFD/JUN23"]:
        return "YPFD.BA"
    elif ticker in ["GGAL/ABR23","GGAL/JUN23"]:
        return "GGAL.BA"

#Ingresando el ticker de un contrato de futuro y una fecha "now" en formato Unix en milisegundos. Devuelva la
# cantidad de días desde la fecha "now" hasta el vencimiento del contrato.
def bus_days_till_mat(ticker,now):

    #Guardo en "info" la información del contrato de futuro "ticker"
    info = pyRofex.get_instrument_details(ticker=ticker)

    #Guardo en "maturity" la fecha de maturity contenida en la información descargada en formato datetime.
    maturity = datetime.strptime(info['instrument']['maturityDate'], '%Y%m%d')

    #Convierto la fecha de maturity del contrato a string y conservo "%Y%m%d" solamente.
    mat_str = str(maturity)[:10]

    #Convierto la "now" de formato Unix en milisegundos a string y conservo "%Y%m%d" solamente.
    now_str = str(datetime.fromtimestamp(now/1000))[:10]

    #Devuelvo la cantidad de días entre las fechas de formato string "mat_str" y "now_str".
    return np.busday_count(now_str,mat_str)

#Función que procesa el mensaje ("message") recibido usando la conexión de Websocket.
def market_data_handler(message):

    #Guardo el ticker del contrato contenido en el mensaje.
    ticker = message['instrumentId']['symbol']

    #Guardo la fecha del mensaje.
    time = message['timestamp']

    #Usando "what_spot()" guardo el último precio del subyacente al contrato de futuro "ticker".
    spot = yf.Ticker(what_spot(ticker)).history(period="5d").iloc[0]['Close']

    #Convierto y guardo la fecha del mensaje en formato string quedandome con fecha, hora, minutos y segundos.
    time_df = str(datetime.fromtimestamp(time/1000))[:19]

    #Guardo la cantidad de días hasta la maturity del contrato de futuro ticker usando bus_days_till_mate().
    days_till_mat = bus_days_till_mat(ticker,time)

    arbitrage = "No"

    #Condición: ¿Tiene el mensaje BID price?
    if len(message['marketData']['BI']) == 0:

        #No, guardo None en BI y BI_rate.
        BI = None
        BI_rate = None
    else:

        #Si, guardo el precio en la variable BI y calculo la tasa implicita COLOCADORA y la guarod en BI_rate.
        BI = message['marketData']['BI'][0]['price']
        BI_rate = ((BI / spot) ** (1 / (252 / days_till_mat))) - 1


    if len(message['marketData']['OF']) == 0:

        #No, guardo None en las variables OF y OF_rate.
        OF = None
        OF_rate = None
    else:

        # Si, guardo el precio en la variable ASK y calculo la tasa implicita TOMADORA y la guardo en ASK_rate.
        OF = message['marketData']['OF'][0]['price']
        OF_rate = ((OF / spot) ** (1 / (252 / days_till_mat))) - 1

    #Condición: ¿Tengo ambas tasas implícitas (tanto TOMADORA como COLOCADORA de precio)?
    if OF_rate != None and BI_rate != None:

        #Si, Condición: ¿Es la ASK implied rate menor que la BID implied rate?
        if OF_rate < BI_rate:

            #Si, hay arbitraje.
            arbitrage = "Yes"

        #No, ya había definido inicialmente "arbitrage = "No""

    #Agrego al dataframe (o reemplazo si ya existe), la fila de "ticker" con todos los datos conseguidos.
    prices.loc[ticker] = spot,BI,BI_rate, OF,OF_rate, time_df, days_till_mat,arbitrage

    #Por default muestro el dataframe en pantalla.
    print(prices.to_markdown(),"\n")

#Funciones para manejo de errores y excepciones.
def error_handler(message):
    print("Error Message Received: {0}".format(message))
def exception_handler(e):
    print("Exception Occurred: {0}".format(e.msg))


# Inicializo la conexión Websocket
pyRofex.init_websocket_connection(market_data_handler=market_data_handler,
                                  error_handler=error_handler,
                                  exception_handler=exception_handler)

# Guardo manualmente los contratos de futuros a los que me voy a suscribir.
instruments = ["DLR/ABR23","DLR/JUN23","PAMP/ABR23","PAMP/JUN23","YPFD/ABR23","YPFD/JUN23","GGAL/ABR23","GGAL/JUN23"]  # Instruments list to subscribe

# Guardo las variables que me interesan obtener cuando me suscriba.
entries = [pyRofex.MarketDataEntry.BIDS,
           pyRofex.MarketDataEntry.OFFERS,
           pyRofex.MarketDataEntry.LAST]

#Me suscribo para recibir mensajes con "market data" con la funcionalidad Websocket. Esto va a comenzar el
# proceso en cual recibo cualquier modificación en precios o fecha de los instrumentos adheridos.
#Cada vez que llegue un mensaje, el market_data_handler recibirá el mensaje y ejecutara el código explicado.
pyRofex.market_data_subscription(tickers=instruments,
                                 entries=entries)
