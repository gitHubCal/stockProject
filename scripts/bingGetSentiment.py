# -*- coding: utf-8 -*-

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
    print(sentiment_api_url)

    uri = 'westus.api.cognitive.microsoft.com'
    path = '/text/analytics/v2.0/sentiment'

    headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
    response  = requests.post(sentiment_api_url, headers=headers, json=documents)
    sentiments = response.json()
    #print(json.dumps(sentiments, indent=4))
    #search_term = "Microsoft"
    #"Gets the sentiments for a set of documents and returns the information."

    #headers = {'Content-Type': 'application/json','Ocp-Apim-Subscription-Key': subscription_key}
    conn = http.client.HTTPSConnection(uri)
    #body = json.dumps(documents)
    #conn.request("POST", path, body, headers)
    #response = conn.getresponse()
    #return response.read(), conn
    return sentiments, conn