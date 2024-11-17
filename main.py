import urllib.request
import json

def makeDate(year, month, day):
    return str(year) + "-" + str(month) + "-" + str(day)

def makeNumbers(date):
    return [int(i) for i in date.split('-')]

def nDaysAgo(n, date):
    try:
        year, month, day = makeNumbers(date)
    except:
        raise ValueError(f"Incorrect date (YYYY-MM-DD): {date}")
    n = 7
    if day > n:
        day -= n
    elif month > 1:
        month -= 1
        day += 28 - n
    else:
        year -= 1
        month += 12 - 1
        day += 28 - n
    return makeDate(year, month, day)

class Securities:
    def __init__(self, ticker):
        self.ticker = ticker
        marketData = self.getMarketData()
        if not marketData:
            self.ticker = None
            self.engine, self.market, self.board = None, None, None
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

    def getPrice(self, date):
        if not self.ticker:
            return -1
        dateTill = date
        dateFrom = nDaysAgo(7, date)
        url = f'https://iss.moex.com/iss/engines/{self.engine}/markets/{self.market}/boards/{self.board}/securities/{self.ticker}/candles.json?from={dateFrom}&till={dateTill}&interval=24'
        response = urllib.request.urlopen(url)
        response = json.loads(response.read().decode('utf-8'))['candles']
        data = response['data']
        if not data:
            return -1
        else:
            data = data[len(data) - 1]
        closeIdx = response['columns'].index('close')
        return data[closeIdx]
        # valueIdx = response['columns'].index('value')
        # volumeIdx = response['columns'].index('volume')
        # return data[valueIdx] / data[volumeIdx]

sec = Securities("Incorrect")
sber = Securities("SBER")
print(sec, sber, None)
