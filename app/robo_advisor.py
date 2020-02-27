# app/robo_advisor.py

import requests
import json
import os
import csv
from dotenv import load_dotenv

load_dotenv()

print("REQUESTING SOME DATA FROM THE INTERNET...")

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="OOPS")

#Processing  user inputs.
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

#Writing a CSV file 
csv_file_path = "data/stock.csv" 



tsd = parsed_response["Time Series (Daily)"]
for date, prices in tsd.items():
    print(date)
    print(prices)
    print("----")
#print(parsed_response)


#
#first_prod = parsed_response[0]
#print(first_prod["name"])

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")