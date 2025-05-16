import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from config_nlp_utils import DB_PARAMS, engine
from dir_nlp_utils import FDM, output_dir

exchanges_file = output_dir / f"exchanges_{FDM}.csv"
df1 = pd.read_csv(exchanges_file, encoding='utf-8')
exchange = df1['exchange'].iloc[0]
SNOWFLAKE = f'C:/.../.venv/2.Enhancement/Output/{exchange}_Snowflake_{FDM}.xlsx'
df = pd.read_excel(SNOWFLAKE, engine='openpyxl')
df.to_sql("snowflake", engine, if_exists='append', index=False)
FINANCIALS = output_dir / f"NLP_{exchange}_Transposed_{exchange}_statements_{FDM}.csv"
df2 = pd.read_csv(FINANCIALS)
df2.to_sql("company_financials", engine, if_exists='append', index=False)

print('Data has been successfully loaded in company_financials / Simply_Prod DB')






