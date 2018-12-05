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
            return None
        else:
            return self.__analyzeSentimentOfFile(url)

    def __createJsonDocument(self, article):
        articleList = { 'documents' : [] }
        index = 0
        language = 'en'
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        paragraphs = tokenizer.tokenize(article)
        print('tokenizer')
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
            return None
        else:
            return self.__createJsonDocument(article.text)     

#Caller
class analyzeSentimentCaller():
    def __init__(self):
        self.__analyzeSentimentFunction = analyzeSentimentFunctor()
    def analyzeSentiment(self, url):
        return self.__analyzeSentimentFunction(url)