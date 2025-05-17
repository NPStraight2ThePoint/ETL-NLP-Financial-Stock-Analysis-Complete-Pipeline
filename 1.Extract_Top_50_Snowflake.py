import pandas as pd
import psycopg2
from config_analytics_utils import db_config, output_dir


exchange = 'ASX'  # You can set this dynamically

top_50_file = output_dir / f"top_50_companies_{exchange}.csv"

# SQL query with placeholder for parameter
query = """
    SELECT *
    FROM snowflake
    WHERE exchange = %s
    ORDER BY overall_score DESC
    LIMIT 50;
"""

try:
    conn = psycopg2.connect(**db_config)
    df_top_50 = pd.read_sql_query(query, conn, params=(exchange,))
    df_top_50.to_csv(top_50_file, index=False)
    print("✅ Top 50 companies exported successfully.")
except Exception as e:
    print("❌ Error:", e)
finally:
    if 'conn' in locals():
        conn.close()
