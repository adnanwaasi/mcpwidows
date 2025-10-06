import code_gen_with_groq
import arch_gen as arch_gen
from dotenv import load_dotenv
import os
import langgen as langgen
# Load environment variables from .env file
load_dotenv()

def generate_code(strings):
    return langgen.initialize(strings)

### to write the code to a file and create directories if needed
def write_code_to_file(code, filename):
    dir_path = os.path.dirname(filename)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
    with open(filename, 'w') as file:
        file.write(code)
    print(f"Code written to {filename}")

def get_prompt_for_code_generation(requested_feature, language, filename):
    return f"Generate a {language} code for the following feature: {requested_feature}. Save the code in a file named {filename}."
    ### pass it to the code generation model

def generate_and_write_code(requested_feature, language, filename):
    prompt = get_prompt_for_code_generation(requested_feature, language, filename)
    code = generate_code(prompt)
    write_code_to_file(code, filename)
    return code
### invoke the function for multple times over the file in the architecture list
def generate_code_for_architecture(requested_feature, language):
    architecture = arch_gen.architecure_in_list(requested_feature)
    for file in architecture: 
        code = generate_and_write_code(requested_feature, language, file)
        print(f"Generated code for {file}:\n{code}\n")
        
if __name__ == "__main__":
    # Example usage
    requested_feature = "a simple web application for a blog platform"
    language = ["HTML", "CSS", "JavaScript"]
    generate_code_for_architecture(requested_feature, language)