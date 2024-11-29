import urllib.request
import json
import datetime as dt

class Securities:
    def __init__(self, ticker):
        self.ticker = ticker
        marketData = self.getMarketData()
        if not marketData:
            self.ticker = None
            return
        self.engine, self.market, self.board = marketData

    def getMarketData(self):
        if not self.ticker:
            return []
        url = f'https://iss.moex.com/iss/securities/{self.ticker}.json'
        response = urllib.request.urlopen(url)
        response = json.loads(response.read().decode('utf-8'))
        if not response['boards']['data']:
            return []
        engineIdx = response['boards']['columns'].index('engine')
        marketIdx = response['boards']['columns'].index('market')
        boardIdx = response['boards']['columns'].index('boardid')
        data = response['boards']['data'][0]
        return data[engineIdx], data[marketIdx], data[boardIdx]

    def getPrice(self, date, atClose=True):
        if not self.ticker:
            return -1
        dateTill = dt.datetime.strptime(date, "%Y-%m-%d")
        dateFrom = dateTill - dt.timedelta(days=5)
        url = f'https://iss.moex.com/iss/engines/{self.engine}/markets/{self.market}/boards/{self.board}/securities/{self.ticker}/candles.json?from={dateFrom.strftime("%Y-%m-%d")}&till={dateTill.strftime("%Y-%m-%d")}&interval=24'
        response = urllib.request.urlopen(url)
        response = json.loads(response.read().decode('utf-8'))['candles']
        data = response['data']
        if not data:
            return -1
        else:
            data = data[len(data) - 1]
        if atClose:
            closeIdx = response['columns'].index('close')
            return data[closeIdx]
        else:
            valueIdx = response['columns'].index('value')
            volumeIdx = response['columns'].index('volume')
            return data[valueIdx] / data[volumeIdx]
