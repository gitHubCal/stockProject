import requests
import json
import numpy as np
import matplotlib.pyplot as mPlot
import matplotlib.dates as mDates
import matplotlib.patches as mpatches
import datetime
from bingGetSentiment import GetSentiment
from bingNewsSearch import BingNewsSearch
from newsApi import newsApiSearch
from sentimentAnalyzer import analyzeSentimentCaller
from sentimentAnalyzer import analyzeSentimentFunctor

from getStockData import getStockData
#Regular Data
from getStockData import plotData
from data import Data

from time import sleep

import holidays
import dateutil.easter as deaster

from multiprocessing.dummy import Pool as Threadpool
from functools import partial

#Dictionary of stocks (Can change anytime)
listOfStocks = {'AMD': None, 'NVDA': None, 'AMZN': None}

#Call Bing Sentiment analyzer and return list of sentiment values for each body of text in a specific site
def getSentimentList(url):
    analyzeSentimentCall = analyzeSentimentCaller()
    document = analyzeSentimentCall.analyzeSentiment(url)
    if document != "Not valid url." and document is not None:
        print('Please wait a moment for the results to appear.\n')
        try:
            result, conn = GetSentiment(document)
            #conn.close()
        except Exception as e:
            print(e)
            return None
        else:
            try:
                #Might be code 200 error is site is down change in sentimentAnalyzer
                #print(json.dumps(json.loads(result), indent=4))
                #return json.loads(result)['documents']
                print('yes')
                return result['documents']
            except:
                return None
    else:
        print('Not valid url.')
        return None

#Aggregates the given list of sentiment for a specific site
def getAverageSiteSentiment(sentimentList):
    if sentimentList is not None:
        #Calculate average regression

        #Assumes data is accurate
        averageSentiment = 0.0
        for text in sentimentList:
            averageSentiment += text['score'] 
        averageSentiment /= len(sentimentList)
        print('Average sentiment is: %f.' %(averageSentiment))
        return averageSentiment
    else:
        print('No valid data.')
        return None
 
#Call Bing News search and return list of sites corresponding to particular stock and date
def getRelevantNews_bing(search_Param, count_Param, safeSearch_Param, setLanguage_Param):
    print('Searching news for: ', search_Param)
    bingResult = BingNewsSearch(search = search_Param, count = count_Param, safeSearch = safeSearch_Param, setLanguage = setLanguage_Param)
    #newsDataResultsValue = json.loads(bingResult)['value']
    newsDataResultsValue = bingResult['value']
    return newsDataResultsValue

#If Bing News returns nothing use News API
def getRelevantNews_newsAPI(pathType_Param, query_Param, oldestDate_Param, newestDate_Param, language_Param, sortBy_Param, sources_Param, page_Param):
    print('Searching news for: ', query_Param)
    newsApiResult = newsApiSearch(pathType = pathType_Param, query = query_Param, oldestDate = oldestDate_Param, newestDate = newestDate_Param, 
                                  language = language_Param, sortBy = sortBy_Param, sources = sources_Param, page = page_Param)
    newsApiResultsValue = json.loads(newsApiResult)['articles']
    return newsApiResultsValue

#Average sentiment for specific date   
def getAverageSentimentForDay(newsDataResultsValue):
    averageSentimentForDay = None
    numOfAverageSentiment = 0
    for site in newsDataResultsValue:
        averageWebsiteSentiment = getAverageSiteSentiment(getSentimentList(site['url']))
        if averageWebsiteSentiment is not None and averageSentimentForDay is None:
            averageSentimentForDay = 0
            averageSentimentForDay += averageWebsiteSentiment
            numOfAverageSentiment += 1
        elif averageWebsiteSentiment is not None and averageSentimentForDay is not None:
            averageSentimentForDay += averageWebsiteSentiment
            numOfAverageSentiment += 1
        else:
            pass    
    if averageSentimentForDay is not None:
        print('The average sentiment for the day is %f.' %(averageSentimentForDay))
        averageSentimentForDay /= numOfAverageSentiment     
    else:
        print('No valid data for average sentiment that day.')
    return averageSentimentForDay

#Dates Stock Market is not open
def checkStockMarketOpen(stockMarketDate):
    #Calculate Good Friday
    #EASTER_JULIAN   = 1    EASTER_ORTHODOX = 2    EASTER_WESTERN  = 3
    goodFriday = deaster.easter(stockMarketDate.year,3) + datetime.timedelta(days=-2)
    #US Holidays
    us_holidays = holidays.US(years=stockMarketDate.year)
    if stockMarketDate.isoweekday() != '6' and stockMarketDate.isoweekday != '7':   #Make sure not weekend
        if us_holidays.get(stockMarketDate) == 'Columbus Day' or us_holidays.get(stockMarketDate) == 'Veterans Day':  
            return True
        else:
            if stockMarketDate != goodFriday and (stockMarketDate not in us_holidays):  #Already checks for Columbus Day and Veterans Day
            #{datetime.date(2017, 1, 1): "New Year's Day", datetime.date(2017, 1, 2): "New Year's Day (Observed)", datetime.date(2017, 1, 16): 'Martin Luther King, Jr. Day', 
            #datetime.date(2017, 2, 20): "Washington's Birthday", datetime.date(2017, 5, 29): 'Memorial Day', datetime.date(2017, 7, 4): 'Independence Day', 
            #datetime.date(2017, 9, 4): 'Labor Day', datetime.date(2017, 10, 9): 'Columbus Day', datetime.date(2017, 11, 11): 'Veterans Day', 
            #datetime.date(2017, 11, 10): 'Veterans Day (Observed)', datetime.date(2017, 11, 23): 'Thanksgiving', datetime.date(2017, 12, 25): 'Christmas Day'}
                return True       
            else:
                return False
    else:
        return False

