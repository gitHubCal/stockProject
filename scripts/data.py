class Data:
    def __init__(self, nameOfStock, date, open, high, low, close, adjClose, volume):
        self.__nameOfStock = nameOfStock
        self.__date = date
        self.__open = open
        self.__high = high
        self.__low = low
        self.__close = close
        self.__adjClose = adjClose
        self.__volume = volume

    @property
    def getNameOfStock(self):
        return self.__nameOfStock

    @property
    def getDate(self):
        return self.__date

    @property
    def getOpen(self):
        return self.__open

    @property
    def getHigh(self):
        return self.__high
    
    @property
    def getLow(self):
        return self.__low

    @property
    def getClose(self):
        return self.__close

    @property
    def getAdjClose(self):
        return self.__adjClose

    @property
    def getVolume(self):
        return self.__volume

    def openCloseDifferencePercentage(self):
        return ((abs(self.__open - self.__close))/self.__open) * 100

    def highOpenDifference(self):
        return abs(self.__high - self.__open)

    def lowOpenDifference(self):
        return abs(self.__low - self.__open)
