# librerias para gestionar datos y graficos
import numpy as np
import matplotlib.pyplot as plt
# api cassandra
from cassandra.cluster import Cluster
# listado indicadores
tablas = ['aviones', 'pasajeros', 'mercancias']
# conexion a cassandra
session = Cluster().connect('aviones_en_canarias')
# succesion temporal de los meses desde 01/2000 hasta 12/2019
x = np.linspace(2000, 2020, 20*12)
# bucle de los indicadores
for i, t in enumerate(tablas):
    y = list(map(lambda r : r[0], session.execute(f"SELECT valor FROM {t} WHERE aeropuerto='Canarias' AND ano>=2000 AND ano<=2019")))
    # calculo regresion lineal
    coefficients = np.polyfit(x, y, 1)
    m = coefficients[0]
    b = coefficients[1]
    line = m * x + b
    # creacion subgrafico
    plt.subplot(1, 3, i+1)
    plt.scatter(x, y, color='blue')
    plt.plot(x, line, color='red')
    plt.title('{}'.format(t.capitalize()))
# visualizacion
plt.suptitle("Regresión lineal de los indicadores en todos los aeropuertos de Canarias")
plt.show()
