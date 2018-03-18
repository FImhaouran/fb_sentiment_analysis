
from urllib.request import urlopen
import urllib.request
import json
import datetime
import csv
import time
from textblob import TextBlob
import re

# use access token (expires fast, so should probably made again) 
# and type in (marketing) page id 
token = "EAACEdEose0cBAPhdwfLpas3euce1x9oWpNhxUl1uSJ8B0Sgv8CRsRcZB6A3a63ZAEYnkrhZBHnXVSb4TVtLogz5uSQWHxwjUnoHkr3ZCpDupgUGaxYEcHKfocZCYIo3bZB8H0EPOcHrvCiIZBBDFQitt2ZC9LkZCOg0vx0wrWzjtwFZB5XNcVpZBUYLnFrBXSZBUAIZCbf32IPWZA5ZCAZDZD"
page_id ="nike"


# get facebook id and facebook name
def check_fb_page(page_id, token):
      
    p_id = "/" + page_id
    param = "/?access_token=%s" % token
    url = "https://graph.facebook.com/v2.4" + p_id + param
    # retrieve data
    request = urllib.request.Request(url)
    
    response = urlopen(request)
    data = json.loads(response.read().decode("utf-8"))
    
    print(json.dumps(data, indent=4, sort_keys=True))
    

# check_fb_page(page_id, token)

# checking response of the url 
def check_request(url):
    req = urllib.request.Request(url)
    success = False
    while success is False:
        try: 
            response = urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception: 
            time.sleep(5)            
            print("Error Url %s: %s" % (url, datetime.datetime.now()))

    return response.read()

# page id, acces and numer of posts
def fbposts_data(page_id, token, num_statuses):
    
    # construct the URL string
    begin_url = "https://graph.facebook.com" + "/" + page_id + "/feed" 
    
    param = "/?fields=message,link,created_time,type,name,id,likes.limit(1).summary(true),comments.limit(999).summary(true),shares&limit=%s&access_token=%s" % (num_statuses, token) # changed
    url = begin_url + param
    # retrieve data
    data = json.loads(check_request(url).decode("utf-8"))
    
    return data


def sentiment_analyses():    
    # select the amount of posts to analyze
    fb_page_data = fbposts_data(page_id, token,8)["data"]

    # opening csv file to save sentiment results
    fb_file = open('fb_marketing.csv', 'a')
    fb_file.write("post, sentiment_score\n")

    print("---------------------processing fb data---------------------")
    num_comment = 0
    tot_sentiment = 0

    for i in fb_page_data:
        # "the Marketing Post"
        if num_comment > 0:
            avg_sentiment = tot_sentiment / num_comment
            # write the sentiment number to csv file
            fb_file.write(str(round(avg_sentiment, 2))+","+"\n")
            # print(num_comment)
        
        # i['message'] is the ad post
        # print(i["message"])
        
        num_comment= 0
        tot_sentiment = 0
        post = re.sub('[^0-9a-zA-Z]+', '*', i['message'])
        
        fb_file.write(post+",")
        
        # "the reaction on the post"
        for j in i["comments"]['data']:
            # get sentiment score of the comment
            blob = TextBlob(j['message'])
            num_comment += 1
            sentiment = blob.sentiment.polarity
            tot_sentiment += sentiment
            # print("Sentiment of the reaction: %f"%(blob.sentiment.polarity))
            
sentiment_analyses()