#Create list of Trues and Falses corresponding to wether stock market is open or not on particular day
#For formatting graphSentiment graph
def stockMarketCloseDates(listOfDates):
    listOfDateOpen = []
    for date in listOfDates:
        listOfDateOpen.append(checkStockMarketOpen(date))
    return listOfDateOpen

def mapSentiment(searchDate, stockName, x_listOfDates, y_listOfAverageSentiment):
    print('Mapping sentiment.\n')
    #Search Parameters
    #---------------Permanent Querys---------------------------------

    #category = "Business"
    count = "15"
    #market = "en-US"
    safeSearch = "Off"
    setLanguage = "EN"
    dateOfArticle = searchDate.strftime('%b %-d %Y')     #"#" Symbol removes leading zero ONLY for Windows "-" for Linux
    search = stockName + ' "' + dateOfArticle + '"'
    x_listOfDates.append(searchDate)
    if checkStockMarketOpen(searchDate) == True:     
        sentimentDataPoint = getAverageSentimentForDay(getRelevantNews_bing(search, count, safeSearch, setLanguage))
        if sentimentDataPoint is not None:
            y_listOfAverageSentiment.append(sentimentDataPoint)
        else: 
            y_listOfAverageSentiment.append(np.nan)
    else:
        y_listOfAverageSentiment.append(y_listOfAverageSentiment[len(y_listOfAverageSentiment)-1])  #Append previous value. No first date case since first date is always True.  
        
def createSentimentList(stockName):
    print('Creating sentiment list.\n')
    listOfDates = []
    #Date Range Parameters
    #Start date of data (In Unix Timecoding)
    #Starts at Wednesday November 1, 2017 5:00 AM
    startDate = datetime.datetime.fromtimestamp(1509512400)
    #End date of data (In Unix Timecoding)
    #Ends at Tuesday November 15, 2017 5:00 AM
    endDate = datetime.datetime.fromtimestamp(1510722000)
    #Note: Free Cognitive Services is 3 requests every second 
    while startDate <= endDate:
        listOfDates.append(startDate)
        startDate += datetime.timedelta(days=1)

    x_listOfDates = []
    y_listOfAverageSentiment = []
    pool = Threadpool(4)
    dataPoint = partial(mapSentiment, stockName = stockName, x_listOfDates = x_listOfDates, y_listOfAverageSentiment = y_listOfAverageSentiment)
    dataResults = pool.map(dataPoint, listOfDates)
    pool.close()
    pool.join()
    return x_listOfDates, y_listOfAverageSentiment

#Graph Sentiment
def graphSentiment(stockName):
    print('Plotting Sentiment.\n')
    x_listOfDates, y_listOfAverageSentiment = createSentimentList(stockName)
    dateArray_X = np.array(stockMarketCloseDates(x_listOfDates))
    avgSentimentArray_Y = np.array(y_listOfAverageSentiment)
    colorFmt = np.where(dateArray_X == False, 'k', np.where(avgSentimentArray_Y < 0.7, 'b','r'))
    
    fig = mPlot.figure()
    ax = fig.add_subplot(1,1,1)
    ax.scatter(x_listOfDates, y_listOfAverageSentiment, c=colorFmt)
    ax.plot(x_listOfDates, y_listOfAverageSentiment, c='purple')
    ax.set_title('Average sentiment of stock per day', fontsize=12, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Sentiment', fontsize=12)
    ax.xaxis.set_major_formatter(mDates.DateFormatter('%m/%d/%Y'))
    ax.xaxis.set_major_locator(mDates.DayLocator())
    fig.autofmt_xdate(rotation=45)
    ax.grid('on')
    ax.set_axisbelow(True)
    black_patch = mpatches.Patch(color='k', label='Stock Market Closed')
    blue_patch = mpatches.Patch(color='b', label='Average Sentiment < 0.7')
    red_patch = mpatches.Patch(color='r', label='Average Sentiment > 0.7')
    ax.legend(loc='upper right')
    ax.legend(handles=[black_patch,blue_patch,red_patch])
    mPlot.show()   

#Get stock data
getStockData('AMD',listOfStocks)
#plotData(listOfStocks,'AMD')
#Graph sentiment vs time
graphSentiment('AMD')