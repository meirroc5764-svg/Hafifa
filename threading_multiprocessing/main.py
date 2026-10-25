from concurrent.futures import ThreadPoolExecutor
import yfinance.exceptions as yf_exceptions
import yfinance as yf
import pandas as pd
import time
import os

# list libary to read from yfinance
THREDINGS_DATES_LIBRARY = {
        "GOOGLE_DATES" : "GOOGL",
        "AMAZON_DATES" : "AMZN",
        "BITCOIN_DATES" : "BTC-USD"
    }

COMPANY_DATES = list(THREDINGS_DATES_LIBRARY.keys())


def write_to_csv(all_results, destination_file):
    df = pd.DataFrame(all_results)
    
    if not os.path.exists(destination_file):
            df.to_csv(destination_file, index=False)
    else:
        df.to_csv(
            destination_file,
                mode="w",
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
     
     if old_price == 0:
        raise ValueError("Old price cannot be zero")
     
     return (new_price - old_price) / old_price * 100


'''take all last data in libary'''
def fetch_prices_history(libary):
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

    file_path = os.environ.get(company)

    if not file_path:
        raise ValueError(f"Environment variable {company} is not set")

    print(company, "->", repr(file_path))

    results = []

    with open(file_path, "r", encoding="utf-8") as file:
        dates = file.read()

        
        dates_list = [line.strip() for line in dates.splitlines() if line.strip()]

        taming_company_price = fetch_prices_history(THREDINGS_DATES_LIBRARY[company])

        if taming_company_price.empty:
            print(f"No price data for {company}")
            return results
        
        else:
            for date in dates_list:

                try:
                    date = pd.Timestamp(date, tz="UTC")
                
                except ValueError:
                    print(f"Skipping invalid date in {company}: {date!r}")
                    continue
            
            
                # Find the closest available price at or before each requested time.          
                new_data_prices = taming_company_price.loc[
                    taming_company_price.index <= date, "Close"
                ]


                # if new price it first inposooble to be old price
                if len(new_data_prices) < 2:
                    print(f"Not enough price data for {company} at {date}")
                    continue

                old_price = new_data_prices.iloc[-2]
                new_price = new_data_prices.iloc[-1]

                if old_price == 0:
                    print(f"Previous price is zero for {company} at {date}")
                    continue

                percentage_change = percentage_change_calculate(new_price, old_price)

                json_to_csv = {
                    "hour": date,
                    "stock_type": THREDINGS_DATES_LIBRARY[company],
                    "percentage_change": percentage_change
                }

                results.append(json_to_csv)

        return results

def main():
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(running_program, COMPANY_DATES))

    all_results = result_list(results)
    
    destination_file = os.environ.get("DESTINATION_FILE", "records.csv")

    write_to_csv(all_results, destination_file)

    print(f"Saved {len(all_results)} records to {destination_file}")



if __name__ == "__main__":
    main()

