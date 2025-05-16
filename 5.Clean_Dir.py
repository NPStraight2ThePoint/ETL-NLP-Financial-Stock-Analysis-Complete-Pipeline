import os
import shutil
import pandas as pd
from datetime import datetime
from dir_utils import output_dir, FDM

exchanges_file = output_dir / f"exchanges_{FDM}.csv"
df = pd.read_csv(exchanges_file)
exchange = df.loc[0, 'exchange']
source_folder = output_dir
destination_folder = os.path.join("../1.ETL/Data Archive", FDM, exchange)

# Create destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Move ALL CSVs to the destination folder
for filename in os.listdir(source_folder):
    if filename.endswith(".csv"):
        src_file = os.path.join(source_folder, filename)
        dest_file = os.path.join(destination_folder, filename)
        shutil.move(src_file, dest_file)
        print(f"📦 Moved: {filename} → {dest_file}")

print("✅ All CSV files moved to:", destination_folder)


