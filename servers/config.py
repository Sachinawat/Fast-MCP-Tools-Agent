import os
import logging
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

# --- LOAD ENVIRONMENT VARIABLES ---
# This looks for .env in the Fastmcp root
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

# --- Paths & Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "enterprise_memory.db")
LOG_PATH = os.path.join(BASE_DIR, "system_events.log")

# --- Centralized Logging ---
logger = logging.getLogger("EnterpriseMCP")
logger.setLevel(logging.INFO)
# Clear existing handlers to avoid duplicates if reloaded
if logger.hasHandlers():
    logger.handlers.clear()
    
file_handler = logging.FileHandler(LOG_PATH)
formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "msg": "%(message)s"}')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# --- SQL Audit Trail ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS audit_logs
                 (id INTEGER PRIMARY KEY, session_id TEXT, tool TEXT, input TEXT, output TEXT, timestamp DATETIME)''')
    conn.commit()
    conn.close()

def log_audit(session_id, tool, input_data, output_data):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO audit_logs (session_id, tool, input, output, timestamp) VALUES (?, ?, ?, ?, ?)",
                  (session_id, tool, str(input_data), str(output_data), datetime.now()))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"DB Error: {e}")

init_db()