import csv, time, datetime
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
csv_file = 'Results.csv' #Name of the document where results will be stored.

#TODO Hacer que escriba siempre que pasa por el loop si el arreglo.
#Records the data into a .csv file
def record(writer, date, compound, negative, neutral, positive, open_price, close_price, high, low, volume_from, gain):
    print('Storing data...')
    writer.writerow({'date': date ,
                    'negative':negative,
                    'neutral':neutral,
                    'positive':positive,
                    'compound': compound,
                    'open': open_price,
                    'close': close_price,
                    'high': high,
                    'low': low,
                    'volume_from': volume_from,
                    'gain': gain })

#Compares the openning price to the closing price to see if there was a profit.
def compare(open_price, close):
    if close <= open_price:
        print('loss')
        return -1 #There is a profit
    else:
        print('gain')
        return 1 #There is no profit

def process(data,name):
    acc = 0
    size = len(data)
    for i in range(0,size):
        acc = acc + float(data[i])
    prom = acc/(size)
    print('Range: ',name,prom)
    return prom 

def main():
    analyzer = SentimentIntensityAnalyzer()
    tweets = [] #Stores the tweets
    dates = [] #Stores the dates of the tweets
    arr_compound = [] # Stores the compund of the sentiment Analysis.
    arr_positive = [] #Stores the positives of the sentiment Analysis.
    arr_neutral = [] #Stores de neutral values of the sentiment Analysis.
    arr_negative= [] #Store the negative values of the Sentiment Analysis.

    #Getting the crypto information
    crypto_data = cryptocompare.get_historical_price_minute('BTC', curr='EUR', limit=1)
    date = datetime.datetime.fromtimestamp(crypto_data[0]['time']).strftime('%d-%m-%Y %H:%M:%S')
    open_price = crypto_data[0]['open']
    close_price = crypto_data[0]['close']
    high = crypto_data[0]['high']
    low = crypto_data[0]['low']
    volume_from = crypto_data[0]['volumefrom']
    gain = compare(crypto_data[0]['close'],crypto_data[1]['close'])
    print("=================================================================================")
    print('Crypto info date: ',date)
    #Getting the tweets form the API.
    for tweet in tweepy.Cursor(api.search, q='Bitcoin -giving -Giveaway', lang='en').items(10):
        tweets.append(tweet.text)
        dates.append(tweet.created_at)
        print('Tweet date: ',tweet.created_at)

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
        #Storing the values of the analysis.
        arr_compound.append(comp)
        arr_positive.append(pos)
        arr_neutral.append(neu)
        arr_negative.append(neg)

        print('Negative: ',neg)
        print('Neutral: ' ,neu)
        print('Positive: ',pos)
        print('Compound: ',comp)

    compound = process(arr_compound,'compound')
    positive = process(arr_positive,'positive')
    negative = process(arr_negative,'negative')
    neutral = process(arr_neutral,'neutral')

    #Creating the object to write in the csv file.
    with open('Results.csv', mode='a') as csv_file:
        fieldnames = ['date','negative','neutral','positive','compound','open','close','high','low','volume_from','gain']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        record(writer, date, compound, negative, neutral, positive, open_price, close_price, high, low, volume_from, gain)
        
if __name__ == "__main__":
    with open('Results.csv', mode='w') as csv_file:
        fieldnames = ['date','negative','neutral','positive','compound','open','close','high','low','volume_from','gain']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
    main()
    while 1:
        time.sleep(60)
        main()
