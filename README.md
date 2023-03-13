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


### Desarrollo del código

#### Inciso C
**Objetivo**: Calcular las tasas implícitas para los futuros GGAL, PAM, YPF, y al menos un plazo de futuro de dólar.


**Desarrollo**:
* Inicializo la conexión con reMarkets.
* Para calcular la tasa implícita necesito tres datos fundamentales: Precio del futuro (S1), precio del spot (S0),cantidad de días hasta el vencimiento (DTM) y cantidad de días en un año (AÑO, asumo fijo y que es 252).
* Tasa implícita del futuro = ((S1/S0)^(DTM/AÑO))-1
* Uso **bus_days_till_mat** para obtener la cantidad de días hasta el vencimiento.
* **futures_market_data** para obtener el precio del futuro.
* **spot_last_close_price** para obtener el precio del spot.
* Itero para todos los contratos seleccionados.

Resultados 13/03/2023:

|               | rate (%)      |
| ------------- |:-------------:|
| DLR/ABR23     | 1.486340      |
| DLR/JUN23     | 7.988572      |
| PAMP/ABR23    | 1.142761      |
| PAMP/JUN23    | 0.000000      |
| YPFD/ABR23    | 0.058302      |
| YPFD/JUN23    | 3.953985      |
| GGAL/ABR23    | 0.974807      |
| GGAL/JUN23    | 7.510603      |

   
#### Inciso D
**Objetivo**: Imprimir en consola las tasas implícitas tomadoras y colocadoras cada vez que haya una modificación en los precios, luego indique si hubiera las oportunidades de arbitraje.

**Desarrollo**:
* Inicializo la conexión con reMarkets.
* Para conseguír las tasas implícitas tomadoras y colocadoras necesito los mismo datos que el incíso anterior con la excepción del precio del contrato de futuro, que debe ser ASK o BID respectivamente.
*Para que mi programa calcule las tasas automaticamente cada vez que se modifican los precios uso la conexión WebSocket de byRofex, que envía mensajes a mi cliente una vez suscripto a la comunicación y a ciertos intrumentos y tipo de datos en particular.
*Considero que, a partir del enunciado. La oportunidad de arbitraje se presenta cuando la "implied BID rate" es mayor a la "implied ASK rate".
*Utilizando las funciones de manejo de mensaje proporcionadas por los documentos de byRofex se establece la conexión WebSocket y se empieza a recibir un mensaje con información sobre los contratos: BID, ASK, FECHAS, etc.
*En mi función **market_data_handler** (la cual se ejecuta cada vez que mi cliente recibe un mensaje), guardo el ASK price, BID price, FECHA y aprovecho esta instancia de tiempo para guardar el precio del SPOT usando **what_spot** y **spot_last_close_price** y cantidad de días hasta el vencimiento usando **bus_days_till_mat**.
*A medida que recibo los mensajes de los diferentes contratos guardo la información en un dataframe y computo la tasa implicita TOMADORA y COLOCADORA. Además, mediante un simple condicional busco posible oportunidades de arbitraje e imprimo todo en consola.

#### Inciso E

**Objetivo**: Test unitario que evalúe la tasa implicita de un futuro.

**Desarrollo**:
* Función simple de la fórmula ya explicitada.


