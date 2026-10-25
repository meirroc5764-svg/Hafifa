import os

COMPANYS_LIST = ["BITCOIN_DATES", "GOOGLE_DATES", "AMAZON_DATES"]


for company in COMPANYS_LIST:

    file_path = os.environ.get(company)

    with open(file_path, "r", encoding="utf-8") as file:
        dates = file.read()

    dates_list = dates.splitlines()

    print(dates_list)