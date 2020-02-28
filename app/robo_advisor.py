# app/robo_advisor.py

import requests
import json
import datetime
import os
import csv
from dotenv import load_dotenv

load_dotenv()

print("REQUESTING SOME DATA FROM THE INTERNET...")

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="OOPS")

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)
#
#Processing user inputs.
#

symbol = input("Please type a stock symbol you are looking for:  ")
print(f"You chose: " + str(symbol))

#Vadlidating user inputs
if len(symbol) != 4:
    print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again.")
    exit()
#elif int(symbol) == [0,99999]:
#    print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again.")
#    exit()

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}]"

#print("URL: ", request_url)
response = requests.get(request_url)
#print(type(response))   #>'requests.models.Response'
#print(dir(response))
#print(response.status_code)
#print(response.text)
#print(type(response.text))  #>'str'

#handle response errors
if "Error Message" in response.text:
    print("OOPS couldn't find that symbol, please try again!")
    exit()

parsed_response = json.loads(response.text) #>to parse response.text (str) to dict
#print(type(parsed_response))    
#> list dict_keys(['Meta Data', 'Time Series (Daily)'])
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"] 

tsd = parsed_response["Time Series (Daily)"]

#Assuming the latest day is non top
dates = list(tsd.keys())

latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]

#Get high price from each day
#maximum of all high prices
high_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(high_price)

recent_high = max(high_prices)


#Writing a CSV file 
#csv_file_path = "data/stock.csv" 
#
#tsd = parsed_response["Time Series (Daily)"]
#for date, prices in tsd.items():
#    print(date)
#    print(prices)
#    print("----")


#
# INFO OUTPUTs
#


now = datetime.datetime.today()
current_time = now.strftime("%Y-%m-%d %H:%M:%S")

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {current_time}")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")