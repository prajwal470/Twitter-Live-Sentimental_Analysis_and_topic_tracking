
"""
Created on Fri Apr 22 19:53:59 2022

@author: prajw
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 16:28:28 2022

@author: prajw
"""

import numpy as np
import re
import tweepy as tw
import pandas as pd
pd.options.mode.chained_assignment = None
import dash
from flask import Flask
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import math
import nltk
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
nltk.download('punkt')
nltk.download('stopwords')

#__________________ importing the DATA ________________________________________________________________________________________

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

search_words = 'ipl'

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
df['Created_at'] = pd.to_datetime(df['Created_at'])




all_city = pd.read_csv('Indian Cities Database.csv')  
    

#cleaning the text and forming dictionary which have city to which the state belongs to
all_city['City'] = all_city['City'].apply(cleanTxt)
all_city['State']= all_city['State'].apply(cleanTxt)
all_city['City']= all_city ['City'].replace({'bengaluru':'bangalore'})
all_city_final = all_city[['City','State']]
STATES = all_city['City']
STATE_DICT=dict(all_city_final.values)   
    
#USER FINAL LOCATION 
user_location = df[['location']] 
    
# some user don't mention location so clearing all spacess
user_location.replace(["",','],np.NaN,inplace = True)
user_location.dropna(inplace = True)                      

# seeing wether the location belongs to any city that we have
l= []
for i in user_location['location']:
    i=i.split(',')
    l.append(i[0])
user_location['location'] = l
user_location_final=user_location[['location']]


# seeing user location to which state it belongs to
is_in_INDIA=[]
    #geo = user_location_final[['location']]
for x in user_location_final['location']:
    check = False
    for s in STATES:
        if s in x:
            is_in_INDIA.append(STATE_DICT[s] if s in STATE_DICT else s)
            check = True
            break
        if not check:
            is_in_INDIA.append(None)
            geo_dist = pd.DataFrame(is_in_INDIA,columns=['State']).dropna().reset_index()


#______ grouping name ______________________________________________________________________________________________________________   
    
geo_dist = geo_dist.groupby('State').count().rename(columns={"index": "Number"}).sort_values(by=['Number'], ascending=False).reset_index()
geo_dist["Log Num"] = geo_dist["Number"].apply(lambda x: math.log(x, 2))
geo_state=geo_dist['State'].tolist() 

#__ as user locaton may be mixed with capital and small case so we converted all text to small but for ge-json we need first letter capital to do that

state_capital=pd.read_csv("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/active_cases_2020-07-17_0800.csv")
state_capital.drop(['active cases'],axis=1,inplace = True)
STATES1= pd.read_csv("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/active_cases_2020-07-17_0800.csv")
STATES1.drop(['active cases'],axis=1,inplace = True)
    
    
#created final state and by creating emty dataframe and added all the state name

STATES1['state']=STATES1['state'].apply(cleanTxt)
state_list=STATES1['state'].tolist()

#____empty data frame to update the new capital value of location

new_state = pd.DataFrame()
    
for x in state_list:
    if x not in geo_state:
        new = {'State':x,'Number':0,'Log Num':0}
        new_state=new_state.append(new,ignore_index=True)
a=new_state.append(geo_dist,ignore_index=True)
a.sort_values(by=['State'], ascending=True,inplace=True)
a.reset_index(inplace=True)
to_add=a.drop(['index'],axis=1)
final_state = pd.concat([to_add, state_capital], axis=1, join='inner')
final_state.drop(['State'],axis=1,inplace = True)

# tokenizing the wold
content = ' '.join(df["tweet"])
content = re.sub(r"http\S+", "", content)
content = content.replace('RT ', ' ').replace('&amp;', 'and')
content = re.sub('[^A-Za-z0-9]+', ' ', content)
content = content.lower()
    
# counting the frequency of the word   
tokenized_word = word_tokenize(content)
stop_words=set(stopwords.words("english"))
filtered_sent=[]
for w in tokenized_word:
    if (w not in stop_words) and (len(w) >= 4):
        filtered_sent.append(w)
fdist = FreqDist(filtered_sent)
fd = pd.DataFrame(fdist.most_common(16), columns = ["Word","Frequency"]).drop([0]).reindex()
fd['Polarity'] = fd['Word'].apply(lambda x: TextBlob(x).sentiment.polarity)
fd['Marker_Color'] = fd['Polarity'].apply(lambda x: 'rgba(255, 50, 50, 0.6)' if x < -0.1 else \
    ('rgba(184, 247, 212, 0.6)' if x > 0.1 else 'rgba(131, 90, 241, 0.6)'))
