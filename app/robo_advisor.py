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
    print("Oh, expecting a properly-formed stock symbol like 'MSFT' with no space. Please try again.")
    exit() #TODO: Validate invalid user inputs further

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}]"

response = requests.get(request_url)


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

#Get high price from each day with the maximum of all high prices
high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(high_price)
    low_price = tsd[date]["3. low"]
    low_prices.append(low_price)

recent_high = max(high_prices)
recent_low = min(low_prices)

now = datetime.datetime.today()
current_time = now.strftime("%Y-%m-%d %H:%M:%S")

#
# INFO OUTPUTs
#


csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=["city", "name"])
    writer.writeheader() # uses fieldnames set above
    writer.writerow({"city": "New York", "name": "Yankees"})
    writer.writerow({"city": "New York", "name": "Mets"})
    writer.writerow({"city": "Boston", "name": "Red Sox"})
    writer.writerow({"city": "New Haven", "name": "Ravens"})



print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {current_time}")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print(f"fWRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

