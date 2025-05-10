import pandas as pd
from pathlib import Path
import os
from datetime import datetime
import re
from dir_utils import FDM, output_dir

exchanges_file = output_dir / f"exchanges_{FDM}.csv"
df1 = pd.read_csv(exchanges_file, encoding='utf-8')

exchange = df1['exchange'].iloc[0]

def transpose_csv(base_directories):
    for base_directory in base_directories:
        print(f"\U0001F50D Processing directory: {base_directory}")

        for root, dirs, files in os.walk(base_directory):
            for file in files:
                if "statements" in file.lower() and file.endswith(".csv"):  # Filter statements CSV files
                    file_path = os.path.join(root, file)
                    print(f"\U0001F4C4 Processing: {file_path}")

                    try:
                        df = pd.read_csv(file_path)
                        required_columns = {'ticker', 'exchange', 'date', 'area', 'name', 'value', 'description'}
                        if not required_columns.issubset(df.columns):
                            print(f"⚠️ Missing required columns in {file_path}. Skipping transformation.")
                            continue  # Skip files that don't have the required columns

                        # Aggregate duplicate (ticker, exchange, date, area, name) before pivoting
                        df = df.groupby(['ticker', 'exchange', 'date', 'area', 'name'], as_index=False).agg({
                            'value': 'first',  # Adjust aggregation method if needed
                            'description': 'first'})

                        # Create new column names for pivoting
                        df['name_value'] = df['area'] + "_" + df['name'] + "_Value"
                        df['name_desc'] = df['area'] + "_" + df['name'] + "_Desc"

                        # Pivot tables for values and descriptions
                        df_value = df.pivot(index=['ticker', 'exchange', 'date'], columns='name_value', values='value')
                        df_desc = df.pivot(index=['ticker', 'exchange', 'date'], columns='name_desc',
                                           values='description')

                        # Merge both pivot tables
                        df_pivot = pd.concat([df_value, df_desc], axis=1).reset_index()

                        df_pivot.columns = df_pivot.columns.str.replace(
                            "VALUE_IsGoodValueComparingPreferredMultipleToPeersAverageValue_Value",
                            "VALUE_IsGoodValueComparingPreferredMultipleToPeersAvgVal_Value")
                        df_pivot.columns = df_pivot.columns.str.replace(
                            "VALUE_IsGoodValueComparingPreferredMultipleToPeersAverageValue_Desc",
                            "VALUE_IsGoodValueComparingPreferredMultipleToPeersAvgVal_Desc")

                        output_csv = os.path.join(root, f"{exchange}_Transposed_{file.replace('.csv', '')}.csv")
                        df_pivot.to_csv(output_csv, index=False)

                        print(f"✅ Successfully transposed and saved: {output_csv}")
                    except Exception as e:
                        print(f"❌ Error processing {file}: {e}")


transpose_csv([output_dir])
