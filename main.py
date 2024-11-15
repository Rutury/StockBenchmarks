import urllib.request
import json

def makeDate(year, month, day):
    return str(year) + "-" + str(month) + "-" + str(day)

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
        dataData = data['boards']['data'][0]
        return dataData[engineIdx], dataData[marketIdx], dataData[boardIdx]

    def getCandle(self, year, month, day):
        dateTill = makeDate(year, month, day)
        step = 7
        if day > step:
            day -= step
        elif month > 1:
            month -= 1
            day += 28 - step
        else:
            year -= 1
            month += 12 - 1
            day += 28 - step
        dateFrom = makeDate(year, month, day)
        url = f'https://iss.moex.com/iss/engines/{self.engine}/markets/{self.market}/boards/{self.board}/securities/{self.ticker}/candles.json?from={dateFrom}&till={dateTill}&interval=24'
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        #candles = [[ticker, dateFrom, interval] + i[:4] for i in data['candles']['data']]
        candles = [i[:4] for i in data['candles']['data']]
        return candles[len(candles)-1:]
