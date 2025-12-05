import time
import psycopg2

time.sleep(5)  # wait for DB container

try:
    conn = psycopg2.connect(
        host="my-postgres",
        database="mydb",
        user="user",
        password="pass"
    )
    cursor = conn.cursor()

    print("Connected to PostgreSQL!")

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100)
        );
    """)
    conn.commit()
    print("Table created!")

    # Insert multiple values
    names = ["Vamsi", "Ris", "Kalyan", "Teja"]

    print("Inserting rows...")
    for name in names:
        cursor.execute("INSERT INTO people (name) VALUES (%s) RETURNING id;", (name,))
        inserted_id = cursor.fetchone()[0]
        print(f"Inserted row -> ID: {inserted_id}, Name: {name}")

    conn.commit()

    # Fetch all rows
    print("\nFetching all rows from table:")
    cursor.execute("SELECT * FROM people;")
    rows = cursor.fetchall()

    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]}")

    cursor.close()
    conn.close()

except Exception as e:
    print("Error:", e)
