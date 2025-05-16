import psycopg2
import pandas as pd
from datetime import datetime
from config_nlp_utils import DB_PARAMS
from dir_nlp_utils import FDM, columns_to_keep, final_columns, score_categories, output_dir

exchanges_file = output_dir / f"exchanges_{FDM}.csv"
df1 = pd.read_csv(exchanges_file, encoding='utf-8')
exchange = df1['exchange'].iloc[0]
queries = {
    "company_statements": f"SELECT * FROM statements WHERE exchange = '{exchange}';"
}

STATEMENTS = f'C:/.../.venv/2.Enhancement/Output/{exchange}_Statements_{FDM}.xlsx'
SNOWFLAKE = f'C:/.../.venv/2.Enhancement/Output/{exchange}_Snowflake_{FDM}.xlsx'

try:
    conn = psycopg2.connect(**DB_PARAMS)
    with pd.ExcelWriter(STATEMENTS, engine="xlsxwriter") as writer:
        for sheet_name, query in queries.items():
            df = pd.read_sql_query(query, conn)
            df.to_excel(writer, sheet_name=sheet_name, index=False)  # Save each DataFrame to a separate sheet
    print(f"Data saved to {STATEMENTS}")
except Exception as e:
    print(f"Error: {e}")
finally:
    if conn:
        conn.close()

df = pd.read_excel(STATEMENTS, engine="openpyxl")
df = df[columns_to_keep]
df.iloc[:, 3:] = df.iloc[:, 3:].fillna(False).astype(bool).astype(int)

for score_col, prefix in score_categories.items():
    matching_cols = [col for col in df.columns if col.startswith(prefix)]
    df[score_col] = df[matching_cols].sum(axis=1) / len(matching_cols)

df["overall_score"] = df[list(score_categories.keys())].sum(axis=1)
df = df[final_columns]
df.to_excel(SNOWFLAKE, index=False, engine="openpyxl")

print(f"Processed data saved to {SNOWFLAKE}")


