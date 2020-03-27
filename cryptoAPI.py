import cryptocompare #Cryptocompare API
import csv
import json
import datetime

#TODO: Get the date in format %d-%m-%Y %H:0:0

crypto_data = cryptocompare.get_historical_price_day('BTC', curr='EUR', limit=30)
days = len(crypto_data)-1

def compare(open, close):#Compares the openning price to the closing price to see if there was a profit.
    if close <= open:
        print('loss')
        return -1 #There is a profit
    else:
        print('gain')
        return 1 #There is no profit

with open('crypto.csv', mode='w') as csv_file:
    fieldnames = ['time','open','close','high','low','volume_from','volume_to','gain']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(0,days):
        writer.writerow({'time': datetime.datetime.fromtimestamp(crypto_data[i]['time']).strftime('%d-%m-%Y %H:%M:%S'),
                         'open': crypto_data[i]['open'],
                         'close': crypto_data[i]['close'],
                         'high':crypto_data[i]['high'],
                         'low': crypto_data[i]['low'],
                         'volume_from': crypto_data[i]['volumefrom'],
                         'volume_to':crypto_data[i]['volumeto'],
                         'gain':compare(crypto_data[i]['close'],crypto_data[i+1]['close'])})
