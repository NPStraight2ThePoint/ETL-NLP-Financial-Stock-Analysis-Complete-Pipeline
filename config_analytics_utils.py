# Simply Wall St API configs
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
from pathlib import Path
def load_env():
    load_dotenv()
    def raise_error(var):
        raise EnvironmentError(f"{var} not found in .env file")
    return {
        "API_KEY": os.getenv("API_KEY") or raise_error("API_KEY"),
        "DB_USER": os.getenv("DB_USER") or raise_error("DB_USER"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD") or raise_error("DB_PASSWORD"),
        "DB_HOST": os.getenv("DB_HOST") or raise_error("DB_HOST"),
        "DB_PORT": os.getenv("DB_PORT") or raise_error("DB_PORT"),
        "DB_NAME": os.getenv("DB_NAME") or raise_error("DB_NAME"),
        "DB_NAME2": os.getenv("DB_NAME2") or raise_error("DB_NAME2")
    }
# Load once and expose
_env = load_env()
DB_USER = _env["DB_USER"]
DB_PASSWORD = _env["DB_PASSWORD"]
DB_HOST = _env["DB_HOST"]
DB_PORT = _env["DB_PORT"]
DB_NAME = _env["DB_NAME"]
DB_NAME2 = _env["DB_NAME2"]

# Connection setup
user = DB_USER
password = DB_PASSWORD
host = DB_HOST
port = DB_PORT
db = DB_NAME
db2 = DB_NAME2
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db2}')

SRC_DB = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
DEST_DB = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME2}"

# Database connection parameters
db_config = {
    'dbname': DB_NAME2,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST,  # or remote host
    'port': DB_PORT         # default PostgreSQL port
}

output_dir = Path('C:/.../.venv/output')
