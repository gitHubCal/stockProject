#!../bin/python3
#Invoke interpreter directly from miniconda env in directory i.e. /home/calvin/python_projects/stockProject

import requests
import urllib.parse
import json

def newsApiSearch(**kwargs):
    apiKey = 'e5a6b185a6c54901853b70dd4919ef68'
    headers = {'X-Api-Key': apiKey}

    pathType = kwargs['pathType']   #top-headlines, everything, sources
    hostPath = 'https://newsapi.org/v2/' + pathType

    query = kwargs['query']
    oldestDate = kwargs['oldestDate']   #from for real-time-data update date to recent one
    newestDate = kwargs['newestDate']   
    language = kwargs['language']
    sortBy = kwargs['sortBy']
    #sources = kwargs['sources']
    page = kwargs['page']

    queryParam = urllib.parse.quote(query)
    #oldestDateParam = urllib.parse.quote(oldestDate)
    #newestDateParam = urllib.parse.quote(newestDate)
    #languageParam = urllib.parse.quote(language)
    #sortByParam = urllib.parse.quote(sortBy)
    #sourcesParam = urllib.parse.quote(sources)

    url = (hostPath + '?q=' + queryParam + '&language=' + language + '&sortBy=' + sortBy + '&page=' + page + '&from=' + oldestDate + '&to=' + newestDate)  
    response = requests.get(url=url,headers=headers)
    return response