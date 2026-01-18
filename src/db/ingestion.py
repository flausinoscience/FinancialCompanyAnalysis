import io, csv
from sqlalchemy import text


def batch_insert(engine, table, columns, rows, batch_size=2000):
    cols = ', '.join(f'"{c}"' for c in columns)
    placeholders = ', '.join(f':{c}' for c in columns)

    sql = text(f'''
        INSERT INTO public."{table}" ({cols})
        VALUES ({placeholders})
    ''')

    batch = []

    with engine.begin() as conn:
        for row in rows:
            batch.append(dict(zip(columns, row)))

            if len(batch) >= batch_size:
                conn.execute(sql, batch)
                batch.clear()

        if batch:
            conn.execute(sql, batch)


def run_sql_file(engine, path):
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()

    with engine.begin() as conn:
        conn.execute(text(sql))

        
def copy_stream(engine, table, columns, rows):
    cols = ', '.join(f'"{col}"' for col in columns)
    copy_sql = f'COPY public."{table}" ({cols}) FROM STDIN WITH CSV'

    raw_conn = engine.raw_connection()
    try:
        cur = raw_conn.cursor()

        buf = io.StringIO()
        writer = csv.writer(buf)
        rows_in_buf = 0

        for row in rows:
            writer.writerow(row)
            rows_in_buf += 1

            if rows_in_buf >= 20_000:
                buf.seek(0)
                cur.copy_expert(copy_sql, buf)
                raw_conn.commit()
                buf = io.StringIO()
                writer = csv.writer(buf)
                rows_in_buf = 0

        if rows_in_buf:
            buf.seek(0)
            cur.copy_expert(copy_sql, buf)
            raw_conn.commit()

    finally:
        cur.close()
        raw_conn.close()
