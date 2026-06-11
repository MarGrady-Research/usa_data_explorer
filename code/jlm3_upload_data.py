import os
import io
import csv
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# 1. Custom function to stream data using native Postgres COPY
def psql_insert_copy(table, conn, keys, data_iter):
    """
    Optimized copy method that streams dataframe rows into PostgreSQL.
    """
    s_buf = io.StringIO()
    writer = csv.writer(s_buf)
    writer.writerows(data_iter)
    s_buf.seek(0)

    # FIX: SQLAlchemy 2.0+ requires .dbapi_connection to get the raw driver
    dbapi_conn = conn.connection.dbapi_connection
    with dbapi_conn.cursor() as cur:
        # Standard unquoted keys are safe now since they are clean snake_case
        sql = f"COPY {table.name} ({', '.join(keys)}) FROM STDIN WITH CSV"
        cur.copy_expert(sql=sql, file=s_buf)

# 2. Load secret variables from .env file
load_dotenv()

# 3. Grab the database URL
DB_URI = os.getenv("SUPABASE_DB_URL")

# Fix SQLAlchemy driver string requirements
if DB_URI and DB_URI.startswith("postgres://"):
    DB_URI = DB_URI.replace("postgres://", "postgresql://", 1)

# 4. Create the connection engine
engine = create_engine(DB_URI)

# 5. Import data
analysis = pd.read_parquet("data/test_percentiles.parquet")

# 6. Stream dataframe directly to Supabase using a stable connection context
print("Streaming snake_case data to the cloud... please wait.")
try:
    # Use engine.begin() to open a strict, un-dropped connection wrapper
    with engine.begin() as connection:
        analysis.to_sql(
            name='test_percentiles', 
            con=connection,              # Use the live block connection
            if_exists='replace',         # Safe to replace since database is snake_case
            index=False,
            chunksize=50000,          
            method=psql_insert_copy   
        )
    print("🚀 Data successfully streamed and uploaded in snake_case!")
except Exception as e:
    print(f"\n❌ Upload failed with the following error:\n{e}")