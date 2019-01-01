#!../bin/python3
#Invoke interpreter directly from miniconda env in directory i.e. /home/calvin/python_projects/stockProject

import datetime
import os
import numpy as np
import matplotlib.pyplot as mPlot
import matplotlib.dates as mDates
from multiprocessing.dummy import Pool as Threadpool
from functools import partial
from stockMarketOpenDateCheck import checkStockMarketOpen
from bingNewsAndSentimentRequestFunctions import getRelevantNews_bing
from bingNewsAndSentimentRequestFunctions import generateSentimentScoreVector
from bingNewsAndSentimentRequestFunctions import getSentimentList
from correlationFunctions import calculateAutocorrelationMatrix

#Calculate Pearson correlation coefficient between sentiments from each website
def getPearsonCorrelationCoefficient(newsDataResultsValue):
    print("Calculating Pearson Correlation Coefficient.\n")
    #newsDataResultsValue is guranteed to exist and have at least 1 news site url since this function would not be called if it did not.
    listOfSentimentScoreVector = []
    for site in newsDataResultsValue:
        sentimentScoreVector = generateSentimentScoreVector(getSentimentList(site['url']))
        if (sentimentScoreVector is not None) and (len(sentimentScoreVector) > 0):
            listOfSentimentScoreVector.append(np.array(sentimentScoreVector))
        else:
            print("No sentiment score array generated for this url.\n")
    if len(listOfSentimentScoreVector) == 0:
        print("No sentiment score arrays can be generated for any of the news urls.\n")
        return None
    else:
        lengthOfLargestSentimentScoreVector = max(listOfSentimentScoreVector,key=len).size
        for index, scoreVector in enumerate(listOfSentimentScoreVector):
            if(scoreVector.size != lengthOfLargestSentimentScoreVector):
                numOfZeroes = lengthOfLargestSentimentScoreVector-scoreVector.size
                new_scoreVector = np.pad(scoreVector,(0,numOfZeroes),'constant')
                #replace old vector with new vector
                listOfSentimentScoreVector[index] = new_scoreVector - np.mean(new_scoreVector)
        print('The data in listOfSentimentScoreVector is:\n')
        print(listOfSentimentScoreVector)
        return listOfSentimentScoreVector

#Calculate how similar the coefficient scores are between each other.
def getAutocorrelationOfDay(newsDataResultsValue):
    print("Calculating autocorrelation value for this day.\n")
    if (newsDataResultsValue is not None) and (len(newsDataResultsValue) > 0):
        autocorrelationValueList = calculateAutocorrelationMatrix(getPearsonCorrelationCoefficient(newsDataResultsValue))
        if (autocorrelationValueList is not None) and (len(autocorrelationValueList) > 0):
            print("Returning average correlation for the day.\n")
            return np.mean(autocorrelationValueList,dtype=np.float64)
        else: 
            print("No average autocorrelation can be calculated for this day.\n")
            return None
    else:
        print("No average autocorrelation can be calculated for this day since there are no news sites returned for this date.\n")
        return None

def mapAutoCorrelation(searchDate, stockName, x_listOfDates, y_listOfAutocorrelationData):
    print('Mapping autocorrelation.\n')
    #Search Parameters
    #---------------Permanent Querys---------------------------------
    #category = "Business"
    count = "15"
    #market = "en-US"
    safeSearch = "Off"
    setLanguage = "EN"
    dateOfArticle = searchDate.strftime('%b %-d %Y')     #"#" Symbol removes leading zero ONLY for Windows "-" for Linux
    search = stockName + ' "' + dateOfArticle + '"'
    x_listOfDates.append(searchDate)    #Get every search date regardless of wether stock market is open that date.
    if checkStockMarketOpen(searchDate) is True:     
        autocorrelationDataPoint = getAutocorrelationOfDay(getRelevantNews_bing(search, count, safeSearch, setLanguage))
        if autocorrelationDataPoint is not None:
            print("Average autocorrelation sucessfully calculated for this day.\n")
            y_listOfAutocorrelationData.append(autocorrelationDataPoint)
        else: 
            print("No average autocorrelation can be calculated for this day.\n")
            y_listOfAutocorrelationData.append(0)
    else:
        #Append previous value if stock market is not open. No first date case since first date is always True (did check in createAutocorrelationDataList).
        y_listOfAutocorrelationData.append(y_listOfAutocorrelationData[len(y_listOfAutocorrelationData)-1])
        
def createAutocorrelationDataList(stockName,userStartDateInput,userEndDateInput):
    print('Creating autocorrelation data list.\n')
    listOfDates = []
    #Start date of data (In Unix Timecoding)
    startDate = datetime.datetime.fromtimestamp(int(userStartDateInput))
    #End date of data (In Unix Timecoding)
    endDate = datetime.datetime.fromtimestamp(int(userEndDateInput))
    #Note: Free Cognitive Services is 3 requests every second 
    while startDate <= endDate:
        #Checks first date case.
        if (startDate == datetime.datetime.fromtimestamp(int(userStartDateInput))) and (checkStockMarketOpen(startDate) is False):
            pass
            #Do not append if for the first date, the stock market is not open.
        else:    
            listOfDates.append(startDate)
        startDate += datetime.timedelta(days=1)

    x_listOfDates = []
    y_listOfAutocorrelationData = []
    #For linux systems
    try:
        #Get number of available cores
        numOfAvailableCore = len(os.sched_getaffinity(0))
    except Exception as e:
        print("Unable to get available number of cores. Using default 2.\n")
        print(e)
        numOfAvailableCore = 2
    pool = Threadpool(numOfAvailableCore)
    dataPoint = partial(mapAutoCorrelation, stockName = stockName, x_listOfDates = x_listOfDates, y_listOfAutocorrelationData = y_listOfAutocorrelationData)
    pool.map(dataPoint, listOfDates)
    pool.close()
    pool.join()
    return x_listOfDates, y_listOfAutocorrelationData

#Graph autocorrelation
def graphAutocorrelationDataList(stockName,userStartDateInput,userEndDateInput):
    print('Plotting autocorrelation data.\n')
    x_listOfDates, y_listOfAutocorrelationData = createAutocorrelationDataList(stockName,userStartDateInput,userEndDateInput)
    if (x_listOfDates is None) or (len(x_listOfDates) < 0) or (y_listOfAutocorrelationData is None) or (len(y_listOfAutocorrelationData) < 0):
        print("Not valid data to plot.\n")
    else:
        fig = mPlot.figure()
        ax = fig.add_subplot(1,1,1)
        ax.scatter(x_listOfDates, y_listOfAutocorrelationData)
        ax.plot(x_listOfDates, y_listOfAutocorrelationData)
        ax.set_title('Average Autocorrelation between news articles per day.', fontsize=12, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Autocorrelation', fontsize=12)
        ax.xaxis.set_major_formatter(mDates.DateFormatter('%m/%d/%Y'))
        ax.xaxis.set_major_locator(mDates.DayLocator())
        fig.autofmt_xdate(rotation=45)
        ax.grid(True)
        ax.set_axisbelow(True)
        mPlot.show()