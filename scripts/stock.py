#!../bin/python3
#Invoke interpreter directly from miniconda env in directory i.e. /home/calvin/python_projects/stockProject

class Stock:
    def __init__(self, nameOfStock):
        self.__nameOfStock = nameOfStock
        self.__tableOfStockData = {}

    @property
    def getNameOfStock(self):
        return self.__nameOfStock
    @property
    def getTableOfStockData(self):
        return self.__tableOfStockData
    def getDate_Open(self, date):
        return self.__tableOfStockData[date][0]
    def getDate_High(self, date):
        return self.__tableOfStockData[date][1]
    def getDate_Low(self, date):
        return self.__tableOfStockData[date][2]
    def getDate_Close(self, date):
        return self.__tableOfStockData[date][3]
    def getDate_AdjClose(self, date):
        return self.__tableOfStockData[date][4]
    def getDate_Volume(self, date):
        return self.__tableOfStockData[date][5]

    def addStockInformation(self, date, open, high, low, close, adjClose, volume):
        stockDataInformation = [open, high, low, close, adjClose, volume]    
        self.__tableOfStockData.update({date : stockDataInformation})

    def openCloseDifferencePercentage(self, date):
        return ((abs(self.getDate_Open(date) - self.getDate_Close(date)))/self.getDate_Open(date)) * 100

    def highOpenDifference(self, date):
        return abs(self.getDate_High(date) - self.getDate_Open(date))

    def lowOpenDifference(self, date):
        return abs(self.getDate_Low(date) - self.getDate_Open(date))