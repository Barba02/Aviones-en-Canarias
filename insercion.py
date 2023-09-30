# modulo para leer datos en un fichero .csv
import csv
# api por interrogar Cassandra
from cassandra.cluster import Cluster

# conexion a la base de datos en nuestro keyspace
session = Cluster().connect('aviones_en_canarias')
tablas = ['pasajeros', 'aviones', 'mercancias']
# creacion tablas
for t in tablas:
    session.execute("CREATE TABLE IF NOT EXISTS {} (aeropuerto text, ano int, mes int, valor int, PRIMARY KEY (aeropuerto, ano, mes))".format(t))
# lectura de los datos en csv
with open('aviones.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader, None) # pasa primera riga de intestacion
    count = 0
    for row in reader:
        # insercion solo de valores absolutos
        if (row[1] == 'Valores absolutos'):
            count += 1
            # conversion en entero del valor
            num = row[6][0:row[6].index('.')]
            valor = 0 if num == '' else int(num)
            # nombre aeropuerto
            aeropuerto = row[3][14:] if ('Aeropuerto de ' in row[3]) else row[3]
            # periodo
            ano = row[4][:4]
            mes = row[4][5:]
            # insercion en la respectiva tabla
            if (row[0] == 'Pasajeros'):
                index = 0
            elif (row[0] == 'Aviones'):
                index = 1
            else:
                index = 2
            session.execute("INSERT INTO {}(aeropuerto, ano, mes, valor) VALUES ('{}', {}, {}, {})".format(tablas[index], aeropuerto, ano, mes, valor))
# comprobacion
for t in tablas:
    query = session.execute('SELECT COUNT(*) FROM {}'.format(t))
    count -= query[0][0]
print("Todos los registros fueron insertados correctamente" if count == 0 else "Ha ocurrido un error")
