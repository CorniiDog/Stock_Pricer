import datetime
import os
import time

from toolbox import database
from toolbox import ticker_prices
from toolbox import ticker_retreival

storage_path = "/mnt/nvme1n1p1/"

database_path = os.path.join(storage_path, "database")
ticker_retreival.set_storage_path(database_path)
ticker_prices.set_storage_path(database_path)

days_to_refresh = 1
delete_trends = False # Set to true to delete all trends

def main():

    if delete_trends:
        approved_tickers = ticker_retreival.get_tickers()
        # Remove all ticker_trends
        for ticker in approved_tickers:
            try:
                database.delete_database(ticker + "_trend")
                print(ticker)
            except:
                pass
        database.save("price_last_ticker", None)
        print("done")
        return

    last_updated = None
    while True:
        now = datetime.datetime.now()
        # If it is a new day, at 5 PM, update the database
        if last_updated is None or (now.hour == 17 and now.minute == 0 and now.second == 0 and now.day != last_updated.day):
            print("New Day, updating database")

            approved_tickers = ticker_retreival.get_tickers()
            for i, ticker in enumerate(approved_tickers):
                last_ticker = database.get("price_last_ticker")
                if last_ticker is not None:
                    if ticker != last_ticker:
                        continue
                print(ticker)
                ticker_prices.get_ticker_historical_trend(ticker)

                if i < len(approved_tickers) - 1:
                    database.save("price_last_ticker", approved_tickers[i + 1])

            database.save("price_last_ticker", None)

            last_updated = datetime.datetime.now()
        time.sleep(10)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

