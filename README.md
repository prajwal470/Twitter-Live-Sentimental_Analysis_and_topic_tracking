# Twitter-Live-Sentimental_Analysisi_and_topic_tracking.
### Hi there 👋,
![20220424_014447](https://user-images.githubusercontent.com/68987382/164944757-f8c87551-1987-4526-8fdf-75f0efd03ff1.gif)

# Inspiration.

### This self-motivated independent  project aims to develop a web application for sentimental analysis of a trend or a topic for someone who  likes to know what's happening around and how one's trend or specific topic is doing on the internet. The project is divided into three parts collecting, developing, and deploying.This solution for evaluating Twitter data is to perform better business decisions and keep tracking all relevant Twitter data about a brand in real-time, perform analysis as topics or issues emerge. By monitoring brand mentions on Twitter, brands could inform management and deliver better experiences for their customers across the word.

# Abstract View
  
 ## This project consist of three parts collecting data , transforming Data , deploying.
  
  ![](https://github.com/prajwal470/Twitter-Live-Sentimental_Analysis_and_topic_tracking/blob/0c585506bb285a74a9b13a18d8d62c1207c93688/Untitled%20Diagram.drawio.png)
 
 # Collecting Data.

### Collecting data is a necessary part of this project. I  used Twitter API to collect the data from the server . The Twitter API lets you read and write Twitter data. Thus, you can use it to compose tweets, read profiles, and access your followers’ data and a high volume of tweets on particular subjects in specific locations. API stands for Application Programming Interface. This software provides "middleman services" between two applications that want to communicate with each other. Any requests you make go to the server first and the response given comes through the same route. one can read documents of Twitter [here](https://developer.twitter.com/en/docs/twitter-api).

## Twitter API.

### To get work with api we need some way to connect to the server to connect Go to http://apps.twitter.com and create an app hear consumer key and secret will be generated for you.
  ```
  
  API_KEY = "XXXXXXXXXXXXXX"
  API_SECRET_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  After the step above, you will be redirected to your app's page.
  Create an access token under the the "Your access token" section
  ACCESS_TOEKN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  ACCESS_TOKEN_SECRET = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  
  ```
## Cleaning Data.
 
 ### Cleaning data before pushing to SQl server and making the data easy to read as the data will be unstructured and filled with unwanted emojis.
 ### pyspark or pandas can be used here I used pandas but i suggest spark becasuse it is better. 
 
 
 ## Point's to note and other Information.
 - ### Getting User location is hard as some user dont mention the loaction.
 - ### user Screen name and user name is always different so it is best to use user id.
 - ### City names may be changed or have differnt name for same city eg banglore and begaluru.
 - ### while installing modules don't mix pip and conda :sweat_smile: 
 - ### best to do project in new envirnoment.
 - ### Final data should be emoji free and other unwanted items like RT , @ , # etc
 - ### As twitter allows 500 pull while developing and 100 pulls while deploying it is better to store data in sepreate Data base. 
 
## MySql Server
 ### The MySQL server provides a database management system with querying and connectivity capabilities, as well as the ability to have excellent data structure and  integration with many different platforms. It can handle large databases reliably and quickly in high-demanding production environments.
 ### As the definition says it's used to store data form twitter API.
 ### If you don't want to store in mysql you can skip but you will have limted number of tweets.
 ### you can even replace existing table if you want to.

### Create local MYsql server.

```
host="localhost"
user="root"
passwd="password"
database_table="TwitterDB"

```
## Input Search_words.

### It can be anyting the you waant to search . As i am learning flask. I will impliment instant search and get analysis mehond Soon :smile:
### For demo i used IPl as it was IPl season.

## Other csv and data files.
- ### You want other data set like city name's and state names.
- ### you need geoJson file for different country.
- ### Importing modulse and installing all the requriments. 

# Developing.
- ### creating a web app using Dash. Dash is a productive Python framework for building web applications. Written on top of Flask, Plotly.js, and React.js, Dash is ideal for building data visualization apps with highly custom user interfaces in pure Python.
- ### getting Data from MySQL server and applying Textblob to create polarity which further used to decide the sentiment of an tweet 
- ### use Ploty to visualization the data 

## Ploty image of final visualization.
  ![demo](https://user-images.githubusercontent.com/68987382/164971389-0bae6aba-4778-498c-8c77-459366941157.png)
  
## Creating Dash Application.

### why dash ??
- ### Dash is simple enough that you can bind a user interface to your code in less than 10 minutes.
- ### Dash apps are rendered in the web browser. You can deploy your apps to VMs or Kubernetes clusters and then share them through URLs. Since Dash apps are viewed in       the web browser, Dash is inherently cross-platform and mobile ready.
- ### You can learn about dash [here](https://dash.plotly.com/introduction).

# Deploying
- ### deployment is last part where you and other use your app simultaneously.
- ### AWS, Google cloud, Microsoft Azure , heroku are some of the cloud pltforms that can be used for deployment.
- ### before deploying you need to set up some files like procfile, requriments, runtime , if you are using nltk use nltk.txt and mention what to download.
- ## __If you are deploying using git hub Change your branch from master to main__.

## Heroku
- ### Heroku is a container-based cloud platform as a Service (PaaS). Developers use Heroku to deploy, manage, and scale modern apps you can learn about heroku [here](https://devcenter.heroku.com/categories/reference). You can deploy a free app here.
- ### create an heroku account and create app by giving name that you want.
- ### You can deploy using github or by pushing from loacl drive.
- ### you need  Heroku CLI, Download and install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
- ### login though cmd in windows and use git bash to push.

## login and deployment.
- ## login through cmd 
 ![](https://user-images.githubusercontent.com/68987382/164972506-4df885b5-33ed-49d7-ad81-eeeee922826a.png)
- ## use git bash form deployment 
 ![](https://user-images.githubusercontent.com/68987382/164972534-ff39b0aa-b89b-46b4-92b9-0d17db190bfd.png)

```
mkdir folder name
cd folder name

$ git init        # initializes an empty git repo 
$ virtualenv venv # creates a virtualenv called "venv" 
$ source venv/bin/activate # uses the virtualenv
$ Heroku git: remote -a THIS-IS-YOUR-APP-NAME

```
- ### Create fresh python modulse inside new env.

```
$ pip install dash 
$ pip install plotly
$ pip install gunicorn
```
- ### After creating requried files Procfile,requriment,runtime.
 ```
 Deploy app
$ heroku create THIS-IS-YOUR-UNIQUE-APP-NAME
$ git add .
$ git commit -m 'Initial the app' 
$ git push heroku main # deploy code to heroku 
 
```
- ### After deployment , use ```heroku open``` to see your file.

# Final thoughts and future Impovement
- ### As i told earlier git hub's branch is main so use main delete old branch and create new one
- ### ``` git checkout -b main ``` and to delete ```git branch -D master``` 
- ### nltk.txt file must be created for to download stopwords and putnk
- ### if app is craching means that twitter rate is reached so you cannot use it until a day
 
