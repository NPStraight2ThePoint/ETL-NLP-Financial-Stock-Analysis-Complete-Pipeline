import requests
import pandas as pd
from dotenv import load_dotenv
from dir_utils import FDM, output_dir
from api_queries import QUERY_EXCHANGES
from config_utils import url, headers, API_KEY

file_path = output_dir / f"exchanges_{FDM}.csv"

response = requests.post(url,json={'query': QUERY_EXCHANGES},headers=headers)

if response.status_code == 200:
    data = response.json()
    exchanges = data['data']['exchanges']
    df = pd.DataFrame(exchanges)
    df = df.rename(columns={'symbol': 'exchange', 'companiesCount': 'company_count'})
    df.insert(0, 'index_date', FDM)
    df.to_csv(file_path, index=False)
    print(f"CSV saved as exchanges_{FDM}.csv")
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")
