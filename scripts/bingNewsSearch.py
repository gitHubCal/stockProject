#!../bin/python3
#Invoke interpreter directly from miniconda env in directory i.e. /home/calvin/python_projects/stockProject
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