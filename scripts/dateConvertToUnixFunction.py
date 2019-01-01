#!../bin/python3
#Invoke interpreter directly from miniconda env in directory i.e. /home/calvin/python_projects/stockProject

from calendar import isleap
from datetime import datetime
from datetime import timezone

def dateToUnixTime(inputMonth, inputDay, inputYear):
    inputTime = 5 #5:00AM is always constant
    monthDict = {"January":1,"February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}
    dayTuple = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31)
    yearTuple = (2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018)
    #date must be in format "month day year"
    if(inputMonth in monthDict):
        if(int(inputYear) in yearTuple):
            #Check leap year
            if(inputMonth == "January") or (inputMonth=="March") or (inputMonth=="May") or (inputMonth=="July") or (inputMonth=="August") or (inputMonth=="October") or (inputMonth=="December"):
                maxDay = 31
            elif(inputMonth=="April") or (inputMonth=="June") or (inputMonth=="September") or (inputMonth=="November"):
                maxDay = 30
            elif(isleap(inputYear) is False):
                maxDay = 29
            else:
                maxDay = 28 #Leap year for February
            if((1 <= int(inputDay) <= maxDay) and (int(inputDay) in dayTuple)):  #Assuming inputDay is integer
                try:
                    dt = datetime(int(inputYear), monthDict[inputMonth], int(inputDay), inputTime)
                except:
                    print("Could not return unix time equivalent.\n")
                    return None
                else:
                    return str(int(dt.replace(tzinfo=timezone.utc).timestamp()))
            else:
                print("Day is not valid.\n")
                return None
        else:
            print("Year is not valid.\n")
            return None
    else:
        print("Month is not valid.\n")
        return None