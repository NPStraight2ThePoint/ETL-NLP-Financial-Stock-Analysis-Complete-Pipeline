import subprocess
import os
from datetime import datetime
from config_utils import API_KEY, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DB_NAME2
from dir_utils import BACKUP_DIR

DATE = datetime.now().strftime("%Y%m%d_%H%M%S")  # Create unique backup file names
BACKUP_FILE = os.path.join(BACKUP_DIR, f"{DB_NAME2}_backup_{DATE}.sql")
pg_dump_path = r"C:\Program Files\PostgreSQL\17\bin\pg_dump.exe"
os.makedirs(BACKUP_DIR, exist_ok=True)

pg_dump_command = [
    pg_dump_path,
    "-U", DB_USER,
    "-h", DB_HOST,
    "-p", str(DB_PORT),
    "-F", "c",
    "-f", BACKUP_FILE,
    DB_NAME2
]

def create_backup():
    os.environ["PGPASSWORD"] = DB_PASSWORD
    try:
        # Run the pg_dump command
        print(f"🧳 Creating backup of {DB_NAME2}...")
        subprocess.run(pg_dump_command, check=True)
        print(f"✅ Backup saved to {BACKUP_FILE}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during backup: {e}")
    finally:
        del os.environ["PGPASSWORD"]  # Clean up the environment variable after use

def main():
    print("🚀 Starting database backup process...")
    create_backup()
    print("\n✅ Backup process completed.")

if __name__ == "__main__":
    main()