import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from config_utils import SRC_DB, DEST_DB

TABLE_NAME = "insider_transactions"

def find_new_rows_only(table_name, src_engine, dest_engine):
    try:
        print(f"\n🔍 Checking for new rows in '{table_name}'...")

        src_df = pd.read_sql_table(table_name, src_engine)
        print(f"📥 Source rows: {len(src_df)}")

        if src_df.empty:
            print(f"⚠️  Source table '{table_name}' is empty.")
            return pd.DataFrame(), pd.DataFrame()

        try:
            dest_df = pd.read_sql_table(table_name, dest_engine)
            print(f"📂 Destination rows: {len(dest_df)}")
        except Exception:
            print("🆕 Destination table does not exist or is empty.")
            dest_df = pd.DataFrame(columns=src_df.columns)

        # Align dtypes to avoid merge errors
        for col in src_df.columns:
            if col in dest_df.columns:
                try:
                    dest_df[col] = dest_df[col].astype(src_df[col].dtype)
                except Exception:
                    pass  # tolerate type mismatch in dest

        # Full row comparison
        merged_df = src_df.merge(dest_df, how="outer", indicator=True)
        new_rows = merged_df.query('_merge == "left_only"').drop(columns=['_merge'])

        print(f"🆕 Found {len(new_rows)} new rows not in destination.")
        return new_rows, src_df

    except Exception as e:
        print(f"❌ Error during comparison: {e}")
        return pd.DataFrame(), pd.DataFrame()

def main():
    print("🚀 Starting comparison of source vs. destination...")

    src_engine = create_engine(SRC_DB)
    dest_engine = create_engine(DEST_DB)

    new_rows, original_src = find_new_rows_only(TABLE_NAME, src_engine, dest_engine)

    if not original_src.empty:
        print(f"✏️ Removing all rows from source table...")
        with src_engine.begin() as conn:
            conn.execute(text(f"DELETE FROM {TABLE_NAME}"))

    if not new_rows.empty:
        print("📤 Inserting only new rows to source table...")
        new_rows.to_sql(TABLE_NAME, src_engine, if_exists='append', index=False)
        print("✅ Source table updated with only new rows.")
    else:
        print("✅ No new rows found. Source table emptied to remove existing matches.")

if __name__ == "__main__":
    main()
