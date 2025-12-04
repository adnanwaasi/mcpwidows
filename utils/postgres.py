import psycopg2

# Connect to PostgreSQL
def connect_to_postgres():
    conn = psycopg2.connect(
        dbname="meme",
        user="adnan",
        password="123",
        host="localhost",
        port=5432
    )
    cursor = conn.cursor()
    return conn, cursor

def push_data_to_postgres(session_id, prompt, output):
    conn, cursor = connect_to_postgres()
    sql_query = "INSERT INTO llm ( id, prompt, output) VALUES (%s, %s, %s)"
    cursor.execute(sql_query, (session_id,  prompt, output))
    conn.commit()
    cursor.close()
    conn.close()

def fetch_data_from_postgres():
    conn, cursor = connect_to_postgres()
    sql_query = "SELECT * FROM llm"
    cursor.execute(sql_query)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records  
if __name__ == "__main__":

    push_data_to_postgres(1, "sample prompt", "sample output")
    data = fetch_data_from_postgres()
    print(data)
