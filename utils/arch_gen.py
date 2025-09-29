import os 
from groq import Groq

def generate_architecture_with_groq(strings):
    current_working_directory = os.getcwd()
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))  # Use environment variable for API key

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "you are a coding architecture expert and you only give os file systems for a project and you dont do anything else like ./currentdir/main.py ./currentdir/utils/helper.py etc and you only give the file system dont give any explanations just write the file system and do nothing dont give any language name or introduction just write the file system don't start and end with ``` or anything else just write the file system",
            },
            {
                "role": "user",
                "content": strings,
            }
        ],
        model="llama-3.3-70b-versatile"  # Update to the correct model name if needed
    )

    return (chat_completion.choices[0].message.content)

###  call the function and convert the string to a list
def architecure_in_list(requested_feature):
    prompt = f"Generate a file system architecture for the following project: {requested_feature}. Use './' to represent the current working directory: {os.getcwd()}"
    architecture = generate_architecture_with_groq(prompt)
    architecture_list = architecture.split('\n')
    return list(filter(None, architecture_list))  # Remove empty strings from the list
if __name__ == "__main__":
    # Example usage
    requested_feature = "a simple web application for a blog platform with user authentication and CRUD operations for posts"
    architecture = architecure_in_list(requested_feature)
    print("Generated Architecture:\n", architecture)
    