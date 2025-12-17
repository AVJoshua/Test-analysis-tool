import yfinance as yf
import requests
from datetime import datetime
from bs4 import BeautifulSoup

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
            'link': newsDict['content']['canonicalUrl']
        }
        allNewsArticle.append(newsDictToAdd)
    return allNewsArticle

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0'
}

def extractCompanyNewsArticles(newsArticle):
    for newsArticle in newsArticle:
        url = newsArticle['link']['url']
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")

        if soup.find_all(string='Continue Reading'):
            print("Tag Found - should skip")
        else:
            print("Tag not found, don't skip")

def getCompanyStockInfo(tickerSymbol):
    #Get data from Yahoo Finance API
    company = yf.Ticker(tickerSymbol)

    # Get basic info on company
    basicInfo = extractBasicInfo(company.info)
    priceHistory = getPriceHistory(company)
    futureEarningsDate = getEarningsDates(company)
    newsArticle = getCompanyNews(company)
    extractCompanyNewsArticles(newsArticle)
    # print(newsArticle)

getCompanyStockInfo('MSFT')
