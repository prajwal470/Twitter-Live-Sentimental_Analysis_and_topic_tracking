# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 18:33:52 2022

@author: prajw
"""

import numpy as np
import os
import psycopg2
import re
import tweepy as tw
import pandas as pd
from textblob import TextBlob
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import itertools
import math
import base64
from flask import Flask
import os
import psycopg2
import datetime
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
from sqlalchemy import create_engine
import pymysql
pd.options.mode.chained_assignment = None

#__________________ importing the DATA ________________________________________________________________________________________
all_city = pd.read_csv('Indian Cities Database.csv')  
# Login Api  

access_token='1442663447443824641-oqgZ168qaGw0UzgLYUaG7CZhB38yPn'
access_token_sectet='huisftAuYKeIwMyCNjsUk30ujoVF9sqr5jAx4dYrwfUxo'

api_key="b9mDVgmazrRQjd24VaaYYGZlw"
api_key_secret = "6t4OmoRMV7z62adurCiUzKw71my9IL6KL8ZAUvMOCIHc712cnO"

# auth handler

auth = tw.OAuthHandler(consumer_key=api_key,consumer_secret=api_key_secret)
auth.set_access_token(access_token,access_token_sectet)
api = tw.API(auth,wait_on_rate_limit=True)

# function for cleaning and other extractions

def cleanTxt(text):
    text = re.sub(r'@[A-Za-z0-9]+','',text)
    text = re.sub(r'#', '',text)
    text = re.sub(r'\@w+|\#','',text)
    text = re.sub(r'RT[\s]+', '',text)
    text = re.sub(r'https?:\/\/\S+', '',text)
    text = re.sub('[0-9]+', '', text)
    text = re.sub(r'\n', '', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) \|(\w+:\/\/\S+)", " ", text).split())
    text = text.lower()
    return text

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
    return TextBlob(text).sentiment.polarity

def getAnalysis(score):
    if score < 0:
        return 'Negative' 
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'
def getAnalysis1(score):
    if score < 0:
        return int(-1)
    elif score == 0:
        return int(0)
    else:
        return int(1)

#search for topic

search_words = input('enter here :')

number_of_tweets = 500
#get all tweets
tweets = tw.Cursor(api.search_tweets, 
                           q=search_words,
                           lang="en",
                           ).items(100)
users_locs = [[tweet.user.id,tweet.user.name,tweet.user.screen_name, tweet.text, tweet.user.location , tweet.created_at,tweet.user.followers_count,] for tweet in tweets]
df = pd.DataFrame(data=users_locs,columns=["tweet_id",'user',"screen_name","tweet","location","Created_at","userfollowercount"])

#Cleaning the data
df['tweet'] = df['tweet'].apply(lambda x: cleanTxt(x))
df['user'] = df['user'].apply(lambda x: cleanTxt(x))
df["screen_name"] = df["screen_name"].apply(lambda x: cleanTxt(x))
df["location"] = df["location"].apply(lambda x: cleanTxt(x))
df['Subjectivity'] = df['tweet'].apply(lambda x: getSubjectivity(x))
df['Polarity'] = df['tweet'].apply(lambda x: getPolarity(x))
df['Polarity'] = df['Polarity'].apply(lambda x: getAnalysis1(x))

# creating the engin to store our data
    
engine = create_engine("mysql+pymysql://root:635241@localhost/Twitterdb?charset=utf8mb4")
dbConnection    = engine.connect()
frame = df.to_sql('tweet', dbConnection , if_exists='replace');

#_____________________________ End of importing and storing of DATA_____________________________________________________________________

df1 = pd.read_sql("select * from Twitterdb.tweet", dbConnection);
df1 = pd.DataFrame(df1)    

#df1['Created_at'] = pd.to_datetime(df1['Created_at']).apply(lambda x: x - datetime.timedelta(hours = 5 , minutes=30))
print(df1['Created_at'].head())
min10 = datetime.datetime.now() - datetime.timedelta(hours=16)
min10=min10.strftime('%Y-%m-%d %H:%M:%S') 
min20 = datetime.datetime.now() - datetime.timedelta(hours=16)
min20=min20.strftime('%Y-%m-%d %H:%M:%S')
 #counting the numbersof tweet 
neu_num =(df1['Polarity']==0).sum()
neg_num = (df1['Polarity']==-1).sum()
pos_num = (df1['Polarity']==1).sum()
#Percentage Number of Tweets changed in Last 12 hours
count_now = df[df['Created_at']>min20]["tweet_id"].count()
print(count_now)
count_before = df[ (df['Created_at']<min20)]["tweet_id"].count()
print(count_before)
percent = (count_now-count_before)/count_before*100
print(percent)






