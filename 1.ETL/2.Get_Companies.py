import requests
import pandas as pd
import time
from datetime import datetime
from pathlib import Path
from dir_utils import FDM, output_dir
from api_queries import QUERY_ALL_COMPANIES
from config_utils import url, headers, API_KEY
file_path = output_dir / f"exchanges_{FDM}.csv"

df_exchanges = pd.read_csv(file_path)
company_count = df_exchanges['company_count'].iloc[0]

# Loop through each exchange
for _, row in df_exchanges.iterrows():
    exchange_symbol = row['exchange']
    if pd.isna(exchange_symbol) or str(exchange_symbol).strip() == "":
        print("⚠️  Encountered blank exchange symbol. Stopping loop.")
        break
    print(f"\nFetching companies for exchange: {exchange_symbol}")

    all_companies = []
    offset = 0
    step = 90

    while True:
        variables = {
            'exchange': exchange_symbol,
            'limit': step,
            'offset': offset
        }
        response = requests.post(
            url,
            json={'query': QUERY_ALL_COMPANIES, 'variables': variables},
            headers=headers
        )
        if response.status_code != 200:
            print(f"❌ Error on {exchange_symbol} offset {offset}: {response.status_code}")
            break
        data = response.json()
        companies = data['data']['companies']
        if not companies:
            print(f"✅ Completed fetching for {exchange_symbol} (Total: {offset} records)")
            break
        # Add IsETF flag based on statements
        for company in companies:
            is_etf = False
            for stmt in company.get('statements', []):
                if stmt.get('name', '').lower() in ['isetf', 'isexchangetradedfund'] and \
                   str(stmt.get('value', '')).lower() in ['true', '1', 'yes']:
                    is_etf = True
                    break
            company['IsETF'] = is_etf
            del company['statements']  # Optional: remove full statements list if not needed

        all_companies.extend(companies)
        offset += step
        print(f"   → Retrieved {offset} records so far...")
        time.sleep(0.1)

    # Save per exchange
    df_exchange = pd.DataFrame(all_companies)
    df_exchange.insert(0, 'index_date', FDM)
    filename = output_dir / f"{exchange_symbol}_{FDM}.csv"
    df_exchange.to_csv(filename, index=False)
    print(f"💾 Saved {len(df_exchange)} companies to {filename}")

# Final count check
if company_count == len(df_exchange):
    print(f"✅ All companies retrieved ({company_count})")
else:
    diff = company_count - len(df_exchange)
    print(f"❌ Mismatch: Expected {company_count}, Got {len(df_exchange)} (Diff = {diff})")
