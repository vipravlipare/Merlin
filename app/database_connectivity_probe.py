import sys
import psycopg
import getpass

def probe_database():
    try:
        password = getpass.getpass(prompt='Password: ', stream=None)
        with psycopg.connect(host="127.0.0.1", port=55432, dbname="merlin_d6", user="merlin_d6", password=password, connect_timeout=3) as conn:
            conn.read_only = True
            with conn.cursor() as cur:
                cur.execute("SELECT current_database(), current_user;")
                db_name, db_user = cur.fetchone()

        print(f"PROBE SUCCESS: Connected to database '{db_name}' as user '{db_user}'.")
        sys.exit(0)

    except psycopg.Error:
        print("DB Probe Failed: Connection or query failed.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    probe_database()
