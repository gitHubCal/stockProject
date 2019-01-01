#!../bin/python3
#Invoke interpreter directly from miniconda env in directory i.e. /home/calvin/python_projects/stockProject

import json
from bingGetSentiment import GetSentiment
from bingNewsSearch import BingNewsSearch
from newsApiSearch import newsApiSearch
from sentimentAnalyzer import analyzeSentimentCaller
from sentimentAnalyzer import analyzeSentimentFunctor

#Call Bing Sentiment analyzer and return list of sentiment values for each body of text in a specific site.
def getSentimentList(url):
    print('Structuring json document for request to call Bing Sentiment analyzer to return list of sentiment values for news article.')
    #url is guranteed to exist since this function will not be called if url does not exist.
    analyzeSentimentCall = analyzeSentimentCaller()
    document = analyzeSentimentCall.analyzeSentiment(url)
    if (document is not None) and (len(document) > 0):
        print('Please wait a moment for the results to appear.\n')
        try:
            result = GetSentiment(document)
        except Exception as e:
            print(e)
            return None
        else:
            try:
                #Might be code 200 error if site is down change in sentimentAnalyzer
                return result['documents']
            except:
                print('Could not return sentiment analysis results for json document.\n')
                return None
    else:
        print('Json document could not be produced.\n')
        return None

#Append list of sentiment scores from a website into a vector.
def generateSentimentScoreVector(siteSentimentScoreList):
    print("Creating list of sentiment scores for this news article.\n")
    if (siteSentimentScoreList is not None) and (len(siteSentimentScoreList) > 0):
        sentimentScoreVector = []
        for text in siteSentimentScoreList: 
            sentimentScoreVector.append(text['score'])
        return sentimentScoreVector
    else:
        print('No valid data.\n')
        return None
 
#Call Bing News search and return list of sites corresponding to particular stock and date.
def getRelevantNews_bing(search_Param, count_Param, safeSearch_Param, setLanguage_Param):
    print('Searching news for: ', search_Param)
    bingResult = BingNewsSearch(search = search_Param, count = count_Param, safeSearch = safeSearch_Param, setLanguage = setLanguage_Param)
    newsDataResultsValue = bingResult['value']
    for data in newsDataResultsValue:
        print('Results of Bing news search are: ' + str(data) + '\n')
    return newsDataResultsValue

#If Bing News returns nothing use News API.
def getRelevantNews_newsAPI(pathType_Param, query_Param, oldestDate_Param, newestDate_Param, language_Param, sortBy_Param, sources_Param, page_Param):
    print('Searching news for: ', query_Param)
    newsApiResult = newsApiSearch(pathType = pathType_Param, query = query_Param, oldestDate = oldestDate_Param, newestDate = newestDate_Param, 
                                  language = language_Param, sortBy = sortBy_Param, sources = sources_Param, page = page_Param)
    newsApiResultsValue = json.loads(newsApiResult)['articles']
    for data in newsApiResultsValue:
        print('Results of API news search are: ' + str(data) + '\n')
    return newsApiResultsValue