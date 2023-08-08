import argparse
import asyncio
import datetime as dt
import gzip
import json
import random

from memphis import Memphis
import pandas as pd
import tqdm

STATION = "bps-transactions"
USERNAME = "testuser"
PASSWORD = "%o3sH$Qfae"
HOST = "localhost"

def add_quantities(tx_prod_df):
    def sample_quantity():
        r = random.random()
        if r <= 0.7:
            q = 1
        elif r <= 0.9:
            q = 2
        else:
            q = 3

        return q

    tx_prod_df["quantity"] = [sample_quantity() for i in range(len(tx_prod_df))]

    return tx_prod_df.copy()

months = {
    "JANUARY" : 1,
    "FEBRUARY" : 2,
    "MARCH" : 3,
    "APRIL" : 4,
    "MAY" : 5,
    "JUNE" : 6,
    "JULY" : 7,
    "AUGUST" : 8,
    "SEPTEMBER" : 9,
    "OCTOBER" : 10,
    "NOVEMBER" : 11,
    "DECEMBER" : 12
}

def add_timestamps(tx_df):
    def sample_timestamp(month):
        """
        Samples a timestamp for the given month
        in the year 2022.
        """
        month_number = months[month]

        month_start = dt.datetime(2022, month_number, 1)

        next_month = month_number + 1
        year = 2022
        if next_month == 13:
            next_month = 1
            year = 2023

        month_end = dt.datetime(year, next_month, 1)

        start_timestamp = month_start.timestamp()
        end_timestamp = month_end.timestamp()

        sampled_timestamp = random.uniform(start_timestamp, end_timestamp)

        timestamp_dt = dt.datetime.fromtimestamp(sampled_timestamp)

        return timestamp_dt

    tx_df["timestamp"] = tx_df["month"].apply(sample_timestamp)

    return tx_df.copy()

def construct_transactions(tx_df, tx_prod_df):
    """
    For each transaction, generates a JSON object of the form:

    {
        "transaction_id" : 123,
        "timestamp" : "2019-05-18T15:17:08.132263",
        "customer_id" : 123,
        "items_sold" : [
            { "item_id" : 123, "quantity" : 1},
            { "item_id" : 101, "quantity" : 2}
        ]
    }
    
    """

    transactions = dict()
    for idx, row in tx_df.iterrows():
        obj = {
            "transaction_id" : int(row["id"]),
            "customer_id" : int(row.customer_id),
            "timestamp": row.timestamp.isoformat(),
            "items_sold" : [ ]
        }

        transactions[row.id] = obj

    for idx, row in tx_prod_df.iterrows():
        obj = {
            "item_id" : int(row.product_id),
            "quantity" : int(row.quantity)
        }
        transactions[row.transaction_id]["items_sold"].append(obj)

    return list(transactions.values())

async def upload_transactions(transactions):
    memphis = Memphis()
    await memphis.connect(host=HOST, username=USERNAME, password=PASSWORD, account_id=1)
    producer = await memphis.producer(station_name=STATION, producer_name="bps-transaction-producer")

    for tx in tqdm.tqdm(transactions):
        tx_str = json.dumps(tx)
        await producer.produce(bytearray(tx_str, "utf-8"))

    await memphis.close()

def parseargs():
    parser = argparse.ArgumentParser()

    parser.add_argument("--transactions-fl",
                        type=str,
                        required=True)

    parser.add_argument("--transactions-products-fl",
                        type=str,
                        required=True)

    return parser.parse_args()

if __name__ == "__main__":
    args = parseargs()

    tx_df = pd.read_table(args.transactions_fl, compression="gzip")
    tx_prod_df = pd.read_table(args.transactions_products_fl, compression="gzip")

    print("Loaded data.")
    
    tx_prod_df = add_quantities(tx_prod_df)

    print("Added quantities.")

    tx_df = add_timestamps(tx_df)

    print("Added timestamps.")

    transactions = construct_transactions(tx_df, tx_prod_df)

    print("Constructed transactions.")

    asyncio.run(upload_transactions(transactions))

    print("Done.")
