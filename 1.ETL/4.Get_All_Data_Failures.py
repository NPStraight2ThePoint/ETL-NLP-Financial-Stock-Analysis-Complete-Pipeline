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
failures_file = output_dir / 'failed_tickers.csv'
df = pd.read_csv(failures_file, encoding='utf-8')
failures_file_2 = output_dir / 'failed_tickers2.csv'
# Output containers
all_statements = []
all_listings = []
all_owners = []
all_insiders = []
all_members = []

# Output directory
os.makedirs("output", exist_ok=True)

# Output containers
all_statements, all_listings, all_owners, all_insiders, all_members = [], [], [], [], []
failed_tickers = []

# Helper function to append data to CSV
def append_to_csv(data, filename):
    file_exists = os.path.isfile(filename)
    pd.DataFrame(data).to_csv(
        filename,
        mode='a',
        index=False,
        header=not file_exists
    )

# Loop through tickers
for idx, row in df.iterrows():
    #if not row['active']:
        #continue

    ticker = row['ticker']
    exchange = row['exchange']
    variables = {"exchange": exchange, "tickerSymbol": ticker}

    print(f"[{idx + 1}/{len(df)}] Processing: {exchange}:{ticker}")

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
            statements, listings, owners, insider_transactions, members = flatten_all(
                company, ticker, exchange, FDM
            )

            # Append to output files
            append_to_csv(statements, f"output/{exchange}_statements_{FDM}.csv")
            append_to_csv(listings, f"output/{exchange}_listings_{FDM}.csv")
            append_to_csv(owners, f"output/{exchange}_owners_{FDM}.csv")
            append_to_csv(insider_transactions, f"output/{exchange}_insider_transactions_{FDM}.csv")
            append_to_csv(members, f"output/{exchange}_members_{FDM}.csv")

        else:
            print(f"⚠️  No data found for {ticker}")

    except Exception as e:
        print(f"❌ Error processing {ticker}: {str(e)}")
        failed_tickers.append({
            "index": idx + 1,
            "ticker": ticker,
            "exchange": exchange,
            "error": str(e)
        })

# Save failed tickers (overwrite each time)
if failed_tickers:
    pd.DataFrame(failed_tickers).to_csv(failures_file_2, index=False)
    print(f"🚨 {len(failed_tickers)} tickers failed. Logged to output/failed_tickers2.csv")
else:
    print("✅ All tickers processed successfully.")


if os.path.exists(failures_file):
    os.remove(failures_file)
    print(f"Deleted '{failures_file}'")
else:
    print(f"File '{failures_file}' does not exist.")

old_name = failures_file_2
new_name = failures_file

os.rename(old_name, new_name)
print(f"Renamed '{old_name}' to '{new_name}'")
