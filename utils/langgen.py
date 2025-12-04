import getpass
import os
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

def main():
    if "GROQ_API_KEY" not in os.environ:
        os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your GROQ API key: ")
    else:
        print("API key initialized")
    prompt=input("Enter your prompt: ")
    initialize(prompt)

def initialize(prompt="print('Hello, World!')"):
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        max_tokens=256,
        timeout=None,
        max_retries=2
    )

    memory = ConversationBufferMemory(return_messages=True)

    # Define the system prompt properly here
    system_prompt = (
        "You are a coding expert. Only output optimized, clean code. "
        "Do not explain anything. "
        "Start every file with '#file:<filename>.py' and end with '#endfile'. "
        "Do not use ``` or language names."
    )

    # Create a template that combines system + user prompt
    prompt_template = PromptTemplate(
        input_variables=["history", "input"],
        template=(
            f"{system_prompt}\n\n"
            "Conversation so far:\n{history}\n\n"
            "User: {input}\nAssistant:"
        )
    )

    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt_template,
        verbose=True
    )

    response = conversation.predict(input=prompt)
    print(response)
    return response


if __name__ == "__main__":
    main()
