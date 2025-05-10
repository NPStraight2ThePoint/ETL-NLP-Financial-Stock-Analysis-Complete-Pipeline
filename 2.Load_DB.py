import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

today = datetime.now().replace(day=1)
today = today.strftime("%Y-%m-%d")

output_file = f'C:/Users/nicho/PycharmProjects/Projects/API2SQL Pipelines/SWS API Production_V2/SWS_API_Prod_V2/.venv/2.Enhancement/Output/Snowflake_{today}.xlsx'
df = pd.read_excel(output_file, engine='openpyxl')
DB_PARAMS = {
            "host": "localhost",
            "port": "5432",
            "database": "Simply_API_Prod",
            "user": "postgres",
            "password": "Arxidolemios39"}

engine = create_engine('postgresql+psycopg2://postgres:Arxidolemios39@localhost:5432/Simply_API_Prod')

df.to_sql("snowflake", engine, if_exists='append', index=False)






