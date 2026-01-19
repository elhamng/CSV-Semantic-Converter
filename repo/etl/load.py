import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

from sqlalchemy import create_engine, text

load_dotenv()

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / "data"
MIGRATIONS_DIR = REPO_ROOT / "migrations"

CSV_ENCODING = os.getenv("CSV_ENCODING", "utf-8")
CSV_DELIMITER = os.getenv("CSV_DELIMITER", ",")

def get_database_url():
    user = os.getenv("PGUSER")
    password = os.getenv("PGPASSWORD")
    host = os.getenv("PGHOST", "localhost")
    port = os.getenv("PGPORT", "5432")
    database = os.getenv("PGDATABASE")
    if not all([user, password, database]):
        raise ValueError("Database credentials are not fully set in environment variables.")

    return f"postgresql://{user}:{password}@{host}:{port}/{database}"

def get_engine():
    database_url = get_database_url()
    return create_engine(database_url)

def ensure_migrations_table(engine):
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS migrations (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.commit()

def run_migrations(engine):
    ensure_migrations_table(engine)
    files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    with engine.connect() as conn:
        applied_files = {
            row['filename'] for row in conn.execute(text("SELECT filename FROM migrations")).fetchall()
        }
        for file in files:
            if file.name in applied_files:
                continue
            with open(file) as f:
                sql = f.read_text(encoding ="utf-8")
                conn.execute(text(sql))
                conn.execute(text("""
                    INSERT INTO migrations (filename) VALUES (:filename)
                """), {"filename": file.name})
                print(f"Applied migration: {file.name}")
        conn.commit()
def load_data(engine, csv_path : Path, table_name: str):
    df = pd.read_csv(csv_path, encoding = CSV_ENCODING, sep=CSV_DELIMITER) 
    with engine.connect() as conn:
        df.to_sql(table_name, conn, if_exists='append', index=False,method='multi', chunksize=100)
        print(f"Loaded data into {table_name} from {csv_path.name}")
def main():
    engine = get_engine()
    run_migrations(engine)

    csv_files = {
        "exampleone.csv": "Exampleone",
        "exampletwo.csv": "Exampletwo",
        "examplethree.csv": "Examplethree"
    }

    for csv_file, table_name in csv_files.items():
        csv_path = DATA_DIR / csv_file
        load_data(engine, csv_path, table_name)
if __name__ == "__main__":
    main()
