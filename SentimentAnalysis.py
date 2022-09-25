#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 14:18:10 2022

@author: w
"""
pip install textblob
pip install tweepy
pip install pycountry
pip install wordcloud
pip install langdetect

import pandas as pd
from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
import pycountry
import re
import string

from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer

import nltk
nltk.download('vader_lexicon')

df = pd.read_csv('scraped_tweets.csv')
df.head()

# Creating a word cloud for scraped tweets
stopwords = set(STOPWORDS)
stopwords.update(["br", "href"])
textt = " ".join(review for review in df.text)
wordcloud = WordCloud(stopwords=stopwords).generate(textt)

plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis("off")
plt.savefig('wordcloud11.png')
plt.show()

# Twitter API info not included in the code for privacy reasons
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


# Sentiment Analysis

# for calculating sentiment makeups 
def percentage(part,whole):
    return 100 * float(part)/float(whole)

# user inputs 
keyword = input("Please enter keyword or hashtag to search: ")
noOfTweet = int(input ("Please enter how many tweets to analyze: "))

# sentiment counters 
tweets = tweepy.Cursor(api.search_tweets, q=keyword).items(noOfTweet)
positive = 0
negative = 0
neutral = 0
polarity = 0
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []


for tweet in tweets:
    #print(tweet.text)
    tweet_list.append(tweet.text)
    #tweet_list.drop_duplicates(inplace = True)
    analysis = TextBlob(tweet.text)
    score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    compound = score['compound']
    polarity += analysis.sentiment.polarity
    
    if neg > pos:
        negative_list.append(tweet.text)
        negative += 1
    elif pos > neg:
        positive_list.append(tweet.text)
        positive += 1
    elif pos == neg:
        neutral_list.append(tweet.text)
        neutral += 1

positive = percentage(positive, noOfTweet)
negative = percentage(negative, noOfTweet)
neutral = percentage(neutral, noOfTweet)
polarity = percentage(polarity, noOfTweet)
positive = format(positive, '.1f')
negative = format(negative, '.1f')
neutral = format(neutral, '.1f')


# Number of Tweets (Total, Positive, Negative, Neutral)

# sentiment counts
tweet_list = pd.DataFrame(tweet_list)
neutral_list = pd.DataFrame(neutral_list)
negative_list = pd.DataFrame(negative_list)
positive_list = pd.DataFrame(positive_list)
print("total number of tweets: ",len(tweet_list))
print("positive tweet counts: ",len(positive_list))
print("negative tweet counts: ", len(negative_list))
print("neutral tweet counts: ",len(neutral_list))

# percentage makeup of sentiments 
neu = len(neutral_list)/len(tweet_list)*100
neg = len(negative_list)/len(tweet_list)*100
pos = len(positive_list)/len(tweet_list)*100
print("% of positive tweets: " + str(pos) + "%")
print("% of negative tweets: " + str(neg) + "%")
print("% of neutral tweets: " + str(neu) + "%")