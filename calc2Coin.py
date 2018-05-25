import urllib.request
import json
import collections
import sqlite3
from coins import coins

def bsToCoin(bsToUsd, usdToCoin, n):
    percent = 1.10
    return n*bsToUsd*usdToCoin*percent

def takeId(elem):
    return int(elem[1]['id'])



conn = sqlite3.connect('coins.db')

print('Calculadora de Bs a divisas.')


'''
Pedimos valor del Dolar
'''
bsToUsd = 1/float(input('Ingrese valor del Dolar en Bs: '))
numBs = float(input('Cantidad de Bs: '))

'''
Obtenemos valores.
'''
try:
    '''
    De la API
    '''
    for coin in coins:
        coin_obj = coins.get(coin)

        # Request a la API de coinmarketcap
        url = 'https://api.coinmarketcap.com/v2/ticker/{}/'.format(coins[coin]['id'])
        webUrl = urllib.request.urlopen(url)
        response = webUrl.read()
        encoding = webUrl.info().get_content_charset('utf-8')
        data = json.loads(response.decode(encoding))
        usdToCoin = 1/float(data['data']['quotes']['USD']['price'])

        coin_obj['usdToCoin'] = usdToCoin*coins[coin]['factor']

        '''
        Actualizamos la base de datos
        '''
        c = conn.cursor()
        params = (coin_obj['usdToCoin'], coin, )
        c.execute('UPDATE coins SET price = ? WHERE name = ?', params)

    conn.commit()

except Exception as e:
    '''
    De la base de datos
    '''
    for coin in coins:
        coin_obj = coins.get(coin)
        c = conn.cursor()
        params = (coin, )
        c.execute('SELECT price FROM coins where name=?', params)
        price = c.fetchone()
        coin_obj['usdToCoin'] = price[0]*1.02


'''
Imprimimos valores, ordenados por ID
'''
conn.close()
print('\n\nConversión:')
print('Dolar: {0:.2f}\n'.format(numBs*bsToUsd))
orderedCoins = collections.OrderedDict(sorted(coins.items(), key=takeId))


for t in orderedCoins.items():
    coin = t[0]
    print(coins[coin]['format'].format(coin, bsToCoin(bsToUsd, coins[coin]['usdToCoin'], numBs)))
