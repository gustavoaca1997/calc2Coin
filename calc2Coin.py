import urllib.request
import json
import collections

percent = 1.10

def bsToCoin(bsToUsd, usdToCoin, n):
	return n*bsToUsd*usdToCoin*percent

def takeId(elem):
	return int(elem[1]['id'])

coins = {
	'GBYTE': {
		'id': '1492',
		'usdToCoin': 0,
		'factor': 1,
		'format': '{0} {1:.6f}'
	},
	'MBYTE': {
		'id': '1492',
		'usdToCoin': 0,
		'factor': 1e3,
		'format': '{0} {1:.2f}'
	},
	'DASH': {
		'id': '131',
		'usdToCoin': 0,
		'factor': 1,
		'format': '{0} {1:.6f}'
	}
}

print('Calculadora de Bs a divisas.')

'''
Pedimos valor del Dolar
'''
bsToUsd = 1/float(input('Ingrese valor del Dolar en Bs: '))
numBs = float(input('Cantidad de Bs: '))

'''
Iteramos por los coins y obtenes los valores.
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
Imprimimos valores, ordenados por ID
'''
print('\nConversión:')
print('Dolar: {0:.2f}'.format(numBs*bsToUsd))
orderedCoins = collections.OrderedDict(sorted(coins.items(), key=takeId))


for t in orderedCoins.items():
	coin = t[0]
	print(coins[coin]['format'].format(coin, bsToCoin(bsToUsd, coins[coin]['usdToCoin'], numBs)))
