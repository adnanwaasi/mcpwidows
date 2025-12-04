import code_gen_with_groq
from dotenv import load_dotenv
import os
import langgen as langgen
import postgres

# Load environment variables from .env file
load_dotenv()

def generate_code(strings, filename):
    # Pass filename context for unique code per file
    prompt = f"Generate a python code for the following feature: {strings}. You are working in various files and currently you are in {filename}. Generate only the code required inside this file, and ensure it is unique and relevant to the filename."
    return langgen.initialize(prompt)

### to write the code to a file and create directories if needed
def write_code_to_file(code, filename):
    dir_path = os.path.dirname(filename)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
    with open(filename, 'w') as file:
        file.write(code)
    print(f"Code written to {filename}")

def generate_and_write_code(requested_feature, language, filename):
    code = generate_code(requested_feature, filename)
    write_code_to_file(code, filename)
    return code
### invoke the function for multiple times over the file in the architecture list


def push_to_postgres(prompt,user_id=1,output=""):
    conn,cursor=postgres.connect_to_postgres()
    sql_query = "INSERT INTO llm values (prompt,user_id,output)"

if __name__ == "__main__":
    # Example usage
    requested_feature = "a fibonacci series in python"
    language = "python"