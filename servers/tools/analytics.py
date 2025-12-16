import sqlite3
import pandas as pd
from servers.config import DB_PATH

def get_logs(limit=5):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT {limit}", conn)
    conn.close()
    return df.to_dict(orient="records")