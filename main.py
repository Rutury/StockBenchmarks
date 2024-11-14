import urllib.request
import json

class Securities:
    def __init__(self, ticker):
        self.ticker = ticker
        self.engine, self.market, self.board = self.getMarketData()

    def getMarketData(self):
        url = f'https://iss.moex.com/iss/securities/{self.ticker}.json'
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        if not data['boards']['data']:
            return []
        engineIdx = data['boards']['columns'].index('engine')
        marketIdx = data['boards']['columns'].index('market')
        boardIdx = data['boards']['columns'].index('boardid')
        return data['boards']['data'][0][engineIdx], data['boards']['data'][0][marketIdx], data['boards']['data'][0][boardIdx]

    def getCandles(self, dateFrom, dateTill=-1, interval=24):
        if dateTill == -1:
            dateTill = dateFrom
        url = f'https://iss.moex.com/iss/engines/{self.engine}/markets/{self.market}/boards/{self.board}/securities/{self.ticker}/candles.json?from={dateFrom}&till={dateTill}&interval={interval}'
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        #candles = [[ticker, dateFrom, interval] + i[:4] for i in data['candles']['data']]
        candles = [i[:4] for i in data['candles']['data']]
        return candles

mySec = Securities("MOEX")
print(mySec.getCandles("2024-11-13"))
