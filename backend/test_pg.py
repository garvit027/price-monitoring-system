import psycopg2

users = ["garvitjuneja27", "postgres", "root", "admin"]
passwords = ["", "password", "postgres", "admin", "1234"]
dbs = ["postgres", "garvitjuneja27", "template1"]

success = False
for db in dbs:
    for u in users:
        for p in passwords:
            try:
                conn = psycopg2.connect(dbname=db, user=u, password=p, host="localhost", port=5432, connect_timeout=1)
                print(f"SUCCESS: postgresql://{u}:{p}@localhost:5432/{db}")
                success = True
                conn.close()
                break
            except Exception:
                pass
        if success: break
    if success: break

if not success:
    print("FAILED ALL")
