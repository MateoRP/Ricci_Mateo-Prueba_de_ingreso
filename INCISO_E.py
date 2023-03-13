
"INCISO E"

#Datos para el testeo de la formula.
SPOT_PRICE = 100
FUTURES_PRICE = 200
DAYS_TO_MAT = 126
DAYS_IN_YEAR = 252

#Función que evalúa la tasa implícita de manera unitaria.
def test_implied_rate(SPOT,FUT,MAT,YEAR):
    return ((FUT/SPOT)**(1/(YEAR/MAT)))-1

print(test_implied_rate(SPOT_PRICE,FUTURES_PRICE,DAYS_TO_MAT,DAYS_IN_YEAR))

