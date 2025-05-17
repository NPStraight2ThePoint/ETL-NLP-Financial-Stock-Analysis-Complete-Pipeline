import pandas as pd
from sqlalchemy import create_engine, text
from config_analytics_utils import db_config, output_dir, engine
import numpy as np

# Set exchange dynamically
exchange = 'ASX'

# Output file path
output_dir.mkdir(parents=True, exist_ok=True)
top_50_file = output_dir / f"top_50_companies_returns_{exchange}.csv"

# Use named parameters (:exchange) and SQLAlchemy text()
query = text("""
SELECT cf.date,
       cf.ticker,
       cf.exchange,
       l.primary_industry,
       l.secondary_industry,
       cf."Current Price",
       cf."DCF Fair Value",
       cf."Dividend Yield %",
       cf."3 month weekly volatility %"
FROM public.company_financials cf
JOIN public.listings l ON cf.ticker = l.ticker_symbol and cf.exchange = l.exchange_symbol
WHERE cf.exchange = :exchange
  AND cf.ticker IN (
      SELECT ticker
      FROM snowflake
      WHERE exchange = :exchange
      ORDER BY overall_score DESC
      LIMIT 50
  );
""")

try:

    # Run parameterized query using SQLAlchemy's `text` and `params`
    with engine.connect() as conn:
        df_top_50 = pd.read_sql_query(query, conn, params={"exchange": exchange})

    # Export to CSV
    #df_top_50.to_csv(top_50_file, index=False)
    print(f"✅ Top 50 companies exported successfully to {top_50_file}")
except Exception as e:
    print("❌ Error:", e)

df = pd.read_csv(top_50_file)

# Set risk-free rate (Rf)
Rf = 0.035

# Remove 'A$' and convert to float
df['Current Price'] = df['Current Price'].replace('[A$]', '', regex=True).astype(float)
df['Analyst 1 Year Target'] = df['Analyst 1 Year Target'].replace('[A$]', '', regex=True).astype(float)
df['Dividend Yield %'] = pd.to_numeric(df['Dividend Yield %'], errors='coerce').fillna(0.0)
df['Volatility %'] = df['3 month weekly volatility %'] * np.sqrt(52)

# Calculate new columns
df['Price Return'] = (df['Analyst 1 Year Target'] - df['Current Price']) / df['Current Price']
df['Total Return'] = (df['Analyst 1 Year Target'] - df['Current Price'] + df['Dividend Yield %']) / df['Current Price']
df['Sharpe Ratio'] = (df['Total Return'] - Rf) / df['3 month weekly volatility %']

# Round for better readability
df = df.round({
    'Price Return': 4,
    'Total Return': 4,
    'Sharpe Ratio': 4
})

# Save to a new file
enhanced_file = output_dir / f"top_50_companies_final_returns_{exchange}.csv"
df.to_csv(enhanced_file, index=False)

print(f"✅ Enhanced CSV with returns and Sharpe Ratio saved to {enhanced_file}")
