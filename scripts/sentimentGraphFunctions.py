#!../bin/python3
#Invoke interpreter directly from miniconda env in directory i.e. /home/calvin/python_projects/stockProject

import datetime
import os
import numpy as np
import matplotlib.pyplot as mPlot
import matplotlib.dates as mDates
import matplotlib.patches as mPatches
from multiprocessing.dummy import Pool as Threadpool
from functools import partial

from stockMarketOpenDateCheck import checkStockMarketOpen
from stockMarketOpenDateCheck import stockMarketCloseDates
from bingNewsAndSentimentRequestFunctions import getSentimentList
from bingNewsAndSentimentRequestFunctions import getRelevantNews_bing

#Aggregates the given list of sentiment for a specific site
def getAverageSiteSentiment(sentimentScoreVector):
    print('Calculating average sentiment for news article.\n')
    if (sentimentScoreVector is not None) and (len(sentimentScoreVector) > 0):
        #Assumes data is accurate
        averageSentiment = 0.0
        for text in sentimentScoreVector:
            print('The score is ' + str(text['score']))
            averageSentiment += text['score'] 
        averageSentiment /= len(sentimentScoreVector)
        print('Average sentiment is: %f.' %(averageSentiment))
        return averageSentiment
    else:
        print('No valid sentiment data.\n')
        return None

#Average sentiment for specific date   
def getAverageSentimentForDay(newsDataResultsValue):
    print('Calculating average sentiment for given day based on the average sentiment for each news article found for that day.\n')
    averageSentimentForDay = None
    numOfAverageSentiment = 0
    #If the returned list is None or the length of the list of articles is 0, do nothing.
    if (newsDataResultsValue is None) or (len(newsDataResultsValue) < 0):
        print("No news sites found for this day.\n")
        return None
    else:
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
            averageSentimentForDay /= numOfAverageSentiment     
        else:
            print('No valid data for average sentiment this day.\n')
        return averageSentimentForDay

def mapAverageSentiment(searchDate, stockName, x_listOfDates, y_listOfAverageSentiment):
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
    if checkStockMarketOpen(searchDate) is True:     
        sentimentDataPoint = getAverageSentimentForDay(getRelevantNews_bing(search, count, safeSearch, setLanguage))
        if sentimentDataPoint is not None:
            print("Average sentiment sucessfully calculated for this day.\n")
            y_listOfAverageSentiment.append(sentimentDataPoint)
        else: 
            print("No average sentiment can be calculated for this day.\n")
            y_listOfAverageSentiment.append(0)
    else:
        y_listOfAverageSentiment.append(y_listOfAverageSentiment[len(y_listOfAverageSentiment)-1])  #Append previous value. No first date case since first date is always True.  
        
def createAverageSentimentList(stockName,userStartDateInput,userEndDateInput):
    print('Creating sentiment list.\n')
    listOfDates = []
    #Start date of data (In Unix Timecoding)
    startDate = datetime.datetime.fromtimestamp(int(userStartDateInput))
    #End date of data (In Unix Timecoding)
    endDate = datetime.datetime.fromtimestamp(int(userEndDateInput))
    #Note: Free Cognitive Services is 3 requests every second 
    while startDate <= endDate:
        #Checks first date case.
        if startDate == datetime.datetime.fromtimestamp(int(userStartDateInput)) and (checkStockMarketOpen(startDate) is False):
            pass
            #Do not append if for the first date, the stock market is not open.
        else:    
            listOfDates.append(startDate)
        startDate += datetime.timedelta(days=1)

    x_listOfDates = []
    y_listOfAverageSentiment = []
    #For linux systems
    try:
        #Get number of available cores
        numOfAvailableCore = len(os.sched_getaffinity(0))
    except Exception as e:
        print("Unable to get available number of cores. Using default 2.\n")
        print(e)
        numOfAvailableCore = 2
    pool = Threadpool(numOfAvailableCore)
    dataPoint = partial(mapAverageSentiment, stockName = stockName, x_listOfDates = x_listOfDates, y_listOfAverageSentiment = y_listOfAverageSentiment)
    pool.map(dataPoint, listOfDates)
    pool.close()
    pool.join()
    return x_listOfDates, y_listOfAverageSentiment

#Graph Sentiment
def graphAverageSentiment(stockName,userStartDateInput,userEndDateInput):
    print('Plotting Sentiment.\n')
    x_listOfDates, y_listOfAverageSentiment = createAverageSentimentList(stockName,userStartDateInput,userEndDateInput)
    if (x_listOfDates is None) or (len(x_listOfDates) < 0) or (y_listOfAverageSentiment is None) or (len(y_listOfAverageSentiment) < 0):
        print('No valid data to plot.\n')
    else:
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
        ax.grid(True)
        ax.set_axisbelow(True)
        black_patch = mPatches.Patch(color='k', label='Stock Market Closed')
        blue_patch = mPatches.Patch(color='b', label='Average Sentiment < 0.7')
        red_patch = mPatches.Patch(color='r', label='Average Sentiment > 0.7')
        ax.legend(loc='upper right')
        ax.legend(handles=[black_patch,blue_patch,red_patch])
        mPlot.show()   