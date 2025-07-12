import psycopg2
import time
import os
import sys

def wait_for_postgres(
    host='db',
    port=5432,
    dbname='vaultgres',
    user='db_root',
    password='db_root',
    retries=10,
    delay=3
):
    print(f"[db_wait] Waiting for PostgreSQL at {host}:{port}...", flush=True)
    for i in range(retries):
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=user,
                password=password
            )
            conn.close()
            print("[db_wait] Connection successful.")
            return True
        except Exception as e:
            print(f"[db_wait] Attempt {i+1}/{retries} failed: {e}")
            time.sleep(delay)
    print("[db_wait] Database not reachable after retries.")
    return False

if __name__ == "__main__":
    success = wait_for_postgres()
    if not success:
        sys.exit(1)
        
