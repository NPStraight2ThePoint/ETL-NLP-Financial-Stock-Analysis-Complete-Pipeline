import pandas as pd
import requests
import datetime
import logging
import os
from flatten_functions import (flatten_all)
from datetime import datetime
from pathlib import Path
from dir_utils import FDM, output_dir
from api_queries import QUERY_ALL_DATA
from config_utils import url, headers, API_KEY

logging.basicConfig(level=logging.INFO)

exchanges_file = output_dir / f"exchanges_{FDM}.csv"
df1 = pd.read_csv(exchanges_file, encoding='utf-8')
exchange = df1['exchange'].iloc[0]
companies_file = output_dir / f"{exchange}_{FDM}.csv"
df = pd.read_csv(companies_file, encoding='utf-8')
output_dir.mkdir(exist_ok=True)

# Output containers
all_statements = []
all_listings = []
all_owners = []
all_insiders = []
all_members = []

os.makedirs("output", exist_ok=True)

all_statements, all_listings, all_owners, all_insiders, all_members = [], [], [], [], []
failed_tickers = []
filtered_df = df[(df['active'] == True) & (df['IsETF'] == False)].reset_index(drop=True)
file_tracker = {}

# Loop through filtered tickers
for idx, row in filtered_df.iterrows():
    ticker = row['tickerSymbol']
    exchange = row['exchangeSymbol']
    variables = {"exchange": exchange, "tickerSymbol": ticker}

    print(f"[{idx + 1}/{len(filtered_df)}] Processing: {exchange}:{ticker}")

    try:
        response = requests.post(
            url,
            json={"query": QUERY_ALL_DATA, "variables": variables},
            headers=headers
        )
        json_data = response.json()
        company = json_data["data"]["companyByExchangeAndTickerSymbol"]

        if company:
            print(f"✔️  Data received for {ticker}, flattening...")
            statements, listings, owners, insider_transactions, members = flatten_all(company, ticker, exchange, FDM)

            def append_to_csv(data, name):
                if data:
                    file_path = output_dir / f"{exchange}_{name}_{FDM}.csv"
                    first_write = file_path not in file_tracker
                    pd.DataFrame(data).to_csv(file_path, mode='a', index=False, header=first_write)
                    file_tracker[file_path] = True

            append_to_csv(statements, "statements")
            append_to_csv(listings, "listings")
            append_to_csv(owners, "owners")
            append_to_csv(insider_transactions, "insider_transactions")
            append_to_csv(members, "members")

        else:
            print(f"⚠️  No data found for {ticker}")

    except Exception as e:
        print(f"❌ Error processing {ticker}: {str(e)}")
        fail_row = {
            "index": idx + 1,
            "ticker": ticker,
            "exchange": exchange,
            "error": str(e)
        }
        fail_file = output_dir / "failed_tickers.csv"
        fail_first_write = not fail_file.exists()
        pd.DataFrame([fail_row]).to_csv(fail_file, mode='a', index=False, header=fail_first_write)

print("✅ All tickers processed (errors logged if any).")
