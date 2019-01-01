#!../bin/python3
#Invoke interpreter directly from miniconda env in directory i.e. /home/calvin/python_projects/stockProject

import holidays
import datetime
import dateutil.easter as deaster

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