import re
import os
import code_gen_with_groq as cg
from dotenv import load_dotenv
import postgres
def write_code_to_files(content):
    # Extract all #file blocks
    blocks = re.findall(r"#file:(.*?)\n(.*?)#endfile", content, re.S)

    # Save code before the first #file: block as app.py
    prefile_code = content.split("#file:")[0].strip()
    if prefile_code:
        with open("app.py", "w", encoding="utf-8") as f:
            f.write(prefile_code + "\n")
        print("Created file: app.py")

    # Write each #file block
    for filepath, code_text in blocks:
        filepath = filepath.strip()
        code_text = code_text.strip()

        # Create directories if needed
        folder = os.path.dirname(filepath)
        if folder:
            os.makedirs(folder, exist_ok=True)
            print(f"Created folder(s): {folder}")

        # Write file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code_text + "\n")
        print(f"Created file: {filepath}")

if __name__ == "__main__":
    load_dotenv()

    # Example usage — generate code using Groq
    prompt = "a simple flask application with a home page and about page and a contact page , my name is adnan and my contact number is 1234567890 and my email is adnan@example.com make a css files for necessary to make it more stylish"    
    content = cg.generate_code_with_groq(prompt)

    write_code_to_files(content)
    postgres.push_data_to_postgres(1, prompt, content)  # Save to PostgreSQL