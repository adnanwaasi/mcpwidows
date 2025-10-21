from groq import Groq
import os
import psycopg2
import code_seperator as cs
import postgres
from dotenv import load_dotenv
load_dotenv()
def update_context(strings,code):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))  # Use environment variable for API key

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a coding expert and you only changes the codes which are optimised , good and satisfying the user needs  , dont give any explanations just write the code and do nothing dont give any language name or introduction just write the code don't start and end with ``` or anything else just when you start the code put the filename starting with #file:filename.py and then write the code , after the code for the file has completed then #endfile.",
            },
            {
                "role": "user",
                "content": f"Here is the existing code:\n{code}\nNow, update the code with the following information:\n{strings}",
            }
        ],
        model="llama-3.3-70b-versatile"  # Update to the correct model name if needed
    )

    return (chat_completion.choices[0].message.content)
if __name__ == "__main__":
    conn=psycopg2.connect(
        dbname="meme",
        user="adnan",
        password="123",
        host="localhost",
        port=5432
    )
    cursor=conn.cursor()
    sql_query="SELECT response from llm ;"
    cursor.execute(sql_query)
    records=cursor.fetchall()
    code_snippet=records[-1]
    prompt=" in the home page make it animated and responsive and a hyperlink to my github profile with the url as 'https://github.com/adnanwaasi'"
    updated_code=update_context(prompt,code_snippet)
    print(f"Original Code Snippet:\n{code_snippet}\nUpdated Code Snippet:\n{updated_code}\n")
    cursor.close()
    conn.close()
    cs.write_code_to_files(updated_code)
    postgres.push_data_to_postgres(1,prompt,updated_code)