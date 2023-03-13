## Mateo Ricci | Prueba de ingreso a MRM Analytics

### Descripción
Este proyecto consiste en la construcción de un bot que busca oportunidades de arbitraje de tasa de interés en la plataforma  ReMarkets de Rofex, utilizando el paquete pyRofex y calculando las tasas implícitas para los futuros GGAL, PAM, YPF y dólar.

Aclaración: Los ejercicios de los incisos "c","d" y "e" fueron resueltos y subidos en archivos diferentes. 

### Librerías 
* **pyRofex**
* **yfinance**
* **numpy**
* **pandas**


### Funciones
* **bus_days_till_mat**: A partir del ticker de un futuro devuelve la cantidad de días hasta el vencimiento del contrato.
* **futures_market_data**: Devuelve los diferentes precios (*Bid*,*Ask*, *Last*, etc.), dependiendo de la información disponible.
* **spot_last_close_price**: A partir del ticker de una acción devuelve el último precio registrado en la plataforma de *Yahoo Finance*.
* **futures_implied_rate**: A partir del ticker de un futuro y el de su subyacente, devuelve la tasa interna de retorno del contrato.
* **what_spot**: A partir del ticker de un futuro devuelve el ticker del contrato del subyacente (limitado a los instrumentos del proyecto).
* **bus_days_till_mat**: A partir del ticker de un futuro y una fecha en formato de tiempo Unix en milisegundos (13 digítos).
* **market_data_handler**: Función que procesa el mensaje recibido usando la conexión de Websocket. En particular, guarda los datos recibidos y los procesa en un dataframe.