fd['Line_Color'] = fd['Polarity'].apply(lambda x: 'rgba(255, 50, 50, 1)' if x < -0.1 else \
    ('rgba(184, 247, 212, 1)' if x > 0.1 else 'rgba(131, 90, 241, 1)'))

#_____________________________ End of importing and storing of DATA_____________________________________________________________________


# creating web app using dash

app = dash.Dash(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Real-Time Twitter Monitor'

server = app.server
markdown_text = '''#### This self-motivated independent  project aims to develop a web application for sentimental analysis of a trend or a topic for someone who  likes to know what's happening around and how one's trend or specific topic is doing on the internet. The project is divided into three parts collecting, developing, and deploying.This solution for evaluating Twitter data is to perform better business decisions and keep tracking all relevant Twitter data about a brand in real-time, perform analysis as topics or issues emerge. By monitoring brand mentions on Twitter, brands could inform management and deliver better experiences for their customers across the world'''
markdown_text1 = '''#### Collecting data is a necessary part of this project. I  used Twitter API to collect the data from the server . The Twitter API lets you read and write Twitter data. Thus, you can use it to compose tweets, read profiles, and access your followers’ data and a high volume of tweets on particular subjects in specific locations. API stands for Application Programming Interface. This software provides "middleman services" between two applications that want to communicate with each other. Any requests you make go to the server first and the response given comes through the same route. one can read documents of Twitter [here](https://developer.twitter.com/en/docs/twitter-api) '''
markdown_text2 = '''#### After collecting Data next part is to clean them. Cleaning is necessary to know the sentiment of the tweet and for Visualization. [Ploty](https://plotly.com/graphing-libraries) is an open-source visualization  Python graphing library that makes interactive, publication-quality graphs. GeoJSON is an open standard geospatial data interchange format that represents simple geographic features and their nonspatial attributes. Every country has its own geo Jason file to mark it's border you can find one on internet.Dash is a python framework created by plotly for creating interactive web applications.For making web application I used dash. [Dash](https://dash.plotly.com/introduction) is written on the top of Flask, Plotly.js and React.js. With Dash, you don’t have to learn HTML, CSS and Javascript in order to create interactive dashboards, you only need python. Dash is open source and the application build using this framework are viewed on the web browser. '''
markdown_text3 = '''####  Deploying is the final stage that helps to connect many people. Heroku is a container-based cloud platform as a Service (PaaS). Developers use Heroku to deploy, manage, and scale modern apps. Heroku offers a free plan to help you learn and get started on the platform. '''
markdown_text4 = '''#### Created by :- Prajwal Simha S / Linked in :- [linked in profile](https://www.linkedin.com/in/prajwal-simha-15857b1a2/) / Git hub :- [Git](https://github.com/prajwal470)'''
# creating app layout

app.layout = html.Div([
                     html.H1('Twitter Sentiment Analysis for trend and Topic Tracking', style={
        'textAlign': 'center'}),    
                           
          
        dcc.Markdown(children=markdown_text),
        html.Div(id='live-update-graph'),
        dcc.Markdown(children=markdown_text1),
        dcc.Graph(id='bar-chart', figure={}),
        dcc.Markdown(children=markdown_text2),
        dcc.Graph(id='map', figure={}),
        dcc.Markdown(children=markdown_text3),
        dcc.Markdown(children=markdown_text4),
        dcc.Interval(
        id='interval-component-slow',
        interval=1*10000, # in milliseconds
        n_intervals=0
    )
    ], style={'padding': '20px'})
         

@app.callback(Output('map', 'figure'),
              Output("bar-chart", 'figure'),
              [Input('interval-component-slow', 'n_intervals')])
def update_graph_bottom_live(n):
    
    fig1 = go.Figure(data=go.Choropleth(
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locationmode='geojson-id',
        locations=final_state['state'],
        z=final_state['Number'],
        autocolorscale=False,
        colorscale=["#fdf7ff", "#835af1"],
        marker_line_color="#835af1",
        colorbar_title = "Numbers of Tweet"
        ))

    fig1.update_geos(fitbounds="locations", visible=False)
    
    fig = go.Figure(data=go.Bar(
                                    x=fd["Frequency"].loc[::-1],
                                    y=fd["Word"].loc[::-1], 
                                    name="Neutrals", 
                                    orientation='h',
                                    marker_color=fd['Marker_Color'].loc[::-1].to_list(),
                                    marker=dict(
                                        line=dict(
                                            color=fd['Line_Color'].loc[::-1].to_list(),
                                            width=1)
                                )   
                            )
                            )
    return fig,fig1
              
               
@app.callback(Output('live-update-graph', 'children'),
              [Input('interval-component-slow', 'n_intervals')])
def update_graph_live(n):
    # loading Datafrom mySQl Data base
    
    df1 = df
    
  #Convert UTC into PDT
    
    
    
    df1['Created_at'] = pd.to_datetime(df1['Created_at'])
   # df1['Polarity'] = df1['Polarity'].apply(lambda x: getAnalysis1(x))
    result = df1.groupby([pd.Grouper(key='Created_at', freq='10s'), 'Polarity']).count().unstack(fill_value=0).stack().reset_index()
    result = result.rename(columns={"tweet_id": "Num of '{}' mentions".format(search_words), "Created_at":"Time"})  
    time_series = result["Time"][result['Polarity']==0].reset_index(drop=True)
    
    #min10 = datetime.datetime.now() - datetime.timedelta(hours=12)
    #min20 = datetime.datetime.now() 
    
    #counting the numbersof tweet 
    neu_num =(df1['Polarity']==0).sum()
    neg_num = (df1['Polarity']==-1).sum()
    pos_num = (df1['Polarity']==1).sum()
    
    

    # Create the Graph 
    children = [
               html.Div([
                   html.Div([
                       dcc.Graph(
                           id='crossfilter-indicator-scatter',
                           figure={
                               'data': [
                                   go.Scatter(
                                       x=time_series,
                                       y=result["Num of '{}' mentions".format(search_words)][result['Polarity']==0].reset_index(drop=True),
                                       name="Neutrals",
                                       opacity=0.8,
                                       mode='lines',
                                       line=dict(width=0.5, color='rgb(131, 90, 241)'),
                                       stackgroup='one' 
                                   ),
                                   go.Scatter(
                                        x=time_series,
                                        y=result["Num of '{}' mentions".format(search_words)][result['Polarity']==-1].reset_index(drop=True).apply(lambda x: -x),
                                        name="Negatives",
                                        opacity=0.8,
                                        mode='lines',
                                        line=dict(width=0.5, color='rgb(255, 50, 50)'),
                                        stackgroup='two' 
                                        ),
                                   go.Scatter(
                                        x=time_series,
                                        y=result["Num of '{}' mentions".format(search_words)][result['Polarity']==1].reset_index(drop=True),
                                        name="Positives",
                                        opacity=0.8,
                                        mode='lines',
                                        line=dict(width=0.5, color='rgb(184, 247, 212)'),
                                        stackgroup='three' 
                                    )
                                ]
                            }
                        )
                    ], style={'width': '73%', 'display': 'inline-block', 'padding': '0 0 0 20'}),
                   
                   html.Div([
                        dcc.Graph(
                            id='pie-chart',
                            figure={
                                'data': [
                                    go.Pie(
                                        labels=['Positives', 'Negatives', 'Neutrals'], 
                                        values=[pos_num, neg_num, neu_num],
                                        name="View Metrics",
                                        marker_colors=['rgba(184, 247, 212, 0.6)','rgba(255, 50, 50, 0.6)','rgba(131, 90, 241, 0.6)'],
                                        textinfo='value',
                                        hole=.65)
                                ],
                                'layout':{
                                    'showlegend':False,
                                    'title':'Currently tracking {} brand on Twitter'.format(search_words),
                                    'annotations':[
                                        dict(
                                            text='{0:.1f}'.format(100),
                                            font=dict(
                                                size=20
                                            ),
                                            showarrow=False
                                        )
                                    ]
                                }

                            }
                        )
                    ], style={'width': '27%', 'display': 'inline-block'})
                ]),
    
                
               ]
    
    
    
                                                 
    return children 

if __name__ == '__main__':
    warnings.warn("use 'python -m nltk', not 'python -m nltk.downloader'",         DeprecationWarning)
    app.run_server(debug=True)




          
