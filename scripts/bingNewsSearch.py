# -*- coding: utf-8 -*-

import http.client, urllib.parse, json
import requests

def BingNewsSearch(**kwargs):
    "Performs a Bing News search and returns the results."
    
    # **********************************************
    # *** Update or verify the following values. ***
    # **********************************************

    # Replace the subscriptionKey string value with your valid subscription key.
    subscription_key = "f0a514694efd4c7a9c4a02d9aa42cc61"
    assert subscription_key

    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"

    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params  = {"q": kwargs['search'], "count": kwargs['count'], "safeSearch": kwargs['safeSearch'], "setLang": kwargs['setLanguage']}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    #print(json.dumps(search_results, indent=4))
    return search_results

    ## Verify the endpoint URI.  At this writing, only one endpoint is used for Bing
    ## search APIs.  In the future, regional endpoints may be available.  If you
    ## encounter unexpected authorization errors, double-check this value against
    ## the endpoint for your Bing search instance in your Azure dashboard.
    #host = "api.cognitive.microsoft.com"
    #path = "/bing/v7.0/news/search"    
    #headers = {'Ocp-Apim-Subscription-Key': subscriptionKey, 'BingAPIs-Market' : 'en-US'}

    #conn = http.client.HTTPSConnection(host)

    #searchParam = urllib.parse.quote(kwargs['search'])
    #countParam = urllib.parse.quote(kwargs['count'])
    #safeSearchParam = urllib.parse.quote(kwargs['safeSearch'])
    #setLanguageParam = urllib.parse.quote(kwargs['setLanguage'])

    #conn.request("GET", path + "?q=" + searchParam
    #                         + "&count=" + countParam
    #                         + "&safeSearch=" + safeSearchParam
    #                         + "&setLang=" + setLanguageParam,
    #             headers=headers)
    #response = conn.getresponse()
    #return response.read().decode("utf8")