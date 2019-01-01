#!../bin/python3
#Invoke interpreter directly from miniconda env in directory i.e. /home/calvin/python_projects/stockProject

#import requests
#import lxml.html
#from lxml.cssselect import CSSSelector
#from bs4 import BeautifulSoup
import json
from newspaper import Article
#import nltk.data
import nltk

#Functor
class analyzeSentimentFunctor:
    def __call__(self, url=None):
        if url is None:
            print("analyzeSentimentFunctor: No url given.\n")
            return None
        else:
            return self.__analyzeSentimentOfFile(url)

    #If this function is called. It is guranteed to have valid a url to tokenize and the article is sucessfully downloaded and parsed.
    def __createJsonDocument(self, article):
        print("analyzeSentimentFunctor: Creating and structring json document from tokenized news article.\n")
        articleList = { 'documents' : [] }
        index = 0
        language = 'en'
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        paragraphs = tokenizer.tokenize(article)
        #Take out unrelated text
        for sentence in paragraphs:
            articleList['documents'].append({ 'id' : index,
                                          'language' : language,
                                          'text' : sentence})
            index += 1
        return articleList
    
    def __analyzeSentimentOfFile(self, url):
        try:
            article = Article(url)
            article.download()
            article.parse()   
        except:
            print("analyzeSentimentFunctor: Could not parse article.\n")
            return None
        else:
            return self.__createJsonDocument(article.text)     

#Caller
class analyzeSentimentCaller():
    def __init__(self):
        self.__analyzeSentimentFunction = analyzeSentimentFunctor()
    def analyzeSentiment(self, url):
        return self.__analyzeSentimentFunction(url)