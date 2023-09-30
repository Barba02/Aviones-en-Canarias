# librerias para gestionar datos y graficos
import numpy as np
import matplotlib.pyplot as plt
# api cassandra
from cassandra.cluster import Cluster
# conexion a cassandra
session = Cluster().connect('aviones_en_canarias')
# bucle de todos los aeropuertos
aeropuertos = list(map(lambda r : r[0], session.execute(f"SELECT DISTINCT aeropuerto FROM aviones")))
aeropuertos.remove('Tenerife')
aeropuertos.remove('Canarias')
for i, a in enumerate(aeropuertos):
    # busqueda de los datos
    x = list(map(lambda r : r[0], session.execute(f"SELECT valor FROM aviones WHERE aeropuerto='{a}' AND ano>=2000 AND ano<=2019")))
    y1 = list(map(lambda r : r[0], session.execute(f"SELECT valor FROM pasajeros WHERE aeropuerto='{a}' AND ano>=2000 AND ano<=2019")))
    y2 = list(map(lambda r : r[0], session.execute(f"SELECT valor FROM mercancias WHERE aeropuerto='{a}' AND ano>=2000 AND ano<=2019")))
    # creacion del subgrafico
    plt.subplot(2, 4, i+1)
    # calculo correlacion y creacion grafico aviones/pasajeros
    pasajeros_coeff = np.corrcoef(x, y1)[0, 1]
    plt.scatter(x, y1, 3)
    plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y1, 1))(np.unique(x)), color='red')
    # calculo correlacion y creacion grafico aviones/mercancias
    mercancias_coeff = np.corrcoef(x, y2)[0, 1]
    plt.scatter(x, y2, 3)
    plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y2, 1))(np.unique(x)), color='green')
    # titulo
    plt.title(f'{a}: {pasajeros_coeff:.2f}, {mercancias_coeff:.2f}')
# visualizacion
plt.suptitle('Correlación aviones/pasajeros (azul-rojo) y aviones/mercancias (naranja-verde)')
plt.show()
