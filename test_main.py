import main
import pytest

dates = ["2024-11-14", "2024-11-10", "6666-06-06", "1111-11-11", "2022-03-23", "2022-03-24"]
prices = {
    "IMOEX" : [2697.47, 2734.56, -1, -1, -1, 2578.51],
    "SBER" : [249.52, 255.98, -1, -1, -1, 136.24],
    "LQDT" : [1.5224, 1.5185, -1, -1, -1, -1]#,
    # "MyIncorrectTicket" : [-1, -1, -1, -1, -1, -1]
}

securities = {
    ticker : main.Securities(ticker)
    for ticker in prices.keys()
}

@pytest.mark.parametrize("ticker, date", [
    (ticker, date)
    for date in dates
    for ticker in prices.keys()
])
def test_tickers(ticker, date):
    idx = dates.index(date)
    assert securities[ticker].getPriceDate(dates[idx]) == prices[ticker][idx]
