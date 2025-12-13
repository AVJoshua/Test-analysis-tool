import yfinance as yf
from datetime import datetime

def extractBasicInfo(data):
    keysToExtract = ['longName', 'website','sector', 'fullTimeEmployees', 'marketCap', 'totalRevenue', 'trailingEps']
    basicInfo = {}
    for key in keysToExtract:
        if key in data:
            basicInfo[key] = data[key]
        else:
            basicInfo[key] = ''
    return basicInfo

def getPriceHistory(company):
    historyDf = company.history(period='12mo')
    prices = historyDf['Open'].tolist()
    dates = historyDf.index.strftime('%Y-%m-%d').tolist()
    return {
        'price': prices,
        'date': dates
    }

def getEarningsDates(company):
    earningsDatesDf = company.earnings_dates
    allDates = earningsDatesDf.index.strftime('%Y-%m-%d').tolist()
    dateObjects = [datetime.strptime(date, '%Y-%m-%d') for date in allDates]
    currentDate = datetime.now()
    futureDates = [date.strftime('%Y-%m-%d') for date in dateObjects if date > currentDate]
    return futureDates

def getCompanyNews(company):
    newsList = company.news
    allNewsArticle = []
    for newsDict in newsList:
        newsDictToAdd = {
            'title': newsDict['content']['title'],
            'link': newsDict['content']['thumbnail']
        }
        allNewsArticle.append(newsDictToAdd)
    return allNewsArticle

def getCompanyStockInfo(tickerSymbol):
    #Get data from Yahoo Finance API
    company = yf.Ticker(tickerSymbol)

    # Get basic info on company
    basicInfo = extractBasicInfo(company.info)
    priceHistory = getPriceHistory(company)
    futureEarningsDate = getEarningsDates(company)
    newsArticle = getCompanyNews(company)
    print(priceHistory)

getCompanyStockInfo('MSFT')
