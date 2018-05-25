import sqlite3
from coins import coins

conn = sqlite3.connect('coins.db')

print('Calculadora de Bs a divisas.')

'''
Creamos la tabla
'''
try:
    c = conn.cursor()
    c.execute('''CREATE TABLE
    coins (name varchar(255), price double)
        ''')
    print('Tabla creada')
except Exception as e:
    print(e)

'''
Llenamos la tabla
'''
try:
    for coin in coins:
        c = conn.cursor()
        params = (coin, 0,)
        c.execute('INSERT INTO coins(name, price) VALUES(?, ?)', params)

    print('Tabla llenada')

except Exception as e:
    print(e)

conn.commit()
conn.close()