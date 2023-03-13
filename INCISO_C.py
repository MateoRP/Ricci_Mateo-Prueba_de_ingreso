import pyRofex
from datetime import datetime
import numpy as np
import yfinance as yf
import pandas as pd


" INCISO B - TASAS IMPLÍCITAS PARA LOS FUTUROS DE LOS SUBYACENTES GGAL, PAM, YPF Y DÓLAR"


#Inicializa la conexión con ecosistema de REMARKET
pyRofex.initialize(user="mricci7850",
                   password="cwjzkD2$",
                   account="REM7850",
                   environment=pyRofex.Environment.REMARKET)

#Tickers de los contratos de los futuros y acciones subyacentes usados para los cálculos de las tasas.
futures_tickers = ["DLR/ABR23","DLR/JUN23","PAMP/ABR23","PAMP/JUN23","YPFD/ABR23","YPFD/JUN23","GGAL/ABR23","GGAL/JUN23"]
spot_tickers = ["USDARS=X","PAMP.BA","YPFD.BA","GGAL.BA"]

#Indicación: Abrir cada función, el desarrollo interno está explicado debidamente.

def bus_days_till_mat(ticker):
    # Guarda en "info" los detalles del instrumento "ticker"
    info = pyRofex.get_instrument_details(ticker=ticker)

    # Guarda la fecha de "maturity" en formato datetime
    maturity = datetime.strptime(info['instrument']['maturityDate'], '%Y%m%d')

    # Convierto a string y hago un split guardando solamente %Y%m%d para la función np.busday_count
    mat_str = str(maturity)[:10]

    #Dependiendo de si el BID y ASK del instrumento está disponible, la respuesta de la función
    # "futures_market_data()" será una lista de 2 o 4 elementos. *Posible optimización -> Que sea siempre de 4*
    if len(futures_market_data(ticker)) == 2:
        #Guardo en date_ms la fecha de la información descargada.
        date_ms = futures_market_data(ticker)[1]
    elif len(futures_market_data(ticker)) == 4:
        # Guardo en date_ms la fecha de la información descargada.
        date_ms = futures_market_data(ticker)[3]

    #Puede ocurrir que no se incluya fecha, en ese caso tomamos la fecha del presente.
    if date_ms == None:

        now_str = str(datetime.now())[:10]
    else:

        #Como la fecha esta en formato de tiempo Unix en milisegundos lo convierto a string "%Y%m%d".
        now_str = str(datetime.fromtimestamp(date_ms/1000))[:10]

    #Devuelvo la cantidad de días entre la fecha de maturity del contrato y el dato más reciente descargado,
    # el cual podría no ser hoy y ahora.
    return int(np.busday_count(now_str,mat_str))

def futures_market_data(ticker):

    #Guardo en data la información más reciente sobre el contrato "ticker".
    data = pyRofex.get_market_data(ticker=ticker)

    #Condición: ¿La información descargada contiene un precio BID?
    if len(data['marketData']['BI'])>0:

        # Si, guardar en variable BID.
        BID = data['marketData']['BI'][0]['price']
    else:

        #No, guardar None en BID.
        BID = None

    # Condición: ¿La información descargada contiene un precio ASK?
    if len(data['marketData']['OF'])>0:

        # Si, guardar en variable ASK.
        ASK = data['marketData']['OF'][0]['price']
    else:

        # No, guardar None en variable ASK.
        ASK = None

    # Condición: ¿La información descargada contiene un precio LAST? (Último precio)
    if data['marketData']['LA'] != None:

        # Si, guardar el dato en la variable LAST y su fecha en DATE.
        LAST = data['marketData']['LA']['price']
        if LAST == None:
            LAST = data['marketData']['CL']['price']
        DATE = data['marketData']['LA']['date']
    else:

        # No, guardar none tanto en la variable LAST como en DATE.
        LAST = None
        DATE = None

    # Si alguno de las condiciones anteriormente planteadas fue resuelta positivamente devolve las cuatro variables.
    if BID != None or ASK != None or LAST != None or DATE != None:
        return [BID,ASK,LAST,DATE]

    # Si no, devolver el CLOSE price (que siempre está) y su fecha.
    else:
        return [data['marketData']['CL']['price'],data['marketData']['CL']['date']]

def spot_last_close_price(ticker):

    #Devuelve el último precio de la plataforma de Yahoo Finance del contrato "ticker" (lo usamos para el subyacente).
    return yf.Ticker(ticker).history(period="5d").iloc[0]['Close']

def futures_implied_rate(fut_ticker,spot_ticker,input="LAST",printout=0):

    #Obtenemos el último precio del subyacente "spot_ticker".
    S0 = spot_last_close_price(spot_ticker)

    #Obtenemos el tiempo hasta la maturity del contrato de futuro "fut_ticker".
    Time_to_mat = bus_days_till_mat(fut_ticker)

    # *Posible optimización -> Integración de bus_days_till_mat() y futures_market_data() con POO*
    #                       -> futures_market_data() -> Devolver un mensaje len()=4, con posición 3 = precio y
    #                                                   posisición 4 = fecha.

    #Obtenemos los precios y fecha del contrato de futuro "fut_ticker".
    fut_data = futures_market_data(fut_ticker)

    #Condición: Largo del mensaje para no encontrar error mediante indexeo más adelante.
    if len(fut_data) == 2:

        #Si el imput es ASK, BID o LAST y el mensaje es de len()=2, no se va a cumplir lo solicitado.
        #Porque el mensaje tendrá el CLOSE price solamente (len()=2). Devuelve este último y eleva aviso.
        if input == "ASK" or input == "BID" or input == "LAST":
            if printout == 1:
                print("Requested price not available. Using close price instead.")
        S1 = fut_data[0]

    #Si BID, ASK o LAST está disponible, guarda en la variable S1 el precio solicitado.
    elif len(fut_data) == 4:
        if input == "BID":
            S1 = fut_data[0]
        if input == "ASK":
            S1 = fut_data[1]
        if input == "LAST":
            S1 = fut_data[2]
        if S1 == None:
            S1 = S0

    #Guarda en la variable rate la tasa implicita del futuro calculando mediante la formula.
    rate = ((S1 / S0) ** (1 / (252 / Time_to_mat))) - 1

    #Si el usuario lo eligiera, imprime en consola los datos conseguidos.
    if printout == 1:
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        print(f"The implied rate is {rate*100}%")
        print(f"{fut_ticker} (futures contract) - {input} Price: {S1} | Time to maturity: {Time_to_mat} | {spot_ticker} (stock) - Price: {S0} |")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        return ""

    #Si el usuario lo eligiera, devuelve la tasa implicita del futuro.
    elif printout == 0:
        return ((S1/S0)**(1/(252/Time_to_mat)))-1


#Crea un dataframe que almacenara todas las tasas implícitas de los diferentes contratos.
implied_rates = pd.DataFrame(columns = ['rate (%)'])

counter = -1
row = []


#Recorre la lista de contratos (futuros y spot) usando for.
for i in range(4):
    for j in range(2):
        counter += 1

        #Guardo una fila nueva con el nombre del ticker del contrato de futuro y conteniendo la tasa implicita del mismo.
        implied_rates.loc[futures_tickers[counter]] = futures_implied_rate(futures_tickers[counter], spot_tickers[i], "LAST", 0)*100

#Imprimo el dataframe resultante.
print(implied_rates)








