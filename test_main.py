import main
import pytest

dates = ["2024-11-14", "2024-11-10", "6666-66-66"]
prices = {
    "IMOEX" : [2697.47, 2734.56, -1],
    "SBER" : [249.52, 255.98, -1],
    "LQDT" : [1.5224, 1.5185, -1]
}

securities = {
    ticker : main.Securities(ticker)
    for ticker in prices.keys()
}

@pytest.mark.parametrize("ticker, date", [
    (ticker, date) 
    for ticker in prices.keys()
    for date in dates
])
def test_tickers(ticker, date):
    idx = dates.index(date)
    assert securities[ticker].getPriceDate(dates[idx]) == prices[ticker][idx]
