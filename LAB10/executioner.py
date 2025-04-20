import psycopg2

conn = psycopg2.connect(
    dbname="snake_game", 
    user="postgres", 
    password="A2682772aa", 
    host="localhost", 
    port="5432"
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL
);
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS "user_score" (
    user_id INTEGER PRIMARY KEY REFERENCES "user"(id),
    score INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1
);
""")

conn.commit()
cur.close()
conn.close()

print("========Executed successfully========")