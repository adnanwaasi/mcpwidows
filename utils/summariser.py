from groq import Groq
import os
import psycopg2

def summarise_code(code_snippet):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))  # Use environment variable for API key

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a coding expert. Summarize the following code snippet in a concise manner, focusing on its functionality and purpose.",
            },
            {
                "role": "user",
                "content": f"Here is the code snippet:\n{code_snippet}",
            }
        ],
        model="llama-3.3-70b-versatile"  # Update to the correct model name if needed
    )

    return chat_completion.choices[0].message.content
if __name__ == "__main__":
    # Example usage
    ## read from the db 
    conn = psycopg2.connect(
        dbname="meme",
        user="adnan",
        password="123",
        host="localhost",
        port=5432
    )
    cursor = conn.cursor()
    sql_query = "SELECT response from llm ;"
    cursor.execute(sql_query)
    records = cursor.fetchall()
    for record in records:
        code_snippet = record[0]
        summary = summarise_code(code_snippet)
        print(f"Code Snippet:\n{code_snippet}\nSummary:\n{summary}\n")
    cursor.close()
    conn.close()