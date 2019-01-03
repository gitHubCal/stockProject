#!../bin/python3
#Invoke interpreter directly from miniconda env in directory i.e. /home/calvin/python_projects/stockProject

import sys
import requests
import socket
import os
import time
import datetime
import matplotlib.pyplot as mPlot
import matplotlib.dates as mDates
import numpy as np
from selenium import webdriver
from stock import Stock
from multiprocessing.dummy import Pool as Threadpool
from functools import partial

def checkConnection():
    print("Checking connection.\n")
    #Create socket connection
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET is ipv4 and SOCK_STREAM is TCP Protocol
        print("Success creating socket connection.\n")
    except: 
        print("Failure to create socket connection.\n")
    
    #Checks if site is down
    port = 80
    try:
        host_ip = socket.gethostbyname('www.finance.yahoo.com')
        print("Success resolving the host.\n")
        s.connect((host_ip,port)) #Use acquired IP to connect
        print("Success connecting to IP: %s on port: %s.\n" %(host_ip,port))
    except:
        print("Error resolving host.\n")
        sys.exit()
    s.close()

def checkWebsiteStatus(url):
    print("Check website status.\n")
    req = requests.get(url)
    if req.status_code == 200:
        print("Request fulfilled.\n")
        return True
    else:
        print("Request failed.\n")
        return False

def readFileLine(line, stockParam):
    print("Reading file line by line into stock object.\n")
    if line != 'Date,Open,High,Low,Close,Adj Close,Volume\n':
        #Note: Stock data does not include weekends or national holidays or days where Stock Market is closed
        stockDataTime = datetime.date(int(line[:4]), int(line[5:7]), int(line[8:10]))
        stockParam.addStockInformation(stockDataTime,
                                  float(line.strip().split(',')[1]),
                                  float(line.strip().split(',')[2]),
                                  float(line.strip().split(',')[3]),
                                  float(line.strip().split(',')[4]),
                                  float(line.strip().split(',')[5]),
                                  float(line.strip().split(',')[6]))

def getStockData(stockName,userStartDateInput,userEndDateInput,listOfStocks):
    #Start date of data (In Unix Timecoding)
    historyPeriod1 = userStartDateInput
    #End date of data (In Unix Timecoding)
    historyPeriod2 = userEndDateInput
    #Get path of where stock data csv file will be (used to determine if file exists; if not, then file will be downloaded to this path).
    stockRead_file_path = ""
    if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
        stockRead_file_path = os.getcwd() + "\Stock-Data\\" + stockName + '.csv'
    else:
        stockRead_file_path = os.getcwd() + "/Stock-Data/" + stockName + '.csv' #For Unix and FreeBSD
    #Obtain file
    if not os.path.exists(stockRead_file_path):
        print("File does not exist. Attempting to download from Yahoo.\n")
        if checkWebsiteStatus('https://finance.yahoo.com') is True:
            #url of website
            url = 'https://finance.yahoo.com/quote/' + stockName + '/history?period1=' + historyPeriod1 + '&period2=' + historyPeriod2 + '&interval=1d&filter=history&frequency=1d'
            try: 
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_experimental_option('prefs', {'download.default_directory' : stockRead_file_path})
                driver = webdriver.Chrome(chrome_options=chrome_options)
                driver.get(url)
                downloadHistoryButton = driver.find_element_by_link_text('Download Data')
                downloadHistoryButton.click()
                #Makes sure download is complete before closing browser
                while not os.path.exists(stockRead_file_path):
                    time.sleep(2)
                driver.quit()
                print("Success. File downloaded.\n")
            except:
                print("Error downloading.\n")
        else:
            print("Error connecting to " + url + "\nCannot download and read crv file.\n")
    else:
        print("File already exists.\n")
    #Check if stock has data associated with it already or if trying to write over the old data, make sure the start and end dates are not the same.
    #No lambda necessary for max and min since "key" will be used for comparison (i.e. datetime.date) and NOT the value.
    if (listOfStocks[stockName] is None) or ((max(listOfStocks[stockName].getTableOfStockData()) != userEndDateInput) and (min(listOfStocks[stockName].getTableOfStockData()) != userStartDateInput)):
        print("Attempting to read file into Stock object.\n")
        #Read from csv file and write output to text file
        try:
            fileToRead = open(stockRead_file_path,'r',encoding='utf-8')
        except IOError:
            print("Error reading and writing files.\n")
        else:
            stock = Stock(stockName)
            #For linux systems
            try:
                #Get number of available cores
                numOfAvailableCore = len(os.sched_getaffinity(0))
            except Exception as e:
                print("Unable to get available number of cores. Using default 2.\n")
                print(e)
                numOfAvailableCore = 2
            pool = Threadpool(numOfAvailableCore)
            updateStockDataInformation = partial(readFileLine,stockParam=stock) #stockParam is fixed, readFileLine has 1 argument
            pool.map(updateStockDataInformation,fileToRead)
            pool.close()
            pool.join()
            fileToRead.close()
            listOfStocks[stockName] = stock   #Updates listOfStocks dictionary with new value for the stockName
            print('Successfully read and wrote crv data into stock object.\n')
    else:
        print("This stock already has data associated with it.")
        
def plotStockData(listOfStocks,stockName):
    print("Ploting anamolies in Stock Data.\n")
    fig = mPlot.figure()
    ax = fig.add_subplot(1,1,1)
    fig.suptitle('Anamolies in Stock Data', fontsize=12, fontweight='bold')

    stockDates = []
    stockOpenPrices = []
    yErrPlotList = []

    anomaliesOpenList = []
    anomaliesDateList = []

    stock_Key = listOfStocks[stockName]

    if stock_Key is not None:
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
        yerr = np.array(yErrPlotList).T
        ax.xaxis.set_major_formatter(mDates.DateFormatter('%m/%d/%Y'))
        fig.autofmt_xdate()
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price', fontsize=12)
        ax.errorbar(stockDates, stockOpenPrices, yerr, fmt='ko', markersize=3, elinewidth=1, capsize=2, ecolor='black', zorder=1, label='Stock High-Open-Low Prices')
        ax.scatter(anomaliesDateList, anomaliesOpenList, marker='^', c='red', s=36, zorder=10, label='Stock Anomalies')
        ax.grid('on')
        ax.set_axisbelow(True)
        ax.legend(loc='upper right')
        mPlot.show()
    else:
        print("There is no data to plot.\n")