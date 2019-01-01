# -*- coding: utf-8 -*-
#!../bin/python3
#Invoke interpreter directly from miniconda env in directory i.e. /home/calvin/python_projects/stockProject

import requests
import json
import http

def GetSentiment(documents):

    # **********************************************
    # *** Update or verify the following values. ***
    # **********************************************

    subscription_key = 'eaffadf9d9464fe6ba0161aa0c2bda8a'
    assert subscription_key

    text_analytics_base_url = "https://eastus.api.cognitive.microsoft.com/text/analytics/v2.0/"
    sentiment_api_url = text_analytics_base_url + "sentiment"

    headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
    response  = requests.post(sentiment_api_url, headers=headers, json=documents)
    sentiments = response.json()
    #print(json.dumps(sentiments, indent=4))
    return sentiments