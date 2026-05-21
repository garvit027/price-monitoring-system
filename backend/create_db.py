import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='Varnit@2010', host='localhost', port=5432)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute('CREATE DATABASE price_monitor;')
    cur.close()
    conn.close()
    print("Database price_monitor created successfully.")
except Exception as e:
    print(f"Error creating database: {e}")
