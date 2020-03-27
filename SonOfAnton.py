import csv 
import time
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer #Sentiment analyzer
import tweepy #Tweeter API helper
import cryptocompare #Cryptocompare API that gets crypto prices. 

#Validation to use the Twitter API.
consumer_key = "CUtaXY1fdcZf8b3TCqncsTwHT"
consumer_secret= "28yOWNF2ENlUjTL1S6iVV238LEPs53CatldGhfHAxvttH7yidp"
access_token = "328524097-ufDmMU5l9l5sVWLyEXha4WIRG4v4kB5I0CCEXMM2"
access_token_secret= "JMIGZn9ch2zNuzuheYPBKfhbiylT0EUeRofESVrgLLsMO"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Function to write the data into the Result.csv
def register(tweets, dates, compund, negative, neutral, positive,  writer):
    for i in range(0,len(dates)):
        writer.writerow({'date': dates[i] , 'negative':negative[i], 'neutral':neutral[i], 'positive':positive[i], 'compound':compound[i]})

analyzer = SentimentIntensityAnalyzer()
tweets =[] #Stores all the tweets.
dates = [] #Stores the dates of the tweets
compound = [] # Stores the compund of the sentiment Analysis. 
positive = [] #Stores the positives of the sentiment Analysis. 
neutral = [] #Stores de neutral values of the sentiment Analysis. 
negative = [] #Store the negative values of the Sentiment Analysis. 
csv_file = 'Results.csv' #Name of the document where results will be stored. 

for tweet in tweepy.Cursor(api.search, q='Bitcoin -Giveaway', lang='en').items(10):
    tweets.append(tweet.text)
    dates.append(tweet.created_at)

for tweet in tweets:
    print("=================================================================================")    
    vs = analyzer.polarity_scores(tweet)
    print(tweet)

    #Getting the values from the Sentiment Analysis. 
    full_result = "{:-<65} {}".format(tweet, str(vs))
    result = full_result.split('{')
    split_result = str(result[1]).split(':')
    params = str(split_result).split(',')
    full_neg = str(params[1]).split('"')
    neg = full_neg[1]
    full_neu = str(params[3]).split('"')
    neu = full_neu[1]
    full_pos = str(params[5]).split('"')
    pos = full_pos[1]
    full_comp = str(params[7]).split('}')
    split_comp = str(full_comp[0]).split()
    comp = split_comp[1]

    #Storing the values. 
    compound.append(comp)
    positive.append(pos)
    neutral.append(neu)
    negative.append(neg)
    print('Negative: ',neg)
    print('Neutral: ' ,neu)
    print('Positive: ',pos)
    print('Compound: ',comp)

#Creating the object to write in the csv file. 
with open('Results.csv', mode='w') as csv_file:
    fieldnames = ['date','negative','neutral','positive','compound']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    register(tweets,dates,compound,positive,neutral,negative,writer)
