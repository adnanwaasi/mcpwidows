import re
import os
import code_gen_with_groq as cg
from dotenv import load_dotenv
import postgres

def write_code_to_files(content, project_dir=None):
    # Check if there is a #project_name: tag in the content
    match = re.search(r"#project_name:\s*([^\n\r]+)", content)
    extracted_project_name = match.group(1).strip() if match else None
    
    # Use the extracted project name if project_dir is not explicitly provided
    # Fallback to current directory "."
    final_project_dir = project_dir or extracted_project_name or "."

    if final_project_dir != ".":
        os.makedirs(final_project_dir, exist_ok=True)
        print(f"Created project folder: {final_project_dir}")

    # Remove the #project_name block from the content so it doesn't leak into app.py
    if match:
        content = content.replace(match.group(0), "").strip()

    # Extract all #file blocks
    blocks = re.findall(r"#file:(.*?)\n(.*?)#endfile", content, re.S)

    # Save code before the first #file: block as app.py
    prefile_code = content.split("#file:")[0].strip()
    if prefile_code:
        app_path = os.path.join(final_project_dir, "app.py")
        with open(app_path, "w", encoding="utf-8") as f:
            f.write(prefile_code + "\n")
        print(f"Created file: {app_path}")

    # Write each #file block
    for filepath, code_text in blocks:
        filepath = filepath.strip()
        full_filepath = os.path.join(final_project_dir, filepath) if final_project_dir != "." else filepath
        code_text = code_text.strip()

        # Create directories if needed
        folder = os.path.dirname(full_filepath)
        if folder:
            os.makedirs(folder, exist_ok=True)
            print(f"Created folder(s): {folder}")

        # Write file
        with open(full_filepath, "w", encoding="utf-8") as f:
            f.write(code_text + "\n")
        print(f"Created file: {full_filepath}")

    return final_project_dir

if __name__ == "__main__":
    load_dotenv()

    # Example usage — generate code using Groq
    prompt = "a simple flask application with a home page and about page and a contact page , my name is adnan and my contact number is 1234567890 and my email is adnan@example.com make a css files for necessary to make it more stylish"    
    content = cg.generate_code_with_groq(prompt)

    write_code_to_files(content)
    postgres.push_data_to_postgres(1, prompt, content)  # Save to PostgreSQL