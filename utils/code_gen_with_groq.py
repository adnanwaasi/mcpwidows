import os
from groq import Groq

def generate_code_with_groq(strings):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))  # Use environment variable for API key

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a coding expert and you only give codes which are optimised and good , dont give any explanations just write the code and do nothing dont give any language name or introduction just write the code don't start and end with ``` or anything else just when you start the code put the filename starting with #file:filename.py and then write the code , after the code for the file has completed then #endfile.",
            },
            {
                "role": "user",
                "content": strings,
            }
        ],
        model="llama-3.3-70b-versatile"  # Update to the correct model name if needed
    )

    return (chat_completion.choices[0].message.content)
if __name__ == "__main__":
    feature = "a simple expense tracker  using nodejs, react and expressjs"
    code = generate_code_with_groq(feature)
    print(code)
