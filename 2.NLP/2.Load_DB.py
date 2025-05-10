import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

today = datetime.now().replace(day=1)
today = today.strftime("%Y-%m-%d")

output_file = f'C:/***/Output/Snowflake_{today}.xlsx'
df = pd.read_excel(output_file, engine='openpyxl')
DB_PARAMS = {
            "host": "localhost",
            "port": "5432",
            "database": "***",
            "user": "***",
            "password": "***"}

engine = create_engine('postgresql+psycopg2://postgres:Arxidolemios39@localhost:5432/Simply_API_Prod')

df.to_sql("snowflake", engine, if_exists='append', index=False)






