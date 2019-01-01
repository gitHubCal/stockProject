#!../bin/python3
#Invoke interpreter directly from miniconda env in directory i.e. /home/calvin/python_projects/stockProject
#For Linux

from getStockData import getStockData
from getStockData import plotStockData
from autocorrelationGraphFunctions import graphAutocorrelationDataList
from sentimentGraphFunctions import graphAverageSentiment
from dateConvertToUnixFunction import dateToUnixTime

def main():
    #Dictionary of stocks. Each stock (key) has a class of stock data (value) associated with it. Initially empty. 
    #Can have multiple values. 
    listOfStocks = {}

    while True:
        userInputCommand = input("Enter number of function you want to use:\n1)plotStockData\n2)graphAutocorrelationDataList\n3)graphAverageSentiment\n")
        if userInputCommand == "Quit" or userInputCommand == "quit":
            break
        elif userInputCommand == "1" or userInputCommand == "2" or userInputCommand == "3":
            userStockSymbolInput = input("Enter stock symbol: ")
            print("User entered stock symbol: " + userStockSymbolInput + "\n")
            while True:
                #Date Range Parameters (NOTE: Date may vary but time is constant i.e. always 5:00AM)
                #Start date of data (In Unix Timecoding): 1509512400
                #Starts at Wednesday November 1, 2017 5:00 AM
                userMonthStart = input("Enter start date month: ")
                userDayStart = input("Enter start date day: ")
                userYearStart = input("Enter start date year: ")
                userStartDateInput = dateToUnixTime(userMonthStart, userDayStart, userYearStart)
                if userStartDateInput is not None:
                    print("User entered start date: " + userStartDateInput + ".\n")
                    affirmCorrectStartDate = input("Is this correct? Type 'yes' or 'no'.\n")
                    if affirmCorrectStartDate == "yes":
                        break
                    elif affirmCorrectStartDate == "no":
                        print("Enter a new (or same) start date.\n")
                    else:
                        print("Cannot recognize input. Type again.\n")
                else: 
                    print("Please enter valid start date.\n")
            while True:
                #End date of data (In Unix Timecoding): 1510722000
                #Ends at Tuesday November 15, 2017 5:00 AM
                userMonthEnd = input("Enter end date month: ")
                userDayEnd = input("Enter end date day: ")
                userYearEnd = input("Enter end date year: ")
                userEndDateInput = dateToUnixTime(userMonthEnd, userDayEnd, userYearEnd)
                if userEndDateInput is not None:
                    print("User entered start date: " + userEndDateInput + ".\n")
                    affirmCorrectEndDate = input("Is this correct? Type 'yes' or 'no'.\n")
                    if affirmCorrectEndDate == "yes":
                        break
                    elif affirmCorrectEndDate == "no":
                        print("Enter a new (or same) end date.\n")
                    else:
                        print("Cannot recognize input. Type again.\n")
                else: 
                    print("Please enter valid end date.\n")
            #Initialize userInput stock name with value None
            listOfStocks[userStockSymbolInput] = None
            if userInputCommand == "1":
                #Get stock data from Yahoo
                getStockData(userStockSymbolInput,userStartDateInput,userEndDateInput,listOfStocks)
                #userStartDateInput and userEndDateInput shall be passed as str.
                #Plot stock data vs time. 
                plotStockData(listOfStocks,userStockSymbolInput)
            elif userInputCommand == "2":
                #Graph autocorrelation vs time. Does not need listOfStocks dictionary since stock data is not used.
                graphAutocorrelationDataList(userStockSymbolInput,userStartDateInput,userEndDateInput)
            elif userInputCommand == "3":
                #Graph sentiment vs time. Does not need listOfStocks dictionary since stock data is not used.
                graphAverageSentiment(userStockSymbolInput,userStartDateInput,userEndDateInput)
        else:
            print("User input command not recognized. Try again.\n")
  
if __name__== "__main__":
    main()
