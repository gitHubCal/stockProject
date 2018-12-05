import sys
import requests
import socket
import os.path
import time
import datetime
import matplotlib.pyplot
import matplotlib.dates
import numpy
from pip import __main__
from selenium import webdriver
from data import Data
from stock import Stock

from multiprocessing.dummy import Pool as Threadpool
from functools import partial

def checkConnection():
    #Create socket connection
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET is ipv4 and SOCK_STREAM is TCP Protocol
        print("Success creating socket connection.")
    except: 
        print("Failure to create socket connection.")
    
    #Checks if site is down
    port = 80
    try:
        host_ip = socket.gethostbyname('www.finance.yahoo.com')
        print("Success resolving the host.")
        s.connect((host_ip,port)) #Use acquired IP to connect
        print("Success connecting to IP: %s on port: %s." %(host_ip,port))
    except:
        print("Error resolving host.")
        sys.exit()
    s.close()

def checkWebsiteStatus(url):
    req = requests.get(url)
    if req.status_code == 200:
        return True
    else:
        return False

def readFileLine(line, stockParam):
    if(line != 'Date,Open,High,Low,Close,Adj Close,Volume\n'):
        lineSplit = line.strip().split(',')
        #Note: Stock data does not include weekends or national holidays or days where Stock Market is closed
        stockDataTime = datetime.date(int(line[:4]), int(line[5:7]), int(line[8:10]))
        #dataPoint = Data('AMD', stockDataTime,
        #                float(line.strip().split(',')[1]),
        #                float(line.strip().split(',')[2]),
        #                float(line.strip().split(',')[3]),
        #                float(line.strip().split(',')[4]),
        #                float(line.strip().split(',')[5]),
        #                float(line.strip().split(',')[6]))
        #listOfStocks[stockName].append(dataPoint)
        stockParam.addStockInformation(stockDataTime,
                                  float(line.strip().split(',')[1]),
                                  float(line.strip().split(',')[2]),
                                  float(line.strip().split(',')[3]),
                                  float(line.strip().split(',')[4]),
                                  float(line.strip().split(',')[5]),
                                  float(line.strip().split(',')[6]))

def getStockData(stockName,listOfStocks):
    #Start date of data (In Unix Timecoding)
    #Starts at Wednesday November 1, 2017 5:00 AM
    historyPeriod1 = '1509512400'
    #End date of data (In Unix Timecoding)
    #Ends at Tuesday November 15, 2017 5:00 AM
    historyPeriod2 = '1510722000'

    if checkWebsiteStatus('https://finance.yahoo.com') is True:
        #url of website
        url = 'https://finance.yahoo.com/quote/' + stockName + '/history?period1=' + historyPeriod1 + '&period2=' + historyPeriod2 + '&interval=1d&filter=history&frequency=1d'
        stockRead_file_path = '/home/calvin/python_projects/stockProject/scripts/Stock-Data/' + stockName + '.csv'
        #Obtain html file
        if not os.path.exists(stockRead_file_path):
            try: 
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_experimental_option('prefs', {'download.default_directory' : '/home/calvin/python_projects/stockProject/scripts/Stock-Data'})
                driver = webdriver.Chrome(chrome_options=chrome_options)
                driver.get(url)
                downloadHistoryButton = driver.find_element_by_link_text('Download Data')
                downloadHistoryButton.click()
                #Makes sure download is complete before closing browser
                while not os.path.exists(stockRead_file_path):
                    time.sleep(2)
                driver.quit()
                print("Success. File downloaded.")
            except:
                print("Error downloading.")
        #Read from csv file and write output to text file
        try:
            fileToRead = open(stockRead_file_path, 'r')
        except IOError:
            print("Error reading and writing files.")
        else:
            stock = Stock(stockName)
            pool = Threadpool(4)
            updateStockDataInformation = partial(readFileLine,stockParam=stock) #stockParam is fixed, readFileLine has 1 argument
            dataPoint = pool.map(updateStockDataInformation,fileToRead)
            pool.close()
            pool.join()
            fileToRead.close()
            listOfStocks[stockName] = stock   #Updates listOfStocks dictionary
            print('Success.')
    else:
        print("Error connecting to " + url)

#Exception for data not downoading and readng

def plotData(listOfStocks,stockName):
    fig = matplotlib.pyplot.figure()
    anomaliesPlot = fig.add_subplot(1,1,1)
    fig.suptitle('Anamolies in Stock Data', fontsize=12, fontweight='bold')

    stockDates = []
    stockOpenPrices = []
    yErrPlotList = []

    anomaliesOpenList = []
    anomaliesDateList = []

    stock_Key = listOfStocks[stockName]

    prevVolume = None
    for key in stock_Key.getTableOfStockData:    #key = date, value = list of stock information
        yErrPlotPoint = (stock_Key.lowOpenDifference(key), stock_Key.highOpenDifference(key))
        yErrPlotList.append(yErrPlotPoint)
        stockDates.append(key)
        stockOpenPrices.append(stock_Key.getDate_Open(key))
        if (stock_Key.openCloseDifferencePercentage(key) > 5) and (prevVolume is not None) and (
            (((abs(stock_Key.getVolume(key) - prevVolume))/(stock_Key.getVolume(key)))*100) > 50):
            anomaliesOpenList.append(stock_Key.getDate_Open(key))
            anomaliesDateList.append(key)
        prevVolume = stock_Key.getDate_Volume(key)

    yerr = numpy.array(yErrPlotList).T

    anomaliesPlot.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d/%Y'))
    fig.autofmt_xdate()
    #anomaliesPlot.xaxis.set_major_locator(matplotlib.dates.WeekdayLocator())
    anomaliesPlot.set_xlabel('Date', fontsize=12)
    anomaliesPlot.set_ylabel('Price', fontsize=12)
    anomaliesPlot.errorbar(stockDates, stockOpenPrices, yerr, fmt='ko', markersize=3, elinewidth=1, capsize=2, ecolor='black', zorder=1, label='Stock High-Open-Low Prices')
    anomaliesPlot.scatter(anomaliesDateList, anomaliesOpenList, marker='^', c='red', s=36, zorder=10, label='Stock Anomalies')
    anomaliesPlot.grid('on')
    anomaliesPlot.set_axisbelow(True)
    anomaliesPlot.legend(loc='upper right')
    matplotlib.pyplot.show()

def main():
    print("Hello World\n")

if __main__ == "__main__": 
    sys.exit(int(main() or 0))

