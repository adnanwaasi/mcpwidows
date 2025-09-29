import code_gen_with_groq

def generate_code(strings):
    return code_gen_with_groq.generate_code_with_groq(strings)

### to write the code to a file
def write_code_to_file(code, filename):
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