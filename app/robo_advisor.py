# app/robo_advisor.py
# Adapted from screencast: https://www.youtube.com/watch?v=UXAVOP1oCog&t=847s

import json
import datetime
import os
import csv
import re

from dotenv import load_dotenv
import requests

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

load_dotenv()

print("REQUESTING SOME DATA FROM THE INTERNET...")


API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="OOPS")

#
#Processing user inputs.
#

#User inputs with Validation: adapted from https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
symbol = input("Please type a stock symbol you are looking for:  ")
if not (0 < len(symbol) < 7):
    print("Sorry! That ticker is invalid. Please try again!")
    exit() 
elif any(q.isdigit() for q in symbol):
    print("Sorry! Tickers do not contains digits. Please try again!")
    exit()
print(f"You chose: " + str(symbol))

if __name__ == "__main__":
    while True:
        risk_tolerance = input("How much risk will you accept? Please enter a number between 1 and 10, with 1 being very low risk and 10 being very high risk: ")
        if 1<= float(risk_tolerance) <= 10 :
            break 
        else:
            print("Sorry, the number is invalid. Please try again.") 

#Requesting informatino from the Internet with a unique API key
request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}]"

response = requests.get(request_url)

#handle response errors
if "Error Message" in response.text:
    print("OOPS couldn't find that symbol, please try again!")
    exit()

parsed_response = json.loads(response.text)   
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

#Calculate recommendation based on the user risk tolerance
recommend_plan = " "
risk_percentage = float(risk_tolerance)/20
if (float(latest_close) - float(recent_low))/float(recent_low) > risk_percentage:
    recommend_plan = "Not BUY! because stock risk is higher than your desired risk."
else:
    recommend_plan = "Buy! Risk, stock risk is within your desired risk."

#
# INFO OUTPUTs
#

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_header = ["timestamp", "open", "high", "low", "close", "volume"]
with open(csv_file_path, "w") as csv_file: 
    writer = csv.DictWriter(csv_file, fieldnames=csv_header)
    writer.writeheader()
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date, 
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["6. volume"]
            })
 

#The date and time when the program was executed, formatted in a human-friendly way (e.g. "Run at: 11:52pm on June 5th, 2018")
#The date when the data was last refreshed, usually the same as the latest available day of daily trading data (e.g. "Latest Data from: June 4th, 2018")

print("-------------------------")
print("SELECTED SYMBOL: " + symbol)
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {current_time}")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION AND REASON: " + recommend_plan)
print("RECOMMENDATION METHOD: We compare your risk tolerance and stock risk, which is calculated by the ratio of the difference between latest closing price and recent lowest price to recent lowest price.")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

