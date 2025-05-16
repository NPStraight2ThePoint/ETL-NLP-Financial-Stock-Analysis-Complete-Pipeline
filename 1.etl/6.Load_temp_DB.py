import pandas as pd
import os
from datetime import datetime
from pathlib import Path
from dir_utils import FDM, output_dir
from config_utils import engine

exchanges_file = output_dir / f"exchanges_{FDM}.csv"
df = pd.read_csv(exchanges_file)

exchange = df.loc[0, 'exchange']
print(exchange)
base_path = output_dir

file_table_map = {
    f"{exchange}_members_{FDM}.csv": "members",
    f"{exchange}_owners_{FDM}.csv": "owners",
    f"{exchange}_insider_transactions_{FDM}.csv": "insider_transactions",
    f"{exchange}_listings_{FDM}.csv": "listings",
    f"exchanges_{FDM}.csv": "exchanges",
    f"{exchange}_{FDM}.csv": "companies",
    f"{exchange}_Transposed_{exchange}_statements_{FDM}.csv": "statements"
}

for file_name, table_name in file_table_map.items():
    file_path = os.path.join(base_path, file_name)

    if not os.path.exists(file_path):
        print(f"⛔ Skipped: {file_name} not found.")
        continue

    if os.path.getsize(file_path) == 0:
        print(f"⚠️ Skipped: {file_name} is empty.")
        continue

    df = pd.read_csv(file_path)

    if df.empty:
        print(f"⚠️ Skipped: {file_name} has no rows.")
        continue

    print(f"📥 Loading {file_name} into '{table_name}' table...")

    # Special handling for exchanges table
    if table_name == "exchanges":
        df = df.head(1)
        df = df.dropna(subset=['index_date', 'exchange', 'company_count'])

        if df.empty:
            print(f"⚠️ Skipped: {file_name} has no valid 'exchanges' row after filtering.")
            continue

        df['index_date'] = pd.to_datetime(df['index_date'], dayfirst=True).dt.date

    df.to_sql(table_name, engine, if_exists='append', index=False)
