# Twitter-Live-Sentimental_Analysisi_and_topic_tracking
### Hi there 👋,
![20220424_014447](https://user-images.githubusercontent.com/68987382/164944757-f8c87551-1987-4526-8fdf-75f0efd03ff1.gif)

# Inspiration

### This self-motivated independent  project aims to develop a web application for sentimental analysis of a trend or a topic for someone who  likes to know what's happening around and how one's trend or specific topic is doing on the internet. The project is divided into three parts collecting, developing, and deploying.This solution for evaluating Twitter data is to perform better business decisions and keep tracking all relevant Twitter data about a brand in real-time, perform analysis as topics or issues emerge. By monitoring brand mentions on Twitter, brands could inform management and deliver better experiences for their customers across the word.

# Abstract View
  
 ## This project consist of three parts collecting data , transforming Data , deploying.
  
  ![](https://github.com/prajwal470/Twitter-Live-Sentimental_Analysis_and_topic_tracking/blob/0c585506bb285a74a9b13a18d8d62c1207c93688/Untitled%20Diagram.drawio.png)
 
 # Collecting Data

### Collecting data is a necessary part of this project. I  used Twitter API to collect the data from the server . The Twitter API lets you read and write Twitter data. Thus, you can use it to compose tweets, read profiles, and access your followers’ data and a high volume of tweets on particular subjects in specific locations. API stands for Application Programming Interface. This software provides "middleman services" between two applications that want to communicate with each other. Any requests you make go to the server first and the response given comes through the same route. one can read documents of Twitter [here](https://developer.twitter.com/en/docs/twitter-api).

## Twitter API

### To get work with api we need some way to connect to the server to connect Go to http://apps.twitter.com and create an app hear consumer key and secret will be generated for you
  ```
  
  API_KEY = "XXXXXXXXXXXXXX"
  API_SECRET_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  After the step above, you will be redirected to your app's page.
  Create an access token under the the "Your access token" section
  ACCESS_TOEKN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  ACCESS_TOKEN_SECRET = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  
  ```
## Cleaning Data
 
 ### Cleaning data before pushing to SQl server and making the data easy to read as the data will be unstructured and filled with unwanted emojis.
 ### pyspark or pandas can be used here I used pandas but i suggest spark becasuse it is better 
 
 
 ## point's to note and other Information
 - ### Getting User location is hard as some user dont mention the loaction
 - ### user Screen name and user name is always different so it is best to use user id
 - ### City names may be changed or have differnt name for same city eg banglore and begaluru
 - ### while installing modules don't mix pip and conda :sweat_smile: 
 - ### best to do project in new envirnoment
 - ### Final data should be emoji free and other unwanted items like RT , @ , # etc
 - ### As twitter allows 500 pull while developing and 100 pulls while deploying it is better to store data in sepreate Data base  
 
## MySql Server
 ### The MySQL server provides a database management system with querying and connectivity capabilities, as well as the ability to have excellent data structure and  integration with many different platforms. It can handle large databases reliably and quickly in high-demanding production environments.
 ### As the definition says it's used to store data form twitter API.
 ### If you don't want to store in mysql you can skip but you will have limted number of tweets.
 ### you can even replace existing table if you want to.

### create local MYsql server

```
host="localhost"
user="root"
passwd="password"
database_table="TwitterDB"

```
## Input Search_words

### It can be anyting the you waant to search . As i am learning flask. I will impliment instant search and get analysis mehond Soon :smile:
### For demo i used IPl as it was IPl season

## Other csv and data files
- ### You want other data set like city name's and state names
- ### you need geoJson file for different country
- Importing modulse and installing all the requriments 

 
 
