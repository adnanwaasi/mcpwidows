import code_gen_with_groq as cg
import arch_gen 
from dotenv import load_dotenv
import os


def seperate_code_and_architecture(code):
    # Define delimiters
    start="#file:"
    end="#endfile"
    file_and_code = {}
    ## you can split the code by the start delimiter and then for each part you can split it by the end delimiter and then you can get the filename and the code
    for part in code.split(start)[1:]:
        filename, code = part.split(end, 1)
        file_and_code[filename.strip()] = code.strip()
    return file_and_code
## chatgpt generated code to write the code to files i have to corrrrect this code too 
import re


content = '''#file:main.py
def main():
    print("Hello, World!")
#endfile

#file:utils.py
def helper():
    return "This is a helper function."
#endfile'''

# find blocks of #file:name ... #endfile
blocks = re.findall(r"#file:(.*?)\n(.*?)#endfile", content, re.S)

for filename, code in blocks:
    filename = filename.strip()
    with open(filename, "w") as f:
        f.write(code.strip() + "\n")
        print(f"Writing to {filename}:\n{code.strip()}\n")
    print(f"Created {filename}")


### chatgpt bro Then run:
if __name__ == "__main__":
    # Example usage
    code = """#file:main.py
def main():
    print("Hello, World!")
#endfile

#file:utils.py
def helper():
    return "This is a helper function."
#endfile
"""
    # result = separate_code_and_architecture(code)
    # print(result)