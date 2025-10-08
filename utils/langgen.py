import getpass
import os
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

def main():
    # Ask for API key if not already set
    while "GROQ_API_KEY" not in os.environ:
        os.environ["GROQ_API_KEY"] = getpass.getpass("enter your api key")
    else:
        print("api key initialized")
    slave=initialize(prompt="can u give me simple html js and css file system architecture for a static web site")
    # hello = initialize(prompt="Generate a fibonacci sequence in python")
    # print(hello)
    print(f"slave: {slave}")

def initialize(prompt="print('Hello, World!')"):
    # Create LLM
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        max_tokens=256,
        timeout=None,
        max_retries=2
    )

    # Reinstantiate memory every run
    memory = ConversationBufferMemory(return_messages=True)

    # Create conversation chain with memory
    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        verbose=True
    )

    # Improved system prompt
    system_prompt = (
        "You are a coding expert. Only output optimized code, no explanations, no language name, no intro, just code. "
        "Remove any backticks and language names. You can also work as a file system expert and provide file system architecture for a project, "
        "but you must not provide both file system architecture and code in the same response. When acting as a file system expert, do not write code. "
        "When acting as a coding expert, do not write file system architecture."
        "when user mentions a filename in the prompt, you must provide code only for that file and ensure it is unique and relevant to the filename."
        " you have to understand the context of the filename and provide code accordingly."
        " you need to generate the filenames when user specifically mentions 'file system architecture' in the prompt."
    )
    conversation.predict(input=system_prompt)
    return conversation.predict(input=prompt)
    
def architecure_in_list(requested_feature):
    prompt = f"Generate a file system architecture for the following project: {requested_feature}. Use './' to represent the current working directory: {os.getcwd()}"
    architecture = initialize(prompt)
    architecture_list = architecture.split('\n')
    return list(filter(None, architecture_list))
if __name__ == "__main__":
    main()