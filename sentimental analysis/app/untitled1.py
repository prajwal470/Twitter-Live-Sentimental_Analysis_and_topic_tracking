import numpy as np
import os
import psycopg2
import re
import tweepy as tw
import pandas as pd
pd.options.mode.chained_assignment = None
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
import plotly.express as px

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
dbConnection  = engine.connect()
frame = df.to_sql('tweet', dbConnection , if_exists='replace');
engine2 = create_engine("mysql+pymysql://root:635241@localhost/Twitterdb?charset=utf8mb4")
dbConnection2  = engine.connect()
frame = df.to_sql('tweet2', dbConnection2 , if_exists='replace');

df
df['Created_at'] = pd.to_datetime(df['Created_at']).apply(lambda x: x - datetime.timedelta(hours=7))

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


# creating app layout

app.layout = html.Div([
                     html.H2('Twitter Sentiment Analysis for trend and Topic Tracking', style={
        'textAlign': 'center'}),    
                     
        html.Div(id='live-update-graph'),
        
        dcc.Graph(id='bar-chart', figure={}),
        
        dcc.Graph(id='map', figure={}),
                     
        dcc.Interval(
        id='interval-component-slow',
        interval=1*10000, # in milliseconds
        n_intervals=0
    )
    ], style={'padding': '20px'})
         

@app.callback(Output('map', 'figure'),
              [Input('interval-component-slow', 'n_intervals')])
def update_graph_bottom_live(n):
    
    fig = go.Figure(data=go.Choropleth(
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

    fig.update_geos(fitbounds="locations", visible=False)
    
    return fig

@app.callback(Output("bar-chart", 'figure'),
              [Input('interval-component-slow', 'n_intervals')])
def update_bar_live(n):
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
    return fig
              
    
@app.callback(Output('live-update-graph', 'children'),
              [Input('interval-component-slow', 'n_intervals')])
def update_graph_live(n):
    # loading Datafrom mySQl Data base
    
    df1 = pd.read_sql("select * from Twitterdb.tweet", dbConnection);
    df1 = pd.DataFrame(df1) 
    
    
    
    #Convert UTC into PDT
    
    
    
    df1['Created_at'] = pd.to_datetime(df1['Created_at']).apply(lambda x: x - datetime.timedelta(hours = 1))
   # df1['Polarity'] = df1['Polarity'].apply(lambda x: getAnalysis1(x))
    result = df1.groupby([pd.Grouper(key='Created_at', freq='10s'), 'Polarity']).count().unstack(fill_value=0).stack().reset_index()
    result = result.rename(columns={"tweet_id": "Num of '{}' mentions".format(search_words), "Created_at":"Time"})  
    time_series = result["Time"][result['Polarity']==0].reset_index(drop=True)
    
    min10 = datetime.datetime.now() - datetime.timedelta(hours=12, minutes=10)
    #min20 = datetime.datetime.now() - datetime.timedelta(hours=12, minutes=20)
    
    #counting the numbersof tweet 
    neu_num =(df1['Polarity']==0).sum()
    neg_num = (df1['Polarity']==-1).sum()
    pos_num = (df1['Polarity']==1).sum()
    # Percentage Number of Tweets changed in Last 12 hours
    

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
                                    'title':'Last hundred teets',
                                    'annotations':[
                                        dict(
                                            text='{0:.1f}'.format(100),
                                            font=dict(
                                                size=40
                                            ),
                                            showarrow=False
                                        )
                                    ]
                                }

                            }
                        )
                    ], style={'width': '27%', 'display': 'inline-block'})
                ])
               
               ]
                                    
    
    return children 

if __name__ == '__main__':
    app.run_server(debug=False,use_reloader=False)




          