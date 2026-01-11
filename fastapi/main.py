from fastapi import FastAPI, Response
import psycopg2
import os
import time
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

DATABASE_URL = os.environ["DATABASE_URL"]

Instrumentator().instrument(app).expose(app)

def get_connection():
    for i in range(30):  # ~30 seconds max
        try:
            conn = psycopg2.connect(DATABASE_URL)
            conn.autocommit = True
            print("Connected to Postgres")
            return conn
        except psycopg2.OperationalError as e:
            print(f"Postgres not ready, retrying... ({i+1})")
            time.sleep(1)
    raise Exception("Could not connect to Postgres")

conn = get_connection()
conn.autocommit = True

@app.on_event("startup")
def init_db():
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id SERIAL PRIMARY KEY,
                sim_num INT,
                payload TEXT,
                created_at TIMESTAMP DEFAULT now()
            );
        """)

        cur.execute("""
            INSERT INTO events (sim_num, payload)
            SELECT
              (random() * 100000)::int AS sim_num,
              (
                'Status changed to ' ||
                (ARRAY['ACTIVE','SUSPENDED','PROVISIONED','DEACTIVATED'])[floor(random() * 4) + 1] ||
                ' via ' ||
                (ARRAY['API','BATCH_JOB','UI','SYNC_PROCESS'])[floor(random() * 4) + 1] ||
                ' at ' ||
                now() - (random() * interval '90 days')
              ) AS payload
            FROM generate_series(1, 500000);
        """)

@app.get("/slow")
def slow_query(
    sim_num: int,
    page: int = 1,
    page_size: int = 10,
):
    offset = (page - 1) * page_size

    with conn.cursor() as cur:
        cur.execute("""
            SELECT payload, created_at
            FROM events
            WHERE sim_num = %s
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s;
        """, (sim_num, page_size, offset))
        rows = cur.fetchall()

    return {
        "sim_num": sim_num,
        "page": page,
        "page_size": page_size,
        "items": [
            {
                "payload": r[0],
                "created_at": r[1].isoformat()
            }
            for r in rows
        ]
    }
