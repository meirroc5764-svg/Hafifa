from concurrent.futures import ThreadPoolExecutor
import yfinance.exceptions as yf_exceptions
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import os

COMPANYS_LIST = ["BITCOIN_DATES", "GOOGLE_DATES", "AMAZON_DATES"]

def write_to_csv(all_results, destination_file):
    df = pd.DataFrame(all_results)
    
    if not os.path.exists(destination_file):
            df.to_csv(destination_file, index=False)
    else:
        df.to_csv(
            destination_file,
                mode="a",
                header=False,
                index=False
            )

# Take a lists in list and open it and return one list   
def result_list(results):
    return [
        record
        for company_results in results
        for record in company_results
        ]
    

def percentage_change_calculate(new_price, old_price): 
    return (new_price - old_price) / old_price * 100

def prices_history(libary):
    for attempt in range(3):
        try:
            return yf.Ticker(libary).history(
            period="max",
            interval="1h"
            )
        except yf_exceptions.YFRateLimitError:
            if attempt == 2:
                raise

            time.sleep(10 * (attempt + 1))


'''The main function operates via two simultaneous threads: it retrieves external information about a specific company
 and its stock for a given timeframe,
 standardizes the data to a single time zone, calculates the changes, records them into a list,
 and returns that list containing all the results.'''
def running_program(company):

    # list libary to read from yfinance
    libarys = {
        "GOOGLE_DATES" : "GOOGL",
        "AMAZON_DATES" : "AMZN",
        "BITCOIN_DATES" : "BTC-USD"
    }


    file_path = os.environ.get(company)

    if not file_path:
        raise ValueError(f"Environment variable {company} is not set")

    print(company, "->", repr(file_path))

    results = []

    with open(file_path, "r", encoding="utf-8") as file:
        dates = file.read()

        
        dates_list = [line.strip() for line in dates.splitlines() if line.strip()]

        taming_data_price = prices_history(libarys[company])

        if taming_data_price.empty:
            print(f"No price data for {company} at {date}")
            return results
        
        else:
            for date in dates_list:

                try:
                    date = pd.Timestamp(date, tz="UTC")
                
                except ValueError:
                    print(f"Skipping invalid date in {company}: {date!r}")
                    continue
            

                
            
                # Find the closest available price at or before each requested time.          
                new_prices = taming_data_price.loc[
                    taming_data_price.index <= date, "Close"
                ]


                # if new price it first inposooble to be old price
                if len(new_prices) < 2:
                    print(f"Not enough price data for {company} at {date}")
                    continue

                old_price = new_prices.iloc[-2]
                new_price = new_prices.iloc[-1]

                percentage_change = percentage_change_calculate(new_price, old_price)

                json_to_csv = {
                    "hour": date,
                    "stock_type": libarys[company],
                    "percentage_change": percentage_change
                }

                results.append(json_to_csv)

        return results

def main():
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(running_program, COMPANYS_LIST))

    all_results = result_list(results)
    
    destination_file = os.environ.get("DESTINATION_FILE", "records.csv")

    write_to_csv(all_results, destination_file)

    print(f"Saved {len(all_results)} records to {destination_file}")



if __name__ == "__main__":
    main()

    

