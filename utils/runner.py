import code_seperator as cs
import change_maker as cm
import code_gen_with_groq as cg
import postgres
import os  
count =0 
if count ==0 :
    prompt=input("Enter your prompt : ")
    content = cg.generate_code_with_groq(prompt)

    cs.write_code_to_files(content)
    count +=1
    postgres.push_data_to_postgres(1, prompt, content)  # Save to PostgreSQL

print("your files are generated successfully ")
flag=False
yes_set = {"yes","y","sure","ok","please","do it","yeah"} 
no_set = {"no","n","not now","later","don't","dont"}
while not flag :
    ans=input("Do you want to update the code ? (yes/no) : ").lower()
    if ans in yes_set :
        flag=True
    elif ans in no_set :
        flag=False
        break 
    else :  
        print("Invalid input. Please respond with 'yes' or 'no'.")
    if flag :
        update_prompt=input("Enter your update prompt : ")
        updated_code=cm.update_context(update_prompt,content)
        cs.write_code_to_files(updated_code)
        print("Your code is updated successfully ") 
